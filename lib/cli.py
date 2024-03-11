# lib/cli.py

from helpers import (exit_program)
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from termcolor import cprint, colored


engine = create_engine('sqlite:///bourbon_collection.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

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


Base.metadata.create_all(engine)


def display_menu():
    cprint("\nPlease choose an option:", 'white', attrs=['bold'])
    print(colored("1. Create Collection", 'blue'))
    print(colored("2. Delete Collection", 'white'))
    print(colored("3. Display All Collections", 'blue'))
    print(colored("4. View Bourbons in Collection", 'white'))
    print(colored("5. Create Bourbon", 'blue'))
    print(colored("6. Add Bourbon to a Collection", 'white'))
    print(colored("7. Delete Bourbon", 'blue'))
    print(colored("8. Display All Bourbons", 'white'))
    print(colored("9. Remove Bourbon from Collection", 'blue'))
    print(colored("0. Exit", 'white'))


def create_collection():
    cprint("\n--- Create a New Collection ---", 'blue', attrs=['bold'])
    name = input("\nWhat's the name of your new collection? ")
    collection = Collection(name=name)
    collection.create()
    cprint("\nCollection created successfully!", 'green')


def delete_collection():
    collections = Collection.get_all()
    if collections:
        print("\nSelect a collection to delete:")
        for collection in collections:
            print(f"\nID: {collection.id}, Name: {collection.name}")
        collection_id = int(input("\nEnter the ID of the collection to delete: "))
        collection = next((c for c in collections if c.id == collection_id), None)
        if collection:
            collection.delete()
            cprint("\nCollection deleted successfully!", 'green')
        else:
            cprint("\nCollection not found.", 'red')
    else:
        cprint("\nNo Collections found.", 'red')

def display_all_collections():
    collections = Collection.get_all()
    if collections:
        cprint("\n--- All Collections ---", 'blue', attrs=['bold'])
        for collection in collections:
            print(f"\nID: {collection.id}, Name: {collection.name}")
    else:
        cprint("\nNo Collections found.", 'red')


def view_bourbons_in_collection():
    collections = Collection.get_all()
    if collections:
        cprint("\n--- Select a Collection ---", 'blue', attrs=['bold'])
        for collection in collections:
            print(f"\nID: {collection.id}, Name: {collection.name}")
        collection_id = int(input("\nEnter the ID of the collection: "))
        collection = next((c for c in collections if c.id == collection_id), None)
        if collection:
            bourbons = collection.bourbons
            if bourbons:
                for bourbon in bourbons:
                    print(f"\nID: {bourbon.id}, Name: {bourbon.name}")
            else:
                cprint("\nNo Bourbons found in this collection.", 'red')
        else:
            cprint("\nCollection not found.", 'red')
    else:
        cprint("\nNo Collections found.", 'red')

def create_bourbon():
    name = input("\nEnter the name of the bourbon: ")
    if isinstance(name, str):
        collections = Collection.get_all()
        if collections:
            print("\nSelect a collection to add the bourbon to:")
            for collection in collections:
                print(f"\nID: {collection.id}, Name: {collection.name}")
            collection_id = int(input("\nEnter the ID of the collection: "))
            collection = next((c for c in collections if c.id == collection_id), None)
            if collection:
                bourbon = Bourbon(name=name, collection=collection)
                bourbon.create()
                cprint("\nBourbon created successfully!", 'green')
            else:
                cprint("\nCollection not found.", 'red')


def add_bourbon_to_collection():
    bourbons = Bourbon.get_all()
    if bourbons:
        cprint("\n--- Select a Bourbon ---", 'blue', attrs=['bold'])
        for bourbon in bourbons:
            print(f"\nID: {bourbon.id}, Name: {bourbon.name}")
        bourbon_id = int(input("\nEnter the ID of the bourbon: "))
        bourbon = next((b for b in bourbons if b.id == bourbon_id), None)
        if bourbon:
            collections = Collection.get_all()
            if collections:
                print("\nSelect a collection:")
                for collection in collections:
                    print(f"\nID: {collection.id}, Name: {collection.name}")
                collection_id = int(input("\nEnter the ID of the collection: "))
                collection = next((c for c in collections if c.id == collection_id), None)
                if collection:
                    collection.bourbons.append(bourbon)
                    session.commit()
                    cprint("\nBourbon added to collection successfully!", 'green')
                else:
                    cprint("\nCollection not found.", 'red')
            else:
                cprint("\nNo Collections found.", 'red')
        else:
            cprint("\nBourbon not found.", 'red')
    else:
        cprint("\nNo Bourbons found.", 'red')

def delete_bourbon():
    bourbons = Bourbon.get_all()
    if bourbons:
        cprint("\n--- Select a Bourbon to Delete ---", 'blue', attrs=['bold'])
        for bourbon in bourbons:
            print(f"\nID: {bourbon.id}, Name: {bourbon.name}")
        bourbon_id = int(input("\nEnter the ID of the bourbon to delete: "))
        bourbon = next((b for b in bourbons if b.id == bourbon_id), None)
        if bourbon:
            bourbon.delete()
            cprint("\nCollection deleted successfully!", 'green')
        else:
            cprint("\nBourbon not found.", 'red')
    else:
        cprint("\nNo Bourbons found.", 'red')

def display_all_bourbons():
    bourbons = Bourbon.get_all()
    if bourbons:
        for bourbon in bourbons:
            print(f"\nID: {bourbon.id}, Name: {bourbon.name}")
    else:
        cprint("\nNo Bourbons found.", 'red')
        
def remove_bourbon_from_collection():
    collections = Collection.get_all()
    if collections:
        cprint("\n ---Select a Collection---", 'blue', attrs=['bold'])
        for collection in collections:
            print(f"\nID: {collection.id}, Name: {collection.name}")
        collection_id = int(input("\nEnter the ID of the collection: "))
        collection = next((c for c in collections if c.id == collection_id), None)
        if collection:
            bourbons = collection.bourbons
            if bourbons:
                cprint("\n--- Select a Bourbon ---", 'blue', attrs=['bold'])
                for bourbon in bourbons:
                    print(f"\nID: {bourbon.id}, Name: {bourbon.name}")
                bourbon_id = int(input("\nEnter the ID of the bourbon to remove: "))
                bourbon = next((b for b in bourbons if b.id == bourbon_id), None)
                if bourbon:
                    collection.bourbons.remove(bourbon)
                    session.commit()
                    cprint("\Bourbon removed from collection successfully!", 'green')
                else:
                    cprint("\nBourbon not found.", 'red')
            else:
                cprint("\nNo Bourbons found in this Collection.", 'red')
        else:
            cprint("\nCollection not found.", 'red')
    else:
        cprint("\nNo Collections found.", 'red')



def main():
    print("""
          
                                                              
        ████████                                    
        ████████                                    
        ████████                                    
        ████████                                  
        ████████                                    
        ████████                                    
        ████████                                    
        ▒▒▒▒▒▒▓▓                                    
        ▒▒▒▒▒▒▒▒                                    
       ▒▒▒▒▒▒▒▒░░                              
       ▒▒▒▒▒▒▒▒▒▒                                    
     ▒▒▒▒▒▒▒▒▒▒▒▒▒▒                                  
  ░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                                
  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                              
  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░                            
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
████████████████████░░░░                        ░░░░
████████████████████░░░░                        ░░░░
████████████████████░░░░                        ░░░░
████████████████████░░░░                        ░░░░
██████████████████████░░░░  ░░░░░░░░  ░░░░      ░░░░
██████████████████████░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░
██████████████████████░░░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░  
██████████████████████░░░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░  
██████████████████████░░░░▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▒▒▒▒░░  
██████████████████████░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░  
██████████████████████░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░  
██████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░  
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░  
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░  
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░    


""")
    while True:
        display_menu()
        choice = input("\nEnter your choice: ")
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
            remove_bourbon_from_collection()
        elif choice == "0":
            print("""
                                      ██▓▓▓▓░░                                      
                                      ██▓▓▓▓░░                                      
                                      ██▓▓▓▓░░                                      
                                      ██▓▓▓▓░░                                      
                                      ██▓▓▓▓░░                                      
                                      ██▓▓▓▓░░                                      
                                      ██▓▓▓▓░░                                      
                                      ▓▓░░░░▒▒                                      
                                      ▓▓░░░░▒▒                                      
                                      ▒▒░░░░▒▒                                      
                                    ▓▓▒▒▒▒▒▒▒▒▒▒                                    
                                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒                                
                                ▒▒▒▒░░░░░░░░░░░░░░░░                                
                                ▒▒▒▒░░░░░░░░░░░░░░░░                                
                                ██▓▓▒▒▓▓▓▓▓▓▓▓▒▒▓▓░░                                
                                ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░                                
                                ██▓▓▓▓        ▓▓▓▓░░                                
                                ██▓▓  ▓▓▓▓▓▓▓▓  ▓▓░░                                
                                ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░                                
                                ██▓▓▓▓        ▓▓▓▓░░                                
                                ██▓▓▓▓        ▓▓▓▓░░                                
                                ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░                                
                                ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░                                
                                ██▓▓            ▓▓░░                                
                                ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░                                
                                ██▓▓            ▓▓░░                                
                                ██▓▓██▓▓▓▓▓▓▓▓▓▓▓▓░░                                
                                ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░                                
                                ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░                                
                                ▒▒░░░░░░░░░░░░░░░░░░                                
                                ▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░                                
                  """)
            exit_program()
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == '__main__':
    main()
