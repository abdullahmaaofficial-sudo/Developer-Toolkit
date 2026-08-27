from pathlib import Path
import os

class SearchForFile:
    def __init__(self, path):
        self.folder_for_search = Path(path)
        self.exists = self.folder_for_search.exists()
        self.all_files = self.give_all_files()
        self.keyword = None
        self.extension = None
        
    def give_all_files(self):
        return [item for item in self.folder_for_search.rglob('*')]
    
    def find_by_word(self):
        return [item for item in self.all_files if self.keyword and self.keyword in item.name]

    def find_by_extension(self):
        return [file for file in self.folder_for_search.rglob(f"*.{self.extension}")]


print("========== File Search ==========")
print("→ Enter '1' searching by keyword")
print("→ Enter '2' searching by extension\n")

user_path = input("Enter correct folder path for searching: ")
while True:
    try:
        user_choice = int(input("\nEnter your choice, '0' to quit: "))
    except ValueError:
        print("Invalid number, Please enter a valid number")
        continue

    if user_choice not in [0,1,2]: 
        print(f"Invalid number {user_choice}, Please enter a valid number")
        continue

    if user_choice == 0: 
        print("Program Ended ☑️")
        break

    search = SearchForFile(user_path)

    if not user_path or not search.exists:
        print(f"Invalid folder path, ({user_path})") 
        break

    if user_choice == 1:
        keyword = input("Enter a keyword: ")
        search.keyword = keyword
        items = search.find_by_word()

        if not len(items):
            print("No file founded")
            continue

        for x in items:
            print(f"\nPath: {x} | name: {x.name}")
        print(f"\nTotal item(s) in folder: {len(search.all_files)}")
        print(f"Total item(s) in folder having ({keyword}): {len(items)}")

    if user_choice == 2:
        extension = input("Enter extension: ")
        search.extension = extension
        items = search.find_by_extension()

        if not len(items):
            print("No file founded")
            continue

        for x in items:
            print(f"\nPath: {x} | name: {x.name}")
        print(f"\nTotal item(s) in folder: {len(search.all_files)}")
        print(f"Total item(s) in folder having ({extension}): {len(items)}")