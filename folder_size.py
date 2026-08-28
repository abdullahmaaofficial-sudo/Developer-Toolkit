from pathlib import Path

def foramtSize(raw_bytes):
    for unit in ['Bytes','KB','MB','GB','TB']:
        if raw_bytes < 1024.0:
            return f'{raw_bytes:.2f}{unit}'
        raw_bytes /= 1024.0
    return f'{raw_bytes:.2f}PB'

class Folders_size:
    def __init__(self, path):
        self.folder_path = Path(path)
        self.all_folders = self.getFolders()

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

            folder_size_dic.update({folder: foramtSize(total_size)})
        return folder_size_dic



ob = Folders_size('C:\\Users\\Abdul\\Downloads')
for folder , size in ob.getFolderSize().items():
    print(f"\nfolder: {folder} | size: {size}")
