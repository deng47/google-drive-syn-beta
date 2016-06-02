from get_creds import *

def sync_record(upload_list, sync_record_path):
    try:
        file = open(sync_record_path)
        data = file.read()
        record = eval(data)
        for each in record:
            if each not in upload_list:
                DRIVE.files().delete(fileId = record[each][1]).execute()
                print('REMOVED:   ',record[each][1])
        file.close()
            
    except:
        file = open(sync_record_path,'w')
        file.write(str(upload_list))
        file.close()
