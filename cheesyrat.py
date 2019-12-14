#!/usr/bin/env python3
#coding: utf-8
#written by kyryloren. https://github.com/kyryloren/cheesyrat

from sys import exit
import signal
import socket
import argparse
import readline
from lib import colors
from tools import server
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
        menu_kw = ["help", "generate", "listen", "credits", "banner", "clear", "exit", "quit", "force quit"]
        completer = autocomplete.Complete(menu_kw)
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')
        ans = cheesyrat_lib.input_func(colors.GREEN + colors.BOLD + ' ┌─[' + colors.RED + 'cheesyrat' + colors.GREEN + colors.BOLD + ']--[' + colors.RED + colors.BOLD + '-' + colors.GREEN + colors.BOLD + ']-[' + colors.YELLOW + 'menu' + colors.GREEN + colors.BOLD + ']:\n' + ' └─────► ' + colors.END)
        ans = ans.lower()
        if ans.strip() == "help" or ans == "?":
            cheesyrat_lib.main_menu_help()
        elif ans.strip() == "generate":
            generate_menu()
        elif ans.strip() == "listen":
            listener_menu()
        elif ans.strip() == "credits":
            while True:
                cheesyrat_lib.clear()
                cheesyrat_lib.credits()
                back = input(colors.GREEN + colors.BOLD + '\n\nPress [ENTER] to return to menu' + colors.END)
                if back == "":
                    print("")
                    break
                else:
                    print("")
                    break
        elif ans.strip() == "banner":
            cheesyrat_lib.banner()
        elif ans.strip() == "clear":
            cheesyrat_lib.clear()
        elif ans.strip() == "exit" or ans.lower() == "quit":
            cheesyrat_lib.exit_function()
        elif ans.strip() == "force quit":
            cheesyrat_lib.force_quit()
        elif ans.strip() == "":
            pass
        else:
            cheesyrat_lib.warning_message("Invalid command. Type 'help' for help")

def generate_menu():
    while True:
        generate_kw = ["help", "clear", "back", "exit", "quit", "options", "info", "set", "run", "generate", "build", "force quit"]
        completer = autocomplete.Complete(generate_kw)
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')
        cmd = cheesyrat_lib.input_func(colors.GREEN + colors.BOLD + ' ┌─[' + colors.RED + 'cheesyrat' + colors.GREEN + colors.BOLD + ']--[' + colors.RED + colors.BOLD + '-' + colors.GREEN + colors.BOLD + ']-[' + colors.YELLOW + 'main/generate' + colors.GREEN + colors.BOLD + ']:\n' + ' └─────► ' + colors.END)
        cmd = cmd.lower()
        if cmd.strip() == "help" or cmd == "?":
            cheesyrat_lib.generate_menu_help()
        elif cmd.strip() == "options":
            cheesyrat_lib.payload_options()
        elif cmd.strip() == "info":
            cheesyrat_lib.payload_info()
        elif cmd.strip().startswith('set'):
            if len(cmd.split()) == 3:
                choice = cmd.split()[1]
                if choice.lower() == "lhost":
                    lhost = cmd.split()[2]
                    try:
                        if socket.gethostbyname(lhost) == lhost:
                            try:
                                socket.inet_aton(lhost)
                                cheesyrat_lib.update_json("lhost_payload", lhost, cheesyrat_lib.get_config_json_file())
                                print(" LHOST => " + lhost)
                            
                            except socket.error:
                                cheesyrat_lib.error_message("Invalid IP address. The IP is probably not up.", False)
                        else:
                            cheesyrat_lib.update_json("lhost_payload", lhost, cheesyrat_lib.get_config_json_file())
                            print(" LHOST => " + lhost)
                    except:
                        cheesyrat_lib.error_message("Invalid or misspelled host address.", False)
                elif choice.lower() == "lport":
                    try:
                        lport = int(cmd.split()[2])
                        if 1 <= lport <= 65535:
                            cheesyrat_lib.update_json("lport_payload", int(lport), cheesyrat_lib.get_config_json_file())
                            print(" LPORT => " + str(lport))
                        elif not 1 <= lport <= 65535:
                            cheesyrat_lib.error_message(str(lport) + " is not a valid port number.", False)
                    except ValueError:
                        cheesyrat_lib.error_message("The port provided is invalid", False)
                else:
                    cheesyrat_lib.warning_message("Invalid option after 'set'. Valid options are 'LHOST' and 'LPORT'.")
        elif cmd.strip() == "generate" or cmd.lower() == "build" or cmd.lower() == "run":
            print("generate payload")
        elif cmd.strip() == "clear":
            cheesyrat_lib.clear()
        elif cmd.strip() == "back":
            break
        elif cmd.strip() == "exit" or cmd.lower() == "quit":
            cheesyrat_lib.exit_function()
        elif cmd.strip() == "force quit":
            cheesyrat_lib.force_quit()
        elif cmd.strip() == "":
            pass
        else:
            cheesyrat_lib.warning_message("Invalid command. Type 'help' for help.")

