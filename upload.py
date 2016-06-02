import os
from create_file import *
from create_folder import *

def upload(path, folder_id, upload_list):
    
    if os.path.isfile(path):
        child_id = create_file(path, folder_id)
        upload_list[path] = [folder_id, child_id]
                 
    elif os.path.isdir(path):
        child_id = create_folder(path, folder_id)
        upload_list[path] = [folder_id, child_id]
    
