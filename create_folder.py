import os
from get_creds import *

def create_folder(path, parentId=None):
    folder_name = os.path.split(path)[1]
    if parentId==None:
        folder = {'name' : folder_name, 'mimeType' : 'application/vnd.google-apps.folder'} 
    else:
        folder = {'name' : folder_name, 'mimeType' : 'application/vnd.google-apps.folder', 'parents':[parentId]}    
    folder_id = DRIVE.files().create(body=folder, fields='id').execute()
    print('Create Folder:   ',folder_name)
    return folder_id['id']
