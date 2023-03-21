import os
import shutil
import time
import argparse

def sync_folders(source_path, replica_path, log_file_path, interval):
    if not os.path.exists(replica_path):
        os.makedirs(replica_path)

    while True:
        for root, dirs, files in os.walk(source_path):
            for directory in dirs:
                source_dir_path = os.path.join(root, directory)
                replica_dir_path = os.path.join(replica_path, os.path.relpath(source_dir_path, source_path))
                if not os.path.exists(replica_dir_path):
                    os.makedirs(replica_dir_path)
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Created directory: {replica_dir_path}")
                    with open(log_file_path, "a") as f:
                        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Created directory: {replica_dir_path}\n")
            for file in files:
                source_file_path = os.path.join(root, file)
                replica_file_path = os.path.join(replica_path, os.path.relpath(source_file_path, source_path))
                if not os.path.exists(replica_file_path) or (os.path.exists(replica_file_path) and os.stat(source_file_path).st_mtime - os.stat(replica_file_path).st_mtime > 1):
                    shutil.copy2(source_file_path, replica_file_path)
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Copied file: {replica_file_path}")
                    with open(log_file_path, "a") as f:
                        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Copied file: {replica_file_path}\n")

        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source", help="Path to source folder.")
    parser.add_argument("replica", help="Path to replica folder.")
    parser.add_argument("log_file", help="Path to log file.")
    parser.add_argument("-i", "--interval", type=int, default=10, help="Interval between syncs (in seconds).")
    args = parser.parse_args()

    source_path = args.source
    replica_path = args.replica
    log_file_path = args.log_file
    interval = args.interval

    sync_folders(source_path, replica_path, log_file_path, interval)

