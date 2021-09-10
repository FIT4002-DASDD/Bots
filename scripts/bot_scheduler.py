import subprocess
import shlex
import time
from multiprocessing.pool import ThreadPool
import os
import csv

SLEEP_TIME = 3600
CONCURRENT_BOTS = 2

def call_proc(cmd):
    """ This runs in a separate thread. """
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return (out, err)

def read_bot_csv(bot_file_dir):
    bots = []
    with open(bot_file_dir) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            bots.append({
                "username": row[0],
                "password": row[1]
            })
    return bots


def main():
    # multiprocessing logic based on this answer: https://stackoverflow.com/a/25120960
    pool = ThreadPool(CONCURRENT_BOTS)
    FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    BAZEL_BOT_BIN = f"{FILE_PATH}/../bazel-bin/bot/app"
    BOT_OUTPUT_DIR = f"{FILE_PATH}/../bot_out"
    BOT_CSV_DIR = f"{FILE_PATH}/bot-info.csv"

    bots = read_bot_csv(BOT_CSV_DIR)

    cmd_list = []
    for bot in bots:
        cmd_list.append(f"{BAZEL_BOT_BIN} --bot_username='{bot['username']}' --bot_password='{bot['password']}' --bot_output_directory='{BOT_OUTPUT_DIR}'")

    for i in range(len(cmd_list)):
        print(cmd_list[i])
        pool.apply_async(call_proc, (cmd_list[i],))

    # Close the pool and wait for each running task to complete
    pool.close()
    pool.join()
    print("All bots have finished their cycles")

if (__name__ == "__main__"):
    while True:
        main()
        print(f"Sleeping for {SLEEP_TIME}s")
        time.sleep(SLEEP_TIME)