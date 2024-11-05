import sqlite3
from training360_example_lib.search_in_list import search_in_list


# Database initialization
conn = sqlite3.connect('configurations.db')
cursor = conn.cursor()

# Create a configurations table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS configurations (
        id INTEGER PRIMARY KEY,
        application_name TEXT,
        key TEXT,
        value TEXT
    )
''')
conn.commit()

def list_applications():
    """List all available applications."""
    cursor.execute('''
        SELECT DISTINCT application_name FROM configurations
    ''')
    rows = cursor.fetchall()
    if rows:
        print("\nAvailable Applications:")
        for idx, row in enumerate(rows, start=1):
            print(f"{idx}. {row[0]}")
    else:
        print("No applications found.")

def select_application():
    """Prompt the user to select an application."""
    while True:
        list_applications()
        print("0. Add new application")
        choice = input("Enter the number of the application to select (q to quit, d to delete): ")
        
        if choice == '0':
            new_app_name = input("Enter the name of the new application: ")
            if new_app_name:
                cursor.execute('''
                    INSERT INTO configurations (application_name, key, value)
                    VALUES (?, ?, ?)
                ''', (new_app_name, '', ''))
                conn.commit()
                print(f"Application '{new_app_name}' added successfully.")
            else:
                print("Invalid application name.")
        elif choice == 'd':
            app_to_delete = input("Enter the name of the application to delete: ")
            cursor.execute('''
                DELETE FROM configurations
                WHERE application_name = ?
            ''', (app_to_delete,))
            conn.commit()
            print(f"Application '{app_to_delete}' deleted successfully.")
        elif choice == 'q':
            return None  # User chose to quit
        try:
            choice_idx = int(choice)
            cursor.execute('''
                SELECT DISTINCT application_name FROM configurations
            ''')
            rows = cursor.fetchall()
            if 1 <= choice_idx <= len(rows):
                return rows[choice_idx - 1][0]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def list_configs(application_name):
    """List all configurations for the selected application."""
    cursor.execute('''
        SELECT key, value FROM configurations
        WHERE application_name = ?
    ''', (application_name,))
    rows = cursor.fetchall()
    if rows:
        print(f"\nConfigurations for {application_name}:")
        for row in rows:
            print(f"{row[0]}: {row[1]}")
    else:
        print(f"No configurations found for {application_name}.")

def search_config(application_name, key):
    """Search for a configuration by a fuzzy key match."""
    cursor.execute('''
        SELECT key, value FROM configurations
        WHERE application_name = ?
    ''', (application_name,))
    rows = cursor.fetchall()

    if rows:
        best_match = search_in_list(key, rows)
        if best_match:
            print(f"Match found: {best_match[0]}")
        else:
            print("No matching configuration found.")
    else:
        print(f"No configurations found for {application_name}.")

def add_config(application_name, key, value):
    """Add a new configuration key, value pair."""
    cursor.execute('''
        INSERT INTO configurations (application_name, key, value)
        VALUES (?, ?, ?)
    ''', (application_name, key, value))
    conn.commit()
    print("Configuration added successfully.")

def delete_config(application_name, key):
    """Delete a configuration by key."""
    cursor.execute('''
        DELETE FROM configurations
        WHERE application_name = ? AND key = ?
    ''', (application_name, key))
    conn.commit()
    print("Configuration deleted successfully.")

def main():
    print("Welcome to the Configuration Manager!")
    
    while True:
        application_name = select_application()
        if application_name is None:
            print("Goodbye!")
            break

        while True:
            print(f"\nSelected Application: {application_name}")
            print("\nSelect an option:")
            print("1. List configurations")
            print("2. Search for a configuration")
            print("3. Add a new configuration")
            print("4. Delete a configuration")
            print("5. Select another application")
            print("6. Quit")
            
            choice = input("Enter your choice (1/2/3/4/5/6): ")
            
            if choice == '1':
                list_configs(application_name)
            elif choice == '2':
                key = input("Enter the key to search for: ")
                search_config(application_name, key)
            elif choice == '3':
                key = input("Enter the configuration key: ")
                value = input("Enter the configuration value: ")
                add_config(application_name, key, value)
            elif choice == '4':
                key = input("Enter the configuration key to delete: ")
                delete_config(application_name, key)
            elif choice == '5':
                break  # Go back to application selection
            elif choice == '6':
                print("Goodbye!")
                exit()
            else:
                print("Invalid choice. Please select a valid option.")

if __name__ == '__main__':
    main()
