#!/usr/bin/python3
import cmd


class HBNBCommand(cmd.Cmd):

    """Defines the HBnB console."""

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the programn\n"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty line input"""
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
