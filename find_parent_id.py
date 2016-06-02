import os.path

def find_parent_id(parent_folder):
    try:
        record_file = os.path.dirname(parent_folder) + '/sync_record.txt'
        file = open(record_file)
        data = file.read()
        record = eval(data)
        parent_id = record.get(parent_folder)[1]
        return parent_id
    except:

        return False
