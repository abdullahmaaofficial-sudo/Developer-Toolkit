from pathlib import Path

def foramtSize(raw_bytes):
    for unit in ['Bytes','KB','MB','GB','TB']:
        if raw_bytes < 1024.0:
            return f'{raw_bytes:.2f}{unit}'
        raw_bytes /= 1024.0
    return f'{raw_bytes:.2f}PB'

class Folders_size_finder:
    def __init__(self, path):
        self.folder_path = Path(path)
        self.all_folders = self.getFolders()
        self.exists = self.folder_path.exists()
        self.rootFolderSize = 0

    def getFolders(self):
        return [folder for folder in self.folder_path.rglob('*') if folder.is_dir()]
    
    def getFolderSize(self):
        folder_size_dic = {}

        for folder in self.all_folders:
            total_size = 0
            try:
                for item in folder.rglob('*'):
                    total_size += item.stat().st_size
            except PermissionError:
                print("Access Denied")
            self.rootFolderSize += total_size
            folder_size_dic.update({folder: foramtSize(total_size)})
        return folder_size_dic



print("========== Folder size finder ==========")
print("Find inner folder size and root folder size by just putting path of the folder.\n")

user_fpath = input("Enter a folder path for it's size: ")
finder = Folders_size_finder(user_fpath)

if not user_fpath or not finder.exists:
    print("Invalid folder path, Please enter a valid path")

for folder, size in finder.getFolderSize().items():
    print(f"\nFolder name: {folder.name} | Size: {size}")

print(f"\nRoot Folder: {finder.folder_path.name} | Size: {foramtSize(finder.rootFolderSize)}\n")