def listener_menu():
    while True:
        generate_kw = ["help", "clear", "back", "exit", "quit", "options", "info", "set", "run", "listen", "force quit", "listen", "sessions", "list"]
        completer = autocomplete.Complete(generate_kw)
        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')
        listener = cheesyrat_lib.input_func(colors.GREEN + colors.BOLD + ' ┌─[' + colors.RED + 'cheesyrat' + colors.GREEN + colors.BOLD + ']--[' + colors.RED + colors.BOLD + '-' + colors.GREEN + colors.BOLD + ']-[' + colors.YELLOW + 'main/listener' + colors.GREEN + colors.BOLD + ']:\n' + ' └─────► ' + colors.END)
        listener = listener.lower()
        if listener.strip() == "help" or listener == "?":
            cheesyrat_lib.listener_menu_help()
        elif listener.strip() == "clear":
            cheesyrat_lib.clear()
        elif listener.strip() == "back":
            break
        elif listener.strip() == "options" or listener.lower() == "info":
            cheesyrat_lib.listener_options()
        elif listener.startswith('set'):
            if len(listener.split()) == 3:
                choice = listener.split()[1]
                if choice.lower() == "lhost":
                    lhost = listener.split()[2]
                    try:
                        if socket.gethostbyname(lhost) == lhost:
                            try:
                                socket.inet_aton(lhost)
                                cheesyrat_lib.update_json("lhost_listener", lhost, cheesyrat_lib.get_config_json_file())
                                print(" LHOST => " + lhost)
                            except socket.error:
                                cheesyrat_lib.error_message("Invalid IP address. The IP is probably not up.", False)
                        else:
                            cheesyrat_lib.update_json("lhost_listener", lhost, cheesyrat_lib.get_config_json_file())
                            print(" LHOST => " + lhost)
                    except:
                        cheesyrat_lib.error_message("Invalid or misspelled host address.", False)
                elif choice.lower() == "lport":
                    try:
                        lport = int(listener.split()[2])
                        if 1 <= lport <= 65535:
                            cheesyrat_lib.update_json("lport_listener", int(lport), cheesyrat_lib.get_config_json_file())
                            print(" LPORT => " + str(lport))
                        elif not 1 <= lport <= 65535:
                            cheesyrat_lib.error_message(str(lport) + " is not a valid port number.", False)
                    except ValueError:
                        cheesyrat_lib.error_message("The port provided is invalid", False)
            #     elif choice.lower() == "proxy":
            #         proxy = str(listener.split()[2])
            #         if proxy.lower() == "-h":
            #             cheesyrat_lib.proxy_menu_help()
            #         else:
            #             cheesyrat_lib.warning_message("Invalid option for 'proxy'")
            #     else:
            #         cheesyrat_lib.warning_message("Invalid option after 'set'. Valid options are 'LHOST' and 'LPORT'.")
            # elif len(listener.split()) == 5:
            #     proxy_select = listener.split()[1]
            #     if proxy_select.lower() == "proxy":
            #         proxy_type = listener.split()[2]
            #         proxy_host = listener.split()[3]
            #         proxy_port = listener.split()[4]
            #         if proxy_type.lower() == "socks5" or proxy_type.lower() == "socks4" or proxy_type.lower() == "http":
            #             print("wait")
            else:
                cheesyrat_lib.warning_message("Insufficient amount of arguments. Type 'help' for help.")
        elif listener.strip() == 'listen' or listener.lower() == 'run':
            print("listen")
        elif listener.strip().startswith('sessions'):
            if len(listener.split()) == 1:
                choice = listener.split()[0]
                cheesyrat_lib.warning_message("Invalid command. Please type 'sesssions -h' for help.")
            if len(listener.split()) == 2:
                selected_arg = listener.split()[1]
                if selected_arg.strip() == "-h" or selected_arg.strip() == "--help":
                    cheesyrat_lib.sessions_menu_help()
                elif selected_arg.strip() == "-l" or selected_arg.strip() == "--list":
                    server.list_connections()
                elif selected_arg.strip() == "-i" or selected_arg.strip() == "--interact":
                    cheesyrat_lib.warning_message("Please provide an interaction ID. Ex: 'sessions -i 2'.")
                else:
                    cheesyrat_lib.warning_message("Invalid argument. Please type 'sesssions -h' for help.")
            elif len(listener.split()) == 3:
                interact_arg = listener.split()[1]
                if interact_arg.strip() == '-i':
                    try:
                        sessions_id = int(listener.split()[2])
                        print(sessions_id)
                    except ValueError:
                        cheesyrat_lib.error_message("The ID provided is not a number.", False)
        elif listener.strip() == "exit" or listener.lower() == "quit":
            cheesyrat_lib.exit_function()
        elif listener.strip() == "force quit":
            cheesyrat_lib.force_quit()
        elif listener.strip() == "":
            pass
        else:
            cheesyrat_lib.warning_message("Invalid command. Type 'help' for help.")

if __name__ == "__main__":
    cheesyrat_lib.check_root()

    parser = argparse.ArgumentParser(add_help=False, description='Cheesyrat is an easy tool used to generate a peristent backdoor for remote access to a Windows machine.')
    parser.add_argument('-h', '-?', '--h', '-help', '--help', action="store_true", help=argparse.SUPPRESS)

    cheesyrat = parser.add_argument_group('[*] Cheesyrat options')
    cheesyrat.add_argument('--config', action="store_true", help="Regenerate the Cheesyrat framework configuration file")
    cheesyrat.add_argument('--setup', action="store_true", help="Tun the setup file and regenerate the Cheesyrat framework configuration file")
    cheesyrat.add_argument('--version', action="store_true", help="Displays version and quits")
    cheesyrat.add_argument('--clean', action="store_true", help="Clean out payloads and handlers")
    args = parser.parse_args()

    if args.h:
        parser.print_help()
        exit()
    if args.version:
        cheesyrat_lib.print_version()
        exit()
    if args.setup:
        cheesyrat_lib.setup_framework()
        exit()
    if args.config:
        cheesyrat_lib.config_framework()
        exit()
    if args.clean:
        cheesyrat_lib.clean_payloads()
        exit()
    else:
        pass

    cheesyrat_lib.check()
    signal.signal(signal.SIGINT, handler)
    complete_menu()
