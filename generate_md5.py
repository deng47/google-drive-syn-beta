import hashlib,os

def generate_md5(file_name):
    """
    根据给定文件名计算文件MD5值
    :param file_name: 文件的路径
    :return: 返回文件MD5校验值
    """

    def read_chunks(fp):
        fp.seek(0)
        chunk = fp.read(8 * 1024)
        while chunk:
            yield chunk
            chunk = fp.read(8 * 1024)
        else:	# 最后要将游标放回文件开头
            fp.seek(0)

    m = hashlib.md5()
    if os.path.exists(file_name):
        with open(file_name, 'rb') as fp:
            for chunk in read_chunks(fp):
                m.update(chunk)
    elif file_name.__class__.name__ in ["StringIO", "cStringIO"] \
            or isinstance(file_name, file):
        for chunk in read_chunks(file_name):
            m.update(chunk)
    else:
        return ""

    return m.hexdigest()


if __name__ == '__main__':
    print (generate_md5('testfile.jpg'))
