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
import json
from lib import colors
from lib import cheesyrat_lib

def complete_menu():
    cheesyrat_lib.clear()
    cheesyrat_lib.banner()
    answ=True
    while answ:
        ans = ""
        ans = cheesyrat_lib.input_func(colors.GREEN + colors.BOLD + ' ┌─[' + colors.RED + 'ChubbyBunny' + colors.GREEN + colors.BOLD + ']--[' + colors.RED + colors.BOLD + '-' + colors.GREEN + colors.BOLD + ']-[' + colors.YELLOW + 'menu' + colors.GREEN + colors.BOLD + ']:\n' + ' └─────► ' + colors.END)

        if ans.lower() == "help":
            cheesyrat_lib.main_menu_help()
        elif ans == "?":
            cheesyrat_lib.main_menu_help()
        elif ans.lower() == "generate":
            print("load generator")
        elif ans.lower() == "listen":
            print("load listener")
        elif ans.lower() == "credits":
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

if __name__ == "__main__":
    complete_menu()
