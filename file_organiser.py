from pathlib import Path
import shutil
import os 

FILE_TYPES = {
    'Images': [
        '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp', '.svg', '.tiff', '.tif', 
        '.heic', '.heif', '.ico', '.psd', '.ai', '.eps', '.raw', '.cr2', '.nef', 
        '.orf', '.sr2', '.dng', '.ind', '.indd', '.jp2'
    ],
    'Videos': [
        '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', 
        '.mpeg', '.m2v', '.3gp', '.3g2', '.ogv', '.vob', '.mts', '.m2ts', '.ts', 
        '.asf', '.rm', '.rmvb', '.divx'
    ],
    'Audio': [
        '.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma', '.opus', '.aiff', 
        '.aif', '.mid', '.midi', '.alac', '.amr', '.ape', '.pcm'
    ],
    'Documents': [
        '.pdf', '.doc', '.docx', '.odt', '.rtf', '.tex', '.txt', '.wpd', '.wps', 
        '.pages', '.epub', '.mobi', '.azw', '.azw3'
    ],
    'Spreadsheets': [
        '.xls', '.xlsx', '.xlsm', '.xlsb', '.ods', '.csv', '.tsv', '.numbers'
    ],
    'Presentations': [
        '.ppt', '.pptx', '.pptm', '.odp', '.key', '.pps', '.ppsx'
    ],
    'Compressed': [
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.iso', '.xz', '.tgz', 
        '.tbz2', '.cab', '.dmg', '.z', '.lz', '.lzma'
    ],
    'Code': [
        '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.scss', '.sass', 
        '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.php', '.rb', '.go', '.rs', 
        '.swift', '.kt', '.kts', '.sh', '.bash', '.zsh', '.ps1', '.bat', '.sql', 
        '.json', '.xml', '.yaml', '.yml', '.toml', '.ini', '.env', '.md', '.lua', 
        '.r', '.dart', '.m', '.scala', '.vue', '.svelte'
    ],
    'Executables': [
        '.exe', '.msi', '.apk', '.app', '.bin', '.cmd', '.gadget', '.jar', '.wsf'
    ],
    'Fonts': [
        '.ttf', '.otf', '.woff', '.woff2', '.eot', '.fon'
    ],
    'Database': [
        '.db', '.sqlite', '.sqlite3', '.mdb', '.accdb', '.sql', '.pdb'
    ],
    '3d_models': [
        '.obj', '.stl', '.fbx', '.dae', '.blend', '.3ds', '.ply', '.gltf', '.glb'
    ],
    'System_files': [
        '.sys', '.dll', '.cur', '.ico', '.lnk', '.dmp', '.tmp', '.bak'
    ],
    'Disk_images': [
        '.iso', '.img', '.vcd', '.toast', '.vmdk'
    ]
}

def get_file_type(file):
    file_ext = os.path.splitext(file)[1].lower()
    for file_type, extensions in FILE_TYPES.items():
        if file_ext in extensions:
            return file_type
    return 'Other'
    
class Base:
    def __init__(self, path):
        self.folder_path = path
        self.specific_folder = None
        self.specific_files = []
        self.exists = os.path.exists(self.folder_path)

    def take_all_files(self):
        if self.exists:
            return [os.path.join(root,file) for root, subfolder, files in os.walk(self.folder_path) for file in files]

    def take_custom_files(self):
        if self.exists:
            return [os.path.join(root,file) for root,sub_f,files in os.walk(self.folder_path) for file in files 
                    if not os.path.join(root,file) in self.specific_files]

    def handle_user_choice(self):
        temp_file_dict = {}
        choice = input("Select the number of the option you want, press enter to skip options: ")
        if not choice in ['1','2']: return 
        
        if choice == '1':
            folder = input("Enter folder name: ")
            
        for file_no , file in enumerate(self.take_all_files()):
            print(f"{file_no + 1}: {file}\n")
            temp_file_dict.update({file_no + 1: file})

        while True:
            try:
                if choice == '1':
                    file_num = int(input(f"Enter a file number for moving it to specific folder ({folder}), enter 0 to quit: "))
                elif choice == '2':
                    file_num = int(input(f"Enter a file number you don't wanna change it's location, enter 0 to quit: "))
            except:
                print("Please enter a number")

            if file_num > len(temp_file_dict): 
                print(f"Invalid number {file_num}, please enter a valid number")
                continue

            if file_num == 0:
                if self.specific_files: 
                    if choice == '1': self.specific_folder = folder
                    print(f"\nFiles Selected: \n{self.specific_files}\n")
                else: print('No file selected')
                return 

            self.specific_files.append(temp_file_dict.get(file_num, ''))

class Organiser(Base):
    def __init__(self, path):
        super().__init__(path)
        
    def make_folders(self):
        files = self.take_custom_files() if self.specific_files and not self.specific_folder else self.take_all_files()
        folders = {}
        for file in files:
            if self.specific_folder and file in self.specific_files:
                file_type = self.specific_folder
            else: file_type = get_file_type(file)

            folder = os.path.join(self.folder_path, file_type)
            os.makedirs(folder, exist_ok=True)
            folders.update({file: folder})
        return folders

    def organise_files(self):
        if not self.exists: return f'Folder dose not exists: {self.folder_path}'
        for file, file_folder in self.make_folders().items():
            filename = os.path.basename(file) 
            new_path = os.path.join(file_folder, filename)
            try:
                shutil.move(file, new_path)
                print("New Path: ", new_path)
            except Exception as e:
                print("Something went wrong, try again: ", e)
        return "\nFolder organised successfully"

    def delete_empty_folders(self):
        base_folder = Path(self.folder_path)
        empty_folders = [item for item in base_folder.rglob('*') if item.is_dir() and not any(item.iterdir())]
        if not empty_folders: return

        print("\n----- Empty Folders -----")
        for folder in empty_folders:
            print(f"→ {folder}")
        print()

        choice = input("Enter '1' to delete all empty folders (press enter to skip): ").strip()
        if choice == '1':
            for folder in empty_folders:
                try:
                    shutil.rmtree(folder)
                except FileNotFoundError:
                    print(f"Error: Folder doesn't exist, ({folder}) ")
                except PermissionError:
                    print(f"Error: Access denied, ({folder})")

            return "~ Operation performed."
        return "~ Operation skipped."

print("============ FILE ORGANISER =============")
print("→ Enter '1' for creating a custom folder")
print("→ Enter '2' for not changing specific files location\n")

user_folder = input("Enter an absolute folder path for organising: ")
ob = Organiser(user_folder)

if ob.exists:
    ob.handle_user_choice()
    while True:
        confirm_user = input("Press enter to organise and '0' to stop: ")
        if confirm_user in ['0','']:
            break
    if confirm_user == '':
        print(ob.organise_files())
        result = ob.delete_empty_folders()
        print(result if result else "")
    else: print("\nThe operation is stoped.")
else: print("Path doesn't exists, try to upload full path.")