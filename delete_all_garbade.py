import os

def delete_files_containing_zone(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if 'Zone' in filename:
                file_path = os.path.join(dirpath, filename)
                os.remove(file_path)
                print(f'Deleted: {file_path}')

# Replace 'your_directory' with the directory you want to search
delete_files_containing_zone('.')
