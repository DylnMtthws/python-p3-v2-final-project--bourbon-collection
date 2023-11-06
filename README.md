# Project Overview

This project is a command-line interface (CLI) application for managing a bourbon collection. It allows users to create collections, add bourbons to collections, delete collections and bourbons, and view all collections and bourbons.

# Instructions for Running the Project

To run the project, follow these steps:

1. Make sure you have Python installed on your machine.

2. Open a terminal or command prompt.

3. Navigate to the directory where the project files are located.

4. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```

5. Run the CLI application by executing the following command:
   ```
   python lib/cli.py
   ```

6. The CLI menu will be displayed. Follow the prompts to interact with the application.

# Instructions for Using the Project

Once the CLI application is running, you can use the following commands to interact with the project:

1. Create Collection: This command allows you to create a new collection. You will be prompted to enter the name of the collection.

2. Delete Collection: This command allows you to delete an existing collection. You will be prompted to select a collection from a list and enter the ID of the collection to delete.

3. Display All Collections: This command displays a list of all collections.

4. View Bourbons in Collection: This command allows you to view all bourbons in a specific collection. You will be prompted to select a collection from a list and enter the ID of the collection.

5. Create Bourbon: This command allows you to create a new bourbon. You will be prompted to enter the name of the bourbon and select a collection to add it to.

6. Add Bourbon to a Collection: This command allows you to add an existing bourbon to a collection. You will be prompted to select a bourbon from a list and enter the ID of the bourbon, and then select a collection from a list and enter the ID of the collection.

7. Delete Bourbon: This command allows you to delete an existing bourbon. You will be prompted to select a bourbon from a list and enter the ID of the bourbon to delete.

8. Display All Bourbons: This command displays a list of all bourbons.

9. Find Bourbon by Name: This command allows you to search for a bourbon by its name. You will be prompted to enter the name of the bourbon.

0. Exit: This command exits the CLI application.

Please note that the project uses a SQLite database to store the collections and bourbons. The database file is named "bourbon_collection.db" and will be created automatically when you run the project for the first time.