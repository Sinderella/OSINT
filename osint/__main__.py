import sys

from logbook import FileHandler

from osintconsole import Console

log_handler = FileHandler('application.log')


def main():
    console = Console()
    while True:
        try:
            console.cmdloop()
        except KeyboardInterrupt:
            print("Quitting...")
            sys.exit(0)


if __name__ == '__main__':
    with log_handler.applicationbound():
        main()
