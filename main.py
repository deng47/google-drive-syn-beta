import os
from get_creds import *
from get_path import *
from create_file import *
from create_folder import *
from path_exist import *
from generate_md5 import *
from upload import *
from sync_record import *
from find_parent_id import *

get_creds()

def mirror(parent_folder, parent_id=False):
    """
    input the path of the directory that on local drive
    input type: string
    
    """
    parent_folder = parent_folder.replace('\\','/')
    
    #取得根目录下单一级的所有文件夹和文件路径的列表
    paths = get_path(parent_folder)
    
    print('\n\n正在处理文件夹：   ', parent_folder,'\n\n')
    
    #查看上级目录的记录文件获，取上级目录ID
    parent_id = find_parent_id(parent_folder)
    
    #如输入了上级目录ID
    if parent_id:
        folder_id = parent_id
    
    #没有输入参数
    else:   
        #没有能够从同步记录文件中获取上级目录ID，生成ID
        folder_id = create_folder(parent_folder)
                           
    #创建上传任务的字典
    sync_record_path = parent_folder + '/sync_record.txt'
    upload_list = {sync_record_path:[folder_id]}
        
    #创建下级目录的文件夹和文件，返回其在Drive的ID，并记录到上传任务的字典中
    for path in paths:
        path = path.replace('\\','/')
        print('checking file:   ',path)
        
        #打开本地sync_record.txt,判断是否存在该文件夹或文件,对比md5确认是否被改动
        file_id = path_exist(path, sync_record_path)
        
        #当对象是一个同步记录文件时，创新除旧
        if file_id and path == sync_record_path:
            print('pass sync_record.txt')
            child_id = create_file(path, folder_id)
            upload_list[path] = [folder_id, child_id]
            file = open(sync_record_path)
            data = file.read()
            record = eval(data)
            sync_record_id = record.get(sync_record_path)[1]  
            file.close()
            DRIVE.files().delete(fileId = sync_record_id).execute()
            continue
        
        elif os.path.isfile(path) and file_id:
            #对比md5
            local_file_md5 = generate_md5(path)
            drive_file_md5 = DRIVE.files().get(fileId=file_id, fields="md5Checksum").execute()['md5Checksum']
            
            if local_file_md5 == drive_file_md5:
                print('file exists, pass')
                #记录ID到上传任务的字典,表示已经存在，无需再上传
                upload_list[path] = [folder_id, file_id]
                continue
            else:         
                #创建并记录ID到上传任务的字典，删除已经被改动的文件
                upload(path, folder_id, upload_list)
                DRIVE.files().delete(fileId = file_id).execute()
                print('REMOVED:   ',os.path.basename(path))
                continue
        elif os.path.isdir(path) and file_id:
            print('folder exists, pass')
            upload_list[path] = [folder_id, file_id]
            continue

        else:
            upload(path, folder_id, upload_list)  
    #用上传任务字典与同步记录文件比较，找出要删除的任务，最后把上传任务的字典写进同步记录文件
    sync_record(upload_list, sync_record_path)
    
    #递归同步下级文件夹
    file = open(sync_record_path)
    record = eval(file.read())
    for each in record:
        if os.path.isdir(each):
            mirror(each)
    
        
        
            
