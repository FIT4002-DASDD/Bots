Small project to demonstrate how to use a C++ Service Worker, that runs on a schedule, to push data outputted
from bots to an external database like AWS RDS.

Files:

- bots.py:
    - an emulation of multiple bots (running via several threads)
    - each bot outputs some data into a csv file for that bot.

- csv files:
    - each bot outputs one
    - simple schema eg:
        bot_id, num
        1, 69
        3, 1738