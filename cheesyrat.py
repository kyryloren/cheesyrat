#!/usr/bin/env python3
#coding: utf-8
#written by kyryloren. https://github.com/kyryloren/cheesyrat

import os
import time
import signal
import socket
import logging
import readline
import threading
from lib import colors
from lib import autocomplete
from lib import cheesyrat_lib

def handler(signum, frame):
    cheesyrat_lib.plain_message(colors.YELLOW, "Please use 'exit' or 'quit' to exit the framework. You might have sessions open...", True, False)
    cheesyrat_lib.plain_message(colors.YELLOW, "Press [ENTER] to continue...", False, False)

def complete_menu():
    cheesyrat_lib.clear()
    cheesyrat_lib.banner()
    answ=True
    while answ:
        ans = ""
        menu_kw = ["help", "generate", "listen", "credits", "banner", "clear", "exit", "quit", "force quit"]
        completer = autocomplete.Complete(menu_kw)
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
        elif ans.lower() == "force quit":
            cheesyrat_lib.force_quit()
        elif ans == "":
            pass
        else:
            cheesyrat_lib.warning_message("Invalid command.")

def generate_menu():
    while True:
        generate_kw = ["help", "clear", "back", "exit", "quit", "options", "info", "set", "run", "generate", "build", "run", "force quit"]
        completer = autocomplete.Complete(generate_kw)
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')
        cmd = cheesyrat_lib.input_func(colors.GREEN + colors.BOLD + ' ┌─[' + colors.RED + 'cheesyrat' + colors.GREEN + colors.BOLD + ']--[' + colors.RED + colors.BOLD + '-' + colors.GREEN + colors.BOLD + ']-[' + colors.YELLOW + 'main/generate' + colors.GREEN + colors.BOLD + ']:\n' + ' └─────► ' + colors.END)
        if cmd.lower() == "help":
            cheesyrat_lib.generate_menu_help()
        elif cmd.lower() == "?":
            cheesyrat_lib.generate_menu_help()
        elif cmd.lower() == "options" or cmd.lower() == "info":
            cheesyrat_lib.payload_options()
        elif cmd.lower()[0:9] == "set lhost":
            lhost = cmd[10:]
            try:
                if socket.gethostbyname(lhost) == lhost:
                    try:
                        socket.inet_aton(lhost)
                        cheesyrat_lib.update_json("lhost", lhost, cheesyrat_lib.get_config_json_file())
                        print(" LHOST => " + lhost)
                    except socket.error:
                        cheesyrat_lib.error_message("Invalid host address. The host is probably not up.", False)
                else:
                    cheesyrat_lib.update_json("lhost", lhost, cheesyrat_lib.get_config_json_file())
                    print(" LHOST => " + lhost)
            except:
                cheesyrat_lib.error_message("Invalid or misspelled host address.", False)
        elif cmd.lower()[0:9] == "set lport":
            try:
                lport = int(cmd[10:])
                if 1 <= lport <= 65535:
                    cheesyrat_lib.update_json("lport", int(lport), cheesyrat_lib.get_config_json_file())
                    print(" LPORT => " + str(lport))
                elif not 1 <= lport <= 65535:
                    cheesyrat_lib.error_message(str(lport) + "is not a valid port number.", False)
            except ValueError:
                cheesyrat_lib.error_message("The port provided is invalid", False)
        elif cmd.lower() == "generate" or cmd.lower() == "build" or cmd.lower() == "run":
            print("generate payload")
        elif cmd.lower() == "clear":
            cheesyrat_lib.clear()
        elif cmd.lower() == "back":
            break
        elif cmd.lower() == "exit":
            cheesyrat_lib.exit_function()
        elif cmd.lower() == "quit":
            cheesyrat_lib.exit_function()
        elif cmd.lower() == "force quit":
            cheesyrat_lib.force_quit()
        elif cmd == "":
            pass
        else:
            cheesyrat_lib.warning_message("Invalid command.")

if __name__ == "__main__":
    cheesyrat_lib.check()
    signal.signal(signal.SIGINT, handler)
    complete_menu()
