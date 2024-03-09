import pickle
from addressbook import *

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(msg):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except BookValueError as err:
                return err
            except ValueError:
                return msg 
            except IndexError:
                return msg 
            except KeyError as name:
                return f"Contact with name {name} not found"
        
        return inner
    return decorator

@input_error("Give me name and phone please.")
def add_contact(args, contacts):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact added."

@input_error("Give me name and birthday please.")
def add_birthday(args, contacts):
    name, bd = args
    rec = contacts.find(name)
    rec.add_birthday(bd)
    return "Birthday added."

@input_error("Give me name and new phone please.")
def change_contact(args, contacts):
    name, no = args
    rec = contacts.find(name)
    rec.change_phone(no)
    return "Contact updated."

@input_error("Give me name please.")
def show_phone(args, contacts):
    name = args[0]
    return str(contacts.find(name))

@input_error("Give me name please.")
def show_birthday(args, contacts):
    name = args[0]
    rec = contacts.find(name)
    if rec.birthday is None:
        return "Birthday don't setted."
    return f"{name}'s birthday is {rec.birthday}"

def main():
    fn = "address-book.dmp"
    book = AddressBook()
    with open(fn, "rb") as fh:
        book = pickle.load(fh)

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            with open(fn, "wb") as fh:
                pickle.dump(book, fh)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(book)
        elif command == "birthdays":
            print(book.get_birthdays_per_week())
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "help":
            print("My command list is: {}".format(", ".join([
                "close", "exit",
                "hello",
                "add",
                "change",
                "phone",
                "all",
                "add-birthday",
                "show-birthday",
                "birthdays"
                ])))
        else:
            print("Invalid command. Try 'help'")

if __name__ == "__main__":
    main()