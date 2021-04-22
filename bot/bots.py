"""
This module creates several "bots" deployed on multiple threads and writes output, on a schedule, to separate
csv files for each bot.

https://pymotw.com/2/threading/
"""
import threading
import csv
import random
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')


def write_data(bot_id: int):
    """
    Writes random data to this particular bot's .csv file
    :param bot_id: id of the bot to associate the data.
    """
    logging.debug('About to write data.')
    rand_val = random.randint(1, 100)
    with open(f'{bot_id}_out.csv', 'a', newline='') as f:
        bot_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        bot_writer.writerow([bot_id, rand_val])
    logging.debug('Data has been written.')


def main():
    bots = [1, 2, 3]
    threads = []
    for bot_id in bots:
        t = threading.Timer(interval=random.randint(0, 3), function=write_data, args=(bot_id,))
        threads.append(t)
        t.start()

    print(threading.currentThread().getName(), threads)


if __name__ == '__main__':
    main()
