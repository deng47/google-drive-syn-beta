
def path_exist(path, sync_record_path):
    try:
        file = open(sync_record_path)
        data = file.read()
        record = eval(data)
        if record.get(path, False):
            return record.get(path)[1]
        else:
            return False
            
    except:
        return False
