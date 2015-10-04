# -*- coding: utf8 -*-

import os
import hashlib

object_ext = ['JPG', 'PNG' 'GIF', 'JPEG', 'PSD']

def get_file_ext(file_name):
    name_file = file_name[::-1]
    pos = name_file.index(os.path.extsep)
    txe = name_file[:pos]
    ext = txe[::-1]
    return ext

def calc_sha1(file_path):
    with open(file_path, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        file_hash = sha1obj.hexdigest()
        return file_hash

def main():
    current_dir = raw_input()
    file_list = os.listdir(current_dir)
    hash_set = set()
    cmd_file = open('copysha1.cmd', 'w')
    index_file = open('index.txt', 'w')
    for file_name in file_list:
        if not os.path.extsep in file_name:
            continue
        file_path = os.path.join(current_dir, file_name)
        if not os.path.isfile(file_path):
            continue
        file_ext = get_file_ext(file_name)
        if not file_ext.upper() in object_ext:
            continue
        file_hash = calc_sha1(file_path)
        index = '{file_hash}\t{file_name}\n'.format(file_hash = file_hash, file_name = file_name)
        index_file.write(index)
        if not file_hash in hash_set:
            hash_set.add(file_hash)
            target_file_name = os.path.extsep.join((file_hash, file_ext))
            sha1_file_path = os.path.join(current_dir, 'sha1')
            target_file_path = os.path.join(sha1_file_path, target_file_name)
            cmd = 'copy {source_file_path} {target_file_path}\n'.format(
                source_file_path = file_path,
                target_file_path = target_file_path)
            cmd_file.write(cmd)
    index_file.close()
    cmd_file.close()

if __name__ == '__main__':
    main()
    print 'done.'
