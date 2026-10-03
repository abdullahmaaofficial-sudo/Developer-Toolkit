import hashlib
import json
import os

FILE_PATH = 'data/hashes.json'

def write_json(data):
    with open(FILE_PATH, 'w') as file:
        json.dump(data,file,indent = 2) 

def load_json():
    try:
        with open(FILE_PATH, 'r') as file:
            return json.load(file)
    except Exception as e:
        print("JSON Error: ",e)
        return {}

def get_all_files(path):
    return [os.path.join(root,file) for root, subfolder, files in os.walk(path) for file in files]

def show_files(files, header, symbol):
    print(f'\n{header}')
    if not files: print(f"{symbol} No file!")
    for file in files:
        print(f"{symbol} {file}")
    print()

class HashGenerator:
    def __init__(self, path : str, is_folder = False):
        self.all_files = get_all_files(path = path) if is_folder else None
        self.path = path

    def generate_hash(self, file_path = None):
        file_path = file_path or self.path
        try:
            with open(file_path , 'rb') as file:
                hash_ob = hashlib.sha256()
                while chunk := file.read(1024 * 1024):
                    hash_ob.update(chunk)
            return hash_ob.hexdigest()
        except Exception as e:
            print("Hash Error: ", e)
                                                           
    def save_hashed_folder(self):
        data = load_json()
        for file in self.all_files:
            file_hash = self.generate_hash(file_path = file)
            if file_hash: data.update({file : file_hash})
        write_json(data = data)

    def save_hashed_file(self):
        data = load_json()
        file_hash = self.generate_hash(file_path = self.path)
        data.update({self.path: file_hash})
        write_json(data = data)

class FileIntegrityChecker:
    def __init__(self, path):
        self.file_path = path

    def file_in_json(self):
        data = load_json()
        return data.get(self.file_path)

    def folder_in_json(self):
        data = load_json()
        return [file for file in data if os.path.commonpath([self.file_path, file]) == self.file_path]
    
    def check_file(self, file_path = None):
        file_path = file_path or self.file_path
        generator = HashGenerator(path = file_path)
        saved_hash = self.file_in_json()
        if saved_hash:
            current_hash = generator.generate_hash()
            return saved_hash == current_hash if current_hash else None
        return None

    def check_folder(self):
        all_files = get_all_files(path = self.file_path)
        saved_files = self.folder_in_json()
        new_files = [file for file in all_files if not file in saved_files]
        deleted_files = [file for file in saved_files if not file in all_files]
        changed_files = [file for file in saved_files if self.check_file(file_path = file) is False]


        while True:
            print(f"Total Files: {len(all_files)}")
            print(f"* Changed files: {len(changed_files)}")
            print(f"+ New files: {len(new_files)}")
            print(f"- Deleted files: {len(deleted_files)}\n")

            choice = input("Enter the symbol to see the files (q to quit): ")
            if choice.lower() == 'q': break
            if not choice in ['*','+','-']: print("Choice Error: Invalid choice!")

            if choice == '*': show_files(files = changed_files, header = "Changed Files: ", symbol = choice)
            elif choice == '+': show_files(files = new_files, header = "New Files: ", symbol = choice)
            elif choice == '-': show_files(files = deleted_files, header = "Deleted Files: ", symbol = choice)


while True:
    print('\n','=' * 8,"FileIntegrityChecker", '=' * 8)
    print("Note: To track files, hashed them first\n")
    print("1- Hashed folder")
    print("2- Hashed file")
    print("3- Check folder")
    print("4- Check file\n")

    try:
        choice = int(input("Enter choice (0 to quit): "))
    except:
        print("Input Error: Not a number!")
        continue

    if choice == 0: break

    if choice not in range(5):
        print("Choice Error: Invalid choice!")

    path = input("Enter an absolute path: ")
    if not os.path.exists(path):
        print("Path Error: Path does not exists!")
        continue

    is_folder = os.path.isdir(path)
    is_file = os.path.isfile(path)
    generator = HashGenerator(path = path, is_folder = is_folder)
    tracker = FileIntegrityChecker(path = path)

    if choice == 1:
        if not is_folder:
            print("Path Error: path is not a folder!")
        else: generator.save_hashed_folder()

    elif choice == 2:
        if not is_file:
            print("Path Error: path is not a file!")
        else: generator.save_hashed_file()
    
    elif choice == 3:
        if not is_folder:
            print("Path Error: path is not a folder!")
        else: tracker.check_folder()

    elif choice == 4:
        if not is_file:
            print("Path Error: path is not a file!")
        else: tracker.check_file()