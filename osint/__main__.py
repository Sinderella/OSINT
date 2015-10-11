from logbook import FileHandler

from osintconsole import Console

log_handler = FileHandler('application.log')


def main():
    try:
        Console().cmdloop()
    except KeyboardInterrupt:
        print("Quitting...")


if __name__ == '__main__':
    with log_handler.applicationbound():
        main()
