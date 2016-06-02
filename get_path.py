import os

def get_path(path):
    asb_paths=[]
    rel_paths = os.listdir(path)
    for rel_path in rel_paths:
        asb_path = path +'/' + rel_path
        asb_paths.append(asb_path)
    return asb_paths
