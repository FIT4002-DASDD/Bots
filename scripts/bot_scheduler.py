"""
This script is used to schedule and run the bots.
The script utilises multiprocessing to spawn a new process for each bot 
and control the maximum number of bots to run concurrently with ThreadPool.
After all the bots are finished, it'll sleep for SLEEP_TIME seconds before continue again.

Check the constant belows to configure the schedule behaviour and input and output directories
"""
import subprocess
import shlex
import time
from multiprocessing.pool import ThreadPool
import multiprocessing
import os
import csv
from datetime import datetime

# Time in seconds between schedule cycles
# A complete schedule cycle means that *each* bot has completed its own cycle
SLEEP_TIME = 5000

# Number of concurrent bots / worker threads
CONCURRENT_BOTS = multiprocessing.cpu_count()

# Directory of this script file
DIRNAME = os.path.dirname(os.path.realpath(__file__))

# Path to bot binary file 
BOT_BIN_PATH = f"{DIRNAME}/../bazel-bin/bot/app"

# Bot output and logs
BOT_OUTPUT_DIR = f"{DIRNAME}/../bot_out"
LOG_DIR = f"{BOT_OUTPUT_DIR}/logs"

# Path to csv file with bot info
BOT_CSV_PATH = f"{DIRNAME}/bot-info.csv"

def call_proc(cmd, bot):
    """ This runs in a separate thread. """
    current_time = datetime.now()
    year = current_time.strftime("%Y")
    month = current_time.strftime("%B")
    log_dir = f"{LOG_DIR}/{year}/{month}"
    timestamp = int(current_time.timestamp())

    if not os.path.exists(log_dir): 
        os.makedirs(log_dir)

    filename = f"{log_dir}/{bot['username']}_{current_time.strftime('%Y%m%d')}_{timestamp}.log"
    with open(filename, 'a') as f:
        f.write(f"--------------------{current_time.strftime('%d/%m/%Y %H:%M:%S')}--------------------\n")
        with subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            for line in p.stderr:
                f.write(line.decode('utf8'))
                f.flush()   # to write logs in real time
    return

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
    bots = read_bot_csv(BOT_CSV_PATH)

    results = []
    for bot in bots:
        cmd = f"python3 {BOT_BIN_PATH} --bot_username='{bot['username']}' --bot_password='{bot['password']}' --bot_output_directory='{BOT_OUTPUT_DIR}' --debug=False"
        results.append(pool.apply_async(call_proc, (cmd, bot, )))

    # Close the pool and wait for each running task to complete
    pool.close()
    pool.join()
    print("All bots have finished their cycles")

if (__name__ == "__main__"):
    while True:
        main()
        print(f"Sleeping for {SLEEP_TIME}s")
        time.sleep(SLEEP_TIME)