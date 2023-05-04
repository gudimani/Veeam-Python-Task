import argparse


def sync(source, replica, interval, log_file):
    print(source, replica, interval, log_file)


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
    replica = args.replica
    interval = args.interval
    log_file = args.log_file

    sync(source, replica, interval, log_file)
