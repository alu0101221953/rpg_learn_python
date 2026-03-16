#!/usr/bin/python3

"""
Password cracker for ZIP files. Uses brute
force attack vector for this, so you must have
strong wordlist.

Usage:
    python3 zipbruter.py -f <encrypted_zip_file> -w <wordlist> -t <threads>
"""

from sys import exit as exit_
from os.path import isfile
from argparse import ArgumentParser
import threading
from queue import Queue
from zipfile import is_zipfile, ZipFile, BadZipfile

def password_gen(n):
    """Password generator for brute force attack vector"""
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ+-!@#$%^&*()_='
    if n == 0:
        yield ''
    else:
        for c in chars:
            for pwd in password_gen(n - 1):
                yield c + pwd

class ZipBruter:

    """Main ZipBruter class"""

    def __init__(self, file, word_list, threads, max_length=0) -> None:
        """Initialized function for ZipBruter"""
        self.file = file
        self.word_list = word_list
        self.threads = threads
        self.max_length = max_length

        # Thread-safe stop flag
        self.found = threading.Event()

        # Create FIFO queue
        self.queue = Queue()

    def worker(self) -> None:
        """Worker thread: checks passwords from the queue."""
        # Open the zip once per worker to avoid repeated overhead.
        with ZipFile(self.file) as zipfile:
            name = zipfile.namelist()[0]
            while not self.found.is_set():
                passwd = self.queue.get()
                if passwd is None:
                    self.queue.task_done()
                    break

                try:
                    with zipfile.open(name, pwd=passwd.encode()) as f:
                        f.read(1)
                    print('Found passwd: %s' % passwd)
                    self.found.set()
                except (RuntimeError, BadZipfile, KeyError):
                    pass
                finally:
                    self.queue.task_done()

    def start_workers(self) -> None:
        """Start worker threads."""
        for _ in range(self.threads):
            t = threading.Thread(target=self.worker, daemon=True)
            t.start()

    def main(self) -> None:
        """Main entrypoint for program"""
        self.start_workers()

        for target_passwd in self.read_wordlist():
            if self.found.is_set():
                break
            self.queue.put(target_passwd)

        # Stop workers
        for _ in range(self.threads):
            self.queue.put(None)

        self.queue.join()

    def read_wordlist(self):
        """Yield passwords from a wordlist file or a generated range."""
        if self.word_list:
            with open(self.word_list, 'r', errors='ignore') as file:
                for line in file:
                    yield line.strip()
        elif self.max_length > 0:
            for length in range(1, self.max_length + 1):
                for password in password_gen(length):
                    yield password


if __name__ == '__main__':
    print('ZipBruter - ZIP password cracker')
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help='Target encrypted zip file.')
    parser.add_argument('-w', '--word-list', type=str, help='Wordlist to be used.')
    parser.add_argument('-m', '--max-length', type=int, default=0,
                        help='Generate passwords up to this length (instead of using a wordlist).')
    parser.add_argument('-t', '--threads', type=int, default=4, help='Thread count.')
    args = parser.parse_args()

    if not args.file or (not args.word_list and args.max_length <= 0):
        print('Please provide a target file and either a wordlist (-w) or a max password length (-m).')
        exit_(1)

    if not is_zipfile(args.file):
        print('Please provide a valid zip file.')
        exit_(1)

    if args.word_list and not isfile(args.word_list):
        print('Please provide a valid wordlist file.')
        exit_(1)

    print('Starting brute force attack...')
    bruter = ZipBruter(args.file, args.word_list, args.threads, max_length=args.max_length)
    bruter.main()

    # Mostramos la duración del ataque
    if bruter.found.is_set():
        print('Brute force attack completed: password found.')
    else:
        print('Brute force attack completed: password not found.')