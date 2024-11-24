from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def create_collection_data(db):
    """Create cats collection documents
    
    db: Database instance from MongoClient
    """
    db.cats.insert_many(
        [
            {
                "name": "barsik",
                "age": 3,
                "features": ["ходить в капці", "дає себе гладити", "рудий"]
            },
            {
                "name": "Lama",
                "age": 2,
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
            {
                "name": "Liza",
                "age": 4,
                "features": ["ходить в лоток", "дає себе гладити", "білий"],
            },
            {
                "name": "barsik",
                "age": 3,
                "features": ["ходить в капці", "дає себе гладити", "рудий"],
            }
        ]
    )

def get_all_cats(db):
    """Prints all decuments from collection
    
    db: Database instance from MongoClient

    Prints cats collection
    """
    result = list(db.cats.find({}))
    if result:
        for cat in result:
            print(cat)
    else:
        print("No records found in the collection.")

def get_cat_by_name(db, name):
    """Prints cat by name
    
    db: Database instance from MongoClient
    name: String

    Prints found cat
    """
    result = db.cats.find_one({"name": name})
    if result:
        print(result)
    else:
        print(f"No cat found with the name '{name}'.")

def update_cat_age_by_name(db, name, new_age):
    """Update cat's age by name
    
    db: Database instance from MongoClient
    name: String
    new_age: String
    """
    result = db.cats.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.matched_count:
        print(f"Updated age of '{name}' to {new_age}.")
    else:
        print(f"No cat found with the name '{name}'.")

def add_feature_to_cat(db, name, feature):
    """Adds feature for cat by name
    
    db: Database instance from MongoClient
    name: String
    feature: String
    """
    result = db.cats.update_one({"name": name}, {"$addToSet": {"features": feature}})
    if result.matched_count:
        print(f"Added feature '{feature}' to '{name}'.")
    else:
        print(f"No cat found with the name '{name}'.")

def delete_cat_by_name(db, name):
    """Deletes cat by name
    
    db: Database instance from MongoClient
    name: String
    """
    result = db.cats.delete_one({"name": name})
    if result.deleted_count:
        print(f"Deleted cat with the name '{name}'.")
    else:
        print(f"No cat found with the name '{name}'.")

def delete_all_cats(db):
    """Deletes all cats
    
    db: Database instance from MongoClient
    """
    result = db.cats.delete_many({})
    print(f"Deleted {result.deleted_count} cats from the collection.")

if __name__ == '__main__':
    uri = "mongodb+srv://<user>:<password>@cluster0.irobh.mongodb.net/<db_name>?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.cats_db
    create_collection_data(db)
    actions = {
        1: lambda: get_all_cats(db),
        2: lambda: get_cat_by_name(db, input("Enter the name of the cat: ").strip()),
        3: lambda: update_cat_age_by_name(db, input("Enter the name of the cat: ").strip(), input("Enter the age of the cat: ").strip()),
        4: lambda: add_feature_to_cat(db, input("Enter the name of the cat: ").strip(), input("Enter the new feature: ").strip()),
        5: lambda: delete_cat_by_name(db, input("Enter the name of the cat: ").strip()),
        6: lambda: delete_all_cats(db),
        7: lambda: print("Exiting the program. Goodbye!")
    }

    while True:
        print("\nChoose an option:")
        print("1. View all cats")
        print("2. Find a cat by name")
        print("3. Update a cat's age")
        print("4. Add a feature to a cat")
        print("5. Delete a cat by name")
        print("6. Delete all cats")
        print("7. Exit")

        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 7.")
            continue

        action = actions.get(choice, lambda: print("Invalid choice. Please enter a number between 1 and 7."))

        try:
            action()

            if choice == 7:
                break
        except Exception as error:
            print(error)
            continue
