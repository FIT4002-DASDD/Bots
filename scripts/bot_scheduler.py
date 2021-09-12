import subprocess
import shlex
import time
from datetime import datetime
from multiprocessing.pool import ThreadPool
import multiprocessing
import os
import csv

# Time in seconds between schedule cycles
# A complete schedule cycle means that *each* bot has completed its own cycle
SLEEP_TIME = 60

# Number of concurrent bots / worker threads
CONCURRENT_BOTS = multiprocessing.cpu_count()

# Directory of this script file
DIRNAME = os.path.dirname(os.path.realpath(__file__))

# Path to bot binary file 
BOT_BIN_PATH = f"{DIRNAME}/../bazel-bin/bot/app"

# Bot output and logs
BOT_OUTPUT_DIR = f"{DIRNAME}/../bot_out"

# Path to csv file with bot info
BOT_CSV_PATH = f"{DIRNAME}/bot-info.csv"

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
    bots = read_bot_csv(BOT_CSV_PATH)

    cmd_list = []
    for bot in bots:
        cmd_list.append(f"{BOT_BIN_PATH} --bot_username='{bot['username']}' --bot_password='{bot['password']}' --bot_output_directory='{BOT_OUTPUT_DIR}'")

    results = []
    for i in range(len(cmd_list)):
        results.append(pool.apply_async(call_proc, (cmd_list[i],)))

    # Close the pool and wait for each running task to complete
    pool.close()
    pool.join()
    print("All bots have finished their cycles")
    print("Writing log files")
    for result, bot in zip(results, bots):
        out, err = result.get()
        filename = f"{BOT_OUTPUT_DIR}/{bot['username']}.log"
        out = out.decode('utf-8')  
        err = err.decode('utf-8')
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(out)
        with open(filename, "a") as file:
            # Writing data to a file
            file.write("\n")
            file.write(f"------------------------------> {dt_string} <--------------------------------")
            file.write("\n")
            file.write("STDOUT:\n")
            file.write(f"{str(out)}\n")
            file.write("STDERR:\n")
            file.write(f"{str(err)}\n")
            file.write("------------------------------> End-of-Cycle <--------------------------------")
            file.write("\n")

if (__name__ == "__main__"):
    while True:
        main()
        print(f"Sleeping for {SLEEP_TIME}s")
        time.sleep(SLEEP_TIME)
