import argparse
import os
import time
import shutil
import datetime
import hashlib
import logging
import logging.handlers


def sync(src_path, dest):

    src_path_original = src_path
    src_path_len = len(src_path)
    dest_path_len = len(dest)
    # if dest path do not eixst
    if not os.path.exists(dest):
        # create and copy all files from source.
        shutil.copytree(src_path_original, dest)
        logging.info('Replica %s folder created', dest)

    # if dest path already exists
    else:
        src_path_len = len(src_path)

        for root, dirs, files in os.walk(src_path):
            # copy/update files in replica if not exists
            for file in files:
                src_path = os.path.join(root, file)
                dest_append = root[src_path_len:]
                dest_path = os.path.join(dest + dest_append, file)

                if not os.path.exists(dest_path):
                    shutil.copy2(src_path, dest_path)
                    logging.info(
                        'File %s copied from source to replica', file)
                else:
                    with open(src_path, 'rb') as s:
                        content = s.read()
                        hash_object = hashlib.md5(content)
                        md5_hash_source = hash_object.hexdigest()
                    with open(dest_path, 'rb') as d:
                        content = d.read()
                        hash_object = hashlib.md5(content)
                        md5_hash_dest = hash_object.hexdigest()
                    if md5_hash_source != md5_hash_dest:
                        shutil.copy2(src_path, dest_path)
                        logging.info(
                            'Modified file %s in source updated in replica', file)
            # create directories in replica which does not exist
            for dir in dirs:
                dest_append = root[src_path_len:]
                dest_dir_path = os.path.join(dest+dest_append, dir)
                if not os.path.exists(dest_dir_path):
                    os.makedirs(dest_dir_path)
                    logging.info(
                        'Missing directory %s created in replica', dir)

        # delete files present at replica but not at source
        for root, dirs, files in os.walk(dest):
            for file in files:
                dest_path = os.path.join(root, file)
                src_path_append = root[len(dest):]
                src = os.path.join(src_path_original+src_path_append, file)
                if not os.path.exists(src):
                    os.remove(dest_path)
                    logging.info(
                        'File %s removed from replica', file)
            for dir in dirs:
                dest_dir_path = os.path.join(root, dir)
                src_path_append = root[dest_path_len:]
                src_dir_path = os.path.join(
                    src_path_original + src_path_append, dir)
                if not os.path.exists(src_dir_path):
                    shutil.rmtree(dest_dir_path)
                    logging.info(
                        'Directory %s removed from replica', dir)


def main(source, dest, interval, log_file):
    try:
        if not os.path.exists(source):
            raise FileNotFoundError(
                'Source path does not exist. Please enter valid source path.')

        app_log = logging.getLogger()
        app_log.setLevel(logging.INFO)

        file_handler = logging.handlers.RotatingFileHandler(
            log_file, mode='a', maxBytes=128)

        log_formatter = logging.Formatter(
            '%(levelname)s:%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

        file_handler.setFormatter(log_formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)

        app_log.addHandler(file_handler)
        app_log.addHandler(console_handler)

        while True:

            sync(source, dest)
            time.sleep(interval*60)

    except FileNotFoundError as error:
        print(error)
    except ValueError as error:
        if str(error) == 'sleep length must be non-negative':
            print('Please provide positive interval value')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Synchronize source and replica at regular intervals')
    parser.add_argument('--source',  type=str, help='Source folder path')
    parser.add_argument('--replica', type=str, help='Replica folder path')
    parser.add_argument('--interval', type=float,
                        default=1, help='Log interval in minutes')
    parser.add_argument('--log_file',  type=str,
                        default='sync.log', help='Log file name')

    args = parser.parse_args()
    source = args.source
    dest = args.replica
    interval = args.interval
    log_file = args.log_file

    main(source, dest, interval, log_file)
