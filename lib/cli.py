# lib/cli.py

from helpers import (
    exit_program,
    helper_1
)
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create the database engine
engine = create_engine('sqlite:///bourbon_collection.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define the Collection model class
class Collection(Base):
    __tablename__ = 'collections'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    bourbons = relationship('Bourbon', back_populates='collection')

    def create(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def get_all():
        return session.query(Collection).all()

    @staticmethod
    def find_by_id(collection_id):
        return session.query(Collection).filter_by(id=collection_id).first()

# Define the Bourbon model class
class Bourbon(Base):
    __tablename__ = 'bourbons'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    collection_id = Column(Integer, ForeignKey('collections.id'))
    collection = relationship('Collection', back_populates='bourbons')

    def create(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def get_all():
        return session.query(Bourbon).all()

    @staticmethod
    def find_by_id(bourbon_id):
        return session.query(Bourbon).filter_by(id=bourbon_id).first()

# Create the database tables
Base.metadata.create_all(engine)

# CLI interface
def display_menu():
    print("1. Create Collection")
    print("2. Delete Collection")
    print("3. Display All Collections")
    print("4. View Bourbons in Collection")
    print("5. Create Bourbon")
    print("6. Add Bourbon to a Collection")
    print("7. Delete Bourbon")
    print("8. Display All Bourbons")
    print("9. Find Bourbon by Name")
    print("0. Exit")

def create_collection():
    name = input("Enter the name of the collection: ")
    collection = Collection(name=name)
    collection.create()
    print("Collection created successfully!")

def delete_collection():
    collections = Collection.get_all()
    if collections:
        print("Select a collection to delete:")
        for collection in collections:
            print(f"ID: {collection.id}, Name: {collection.name}")
        collection_id = int(input("Enter the ID of the collection to delete: "))
        collection = next((c for c in collections if c.id == collection_id), None)
        if collection:
            collection.delete()
            print("Collection deleted successfully!")
        else:
            print("Collection not found.")
    else:
        print("No collections found.")

def display_all_collections():
    collections = Collection.get_all()
    if collections:
        for collection in collections:
            print(f"ID: {collection.id}, Name: {collection.name}")
    else:
        print("No collections found.")

def view_bourbons_in_collection():
    collections = Collection.get_all()
    if collections:
        print("Select a collection:")
        for collection in collections:
            print(f"ID: {collection.id}, Name: {collection.name}")
        collection_id = int(input("Enter the ID of the collection: "))
        collection = next((c for c in collections if c.id == collection_id), None)
        if collection:
            bourbons = collection.bourbons
            if bourbons:
                for bourbon in bourbons:
                    print(f"ID: {bourbon.id}, Name: {bourbon.name}")
            else:
                print("No bourbons found in this collection.")
        else:
            print("Collection not found.")
    else:
        print("No collections found.")

# def find_collection_by_name():
#     name = input("Enter the name of the collection: ")
#     collections = session.query(Collection).filter_by(name=name).all()
#     if collections:
#         for collection in collections:
#             print(f"ID: {collection.id}, Name: {collection.name}")
#     else:
#         print("Collection not found.")

def create_bourbon():
    name = input("Enter the name of the bourbon: ")
    collections = Collection.get_all()
    if collections:
        print("Select a collection to add the bourbon to:")
        for collection in collections:
            print(f"ID: {collection.id}, Name: {collection.name}")
        collection_id = int(input("Enter the ID of the collection: "))
        collection = next((c for c in collections if c.id == collection_id), None)
        if collection:
            bourbon = Bourbon(name=name, collection=collection)
            bourbon.create()
            print("Bourbon created successfully!")
        else:
            print("Collection not found.")
    else:
        print("No collections found.")
        
def add_bourbon_to_collection():
    bourbons = Bourbon.get_all()
    if bourbons:
        print("Select a bourbon:")
        for bourbon in bourbons:
            print(f"ID: {bourbon.id}, Name: {bourbon.name}")
        bourbon_id = int(input("Enter the ID of the bourbon: "))
        bourbon = next((b for b in bourbons if b.id == bourbon_id), None)
        if bourbon:
            collections = Collection.get_all()
            if collections:
                print("Select a collection:")
                for collection in collections:
                    print(f"ID: {collection.id}, Name: {collection.name}")
                collection_id = int(input("Enter the ID of the collection: "))
                collection = next((c for c in collections if c.id == collection_id), None)
                if collection:
                    collection.bourbons.append(bourbon)
                    session.commit()
                    print("Bourbon added to collection successfully!")
                else:
                    print("Collection not found.")
            else:
                print("No collections found.")
        else:
            print("Bourbon not found.")
    else:
        print("No bourbons found.")



def delete_bourbon():
    bourbons = Bourbon.get_all()
    if bourbons:
        print("Select a bourbon to delete:")
        for bourbon in bourbons:
            print(f"ID: {bourbon.id}, Name: {bourbon.name}")
        bourbon_id = int(input("Enter the ID of the bourbon to delete: "))
        bourbon = next((b for b in bourbons if b.id == bourbon_id), None)
        if bourbon:
            bourbon.delete()
            print("Bourbon deleted successfully!")
        else:
            print("Bourbon not found.")
    else:
        print("No bourbons found.")


def display_all_bourbons():
    bourbons = Bourbon.get_all()
    if bourbons:
        for bourbon in bourbons:
            print(f"ID: {bourbon.id}, Name: {bourbon.name}")
    else:
        print("No bourbons found.")

def find_bourbon_by_name():
    name = input("Enter the name of the bourbon: ")
    bourbons = session.query(Bourbon).filter_by(name=name).all()
    if bourbons:
        for bourbon in bourbons:
            print(f"ID: {bourbon.id}, Name: {bourbon.name}")
    else:
        print("Bourbon not found.")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            create_collection()
        elif choice == '2':
            delete_collection()
        elif choice == '3':
            display_all_collections()
        elif choice == '4':
            view_bourbons_in_collection()
        elif choice == '5':
            create_bourbon()
        elif choice == '6':
            add_bourbon_to_collection()
        elif choice == '7':
            delete_bourbon()
        elif choice == '8':
            display_all_bourbons()
        elif choice == '9':
            find_bourbon_by_name()
        elif choice == "0":
            exit_program()
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()


  
