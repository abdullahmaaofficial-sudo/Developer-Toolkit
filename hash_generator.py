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

class HashGenerator:
    def __init__(self, path : str):
        self.path = path
        self.all_files = self.get_all_files()

    def get_all_files(self):
        return [os.path.join(root,file) for root, subfolder, files in os.walk(self.path) for file in files]

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

class TrackChangedFiles:
    def __init__(self, path):
        self.file_path = path

    def file_in_json(self):
        data = load_json()
        return data.get(self.file_path)
    
    def file_changed(self):
        generator = HashGenerator(path = self.file_path)
        saved_hash = self.file_in_json()
        if saved_hash:
            current_hash = generator.generate_hash()
            return saved_hash == current_hash if current_hash else None
        print("Error: File is not hashed yet")
        return None


ob = HashGenerator(path = "C:\\Users\\abdul\\Downloads")
ob.save_hashed_folder()
print(load_json())
