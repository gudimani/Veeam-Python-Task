import argparse
import os
import time
import shutil
import datetime
import hashlib


def sync(src_path, dest, log_file):
    # TODO catch path does not exist error
    # check source is proper or not ---yet to do

    src_path_2 = src_path
    src_path_len = len(src_path)
    dest_path_len = len(dest)
    if not os.path.exists(dest):
        os.makedirs(dest)
        print(f"Directory '{dest}' created")
        # check for files or folders in source
        shutil.copytree(src_path, dest)

        # for file in os.listdir(source):
        #     source_file_path = os.path.join(source, file)
        #     replica_file_path = os.path.join(replica, file)
        #     # shutil.copy2(os.path.join(source, file), replica) is throwing permission error while copying folders
        #     # TODO-- copy entire directory
        #     if os.path.isdir(source_file_path):
        #         shutil.copytree(source_file_path, replica_file_path)

        #     elif os.path.isfile(source_file_path):
        #         shutil.copy2(source_file_path, replica_file_path)

        #     else:
        #         print(
        #             "copy other than files/folders to replica, edge cases such as .git etc")

    else:
        print(f"Directory '{dest}' already exists")
        src_path_len = len(src_path)
        for root, dirs, files in os.walk(src_path):
            # print(root, dirs, files)

            for file in files:
                src_path = os.path.join(root, file)

                dest_append = root[src_path_len:]

                dest_path = os.path.join(dest+dest_append, file)
                if not os.path.exists(dest_path):
                    shutil.copy2(src_path, dest_path)
                else:
                    with open(src_path, 'rb') as s:
                        contents = s.read()
                        hash_object = hashlib.md5(contents)
                        md5_hash_source = hash_object.hexdigest()
                    with open(dest_path, 'rb') as d:
                        contents = d.read()
                        hash_object = hashlib.md5(contents)
                        md5_hash_dest = hash_object.hexdigest()
                    if md5_hash_source != md5_hash_dest:
                        shutil.copy2(src_path, dest_path)
            for dir in dirs:
                dest_append = root[src_path_len:]
                dest_dir_path = os.path.join(dest+dest_append, dir)
                if not os.path.exists(dest_dir_path):
                    os.makedirs(dest_dir_path)

        # deletefiles at replica but not at source
        for root, dirs, files in os.walk(dest):
            for file in files:
                dest_path = os.path.join(root, file)
                src_path_append = root[len(dest):]
                src = os.path.join(src_path_2+src_path_append, file)
                if not os.path.exists(src):
                    os.remove(dest_path)
            for dir in dirs:
                dest_dir_path = os.path.join(root, dir)
                src_path_append = root[dest_path_len:]
                src_dir_path = os.path.join(src_path_2+src_path_append, dir)
                if not os.path.exists(src_dir_path):
                    shutil.rmtree(dest_dir_path)
        # Compare files in both add if not present at replica, if present check for the modifications at source and update at replica


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Synchronize source and replica at regular intervals')
    parser.add_argument('--source',  type=str, help='Source folder path')
    parser.add_argument('--replica', type=str, help='Replica folder path')
    parser.add_argument('--interval', type=int,
                        default=30, help='Log interval in minutes')
    parser.add_argument('--log_file',  type=str,
                        default='sync.log', help='Log file name')

    args = parser.parse_args()
    source = args.source
    dest = args.replica
    interval = args.interval
    log_file = args.log_file

    while True:

        sync(source, dest, log_file)
        time.sleep(60)
