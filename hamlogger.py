#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json
import datetime
import sys
import tty
import termios
from collections import defaultdict, namedtuple
import os


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("working")


def get_char():
    """Get a single character input"""

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def load_ham_log(fname='db.json'):
    """Load ham radio log entries"""

    fname = "db.json"
    try:
        with open(fname) as fd:
            data = fd.read()
        db = json.loads(data)
    except FileNotFoundError:
        db = {}

    return db


def save_ham_log(db, fname='db.json'):
    """Save database to file"""

    # TODO: error checking
    # json for now...

    with open(fname, 'w') as fd:
        fd.write(json.dumps(db))


def lookup(entry):
    """Lookup callsign on QRZ"""

    callsign = entry['callsign']
    url = "https://www.qrz.com/db/{}".format(callsign)
    os.system("open {}".format(url))


def add_log_entry(db, entry):
    """Add entry to the database"""

    callsign = entry.pop('callsign')
    if callsign is not '':
        if callsign not in db:
            db[callsign] = []
        db[callsign].append(entry)
        save_ham_log(db, 'tmp.json')


def get_time():
    """Get the time"""

    t = datetime.datetime.utcnow()
    Time = namedtuple("Time", ['date', 'time'])
    return Time(t.date(), t.time())


def get_callsign(db, entry):
    """Input callsign"""

    callsign = input("Callsign: ").upper()
    entry['callsign'] = callsign

    if callsign in db:

        if entry['name'] == '':
            entry['name'] = db[callsign][-1]['name']

        if entry['qth'] == '':
            entry['qth'] = db[callsign][-1]['qth']

    return entry


def get_name(entry):
    """Input name"""

    start_name = entry['name']

    name = input("Name: [{}] ".format(start_name).title())
    if name == '':
        name = start_name

    return name


def get_qth():
    """Get QTH"""

    qth = input("QTH: ").upper()
    return qth


def get_mode():
    """Get mode"""

    mode = input("Mode: ").upper()
    return mode


def get_freq():
    """ Get the frequency"""

    freq = input("Frequency: ")
    return freq


def get_tx_rst():
    """Input TX RST"""

    rst = input("TX (RST): ")
    return rst


def get_rx_rst():
    """Input RX RST"""

    rst = input("RX (RST): ")
    return rst


def print_entry(entry):
    """Print out a single entry"""

    output = ("\n"
              "===========================================================\n"
              "\n"
              "Callsign: {callsign}\n"
              "Name: {name}\n"
              "QTH: {qth}\n"
              "Start Date: {start_date}\n"
              "Start Time: {start_time}\n"
              "End Date: {end_date}\n"
              "End Time: {end_time}\n"
              "\n"
              "Mode: {mode}\n"
              "Frequency: {freq}\n"
              "TX (RST): {tx_rst}\n"
              "RX (RST): {rx_rst}\n"
              "\n"
              "===========================================================\n")

    print(output.format(**entry))


def print_db_entry(entry):
    """Print an entry out of the database"""

    output = ("\n"
              "Name: {name}\n"
              "QTH: {qth}\n"
              "Start Date: {start_date}\n"
              "Start Time: {start_time}\n"
              "End Date: {end_date}\n"
              "End Time: {end_time}\n"
              "\n"
              "Mode: {mode}\n"
              "Frequency: {freq}\n"
              "TX (RST): {tx_rst}\n"
              "RX (RST): {rx_rst}\n"
              "\n")

    print(output.format(**entry))


def print_database(db):
    """Print out the database"""

    for key in db:
        print("===========================================================")
        print("{}".format(key))
        print("-----------------------------------------------------------")
        for entry in db[key]:
            entry = defaultdict(str, entry)
            print_db_entry(entry)
        print("===========================================================\n")


def main_menu():
    """Print main menu"""

    output = (
        "-----------------------------------------------------------\n"
        "(c)allsign, (n)ame, qt(h), (s)tart time, (e)nd time        \n"
        "(m)ode, (f)req, (t)x rst, (r)x rst, sa(v)e entry, (q)uit   \n"
        "-----------------------------------------------------------\n"
    )
    print(output)


def main():
    """ Main code block """

    db = load_ham_log()

    entry = defaultdict(str)
    default_entry = defaultdict(str)

    while True:

        print_entry(entry)
        main_menu()

        c = get_char()

        if c == 's':
            t = get_time()
            entry['start_time'] = str(t.time).split(".")[0]
            entry['start_date'] = str(t.date)

        if c == 'e':
            t = get_time()
            entry['end_time'] = str(t.time).split(".")[0]
            entry['end_date'] = str(t.date)

        if c == 'c':
            entry = get_callsign(db, entry)

        if c == 'n':
            name = get_name(entry)
            entry['name'] = name

        if c == 'h':
            qth = get_qth()
            entry['qth'] = qth

        if c == 'm':
            mode = get_mode()
            entry['mode'] = mode
            default_entry['mode'] = mode

        if c == 'f':
            freq = get_freq()
            entry['freq'] = freq
            default_entry['freq'] = freq

        if c == 't':
            tx_rst = get_tx_rst()
            entry['tx_rst'] = tx_rst

        if c == 'r':
            rx_rst = get_rx_rst()
            entry['rx_rst'] = rx_rst

        if c == 'v':
            add_log_entry(db, entry)
            entry = defaultdict(str, default_entry)

        if c == 'x':
            entry = defaultdict(str, default_entry)

        if c == 'p':
            print_database(db)

        if c == 'l':
            lookup(entry)

        if c == 'q':
            save_ham_log(db)
            break


if __name__ == "__main__":
    main()
