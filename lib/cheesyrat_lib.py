import subprocess
import os
import string
import time
import sys
import platform
import json
from lib import colors

def get_json_file():
    #Add check to see if exists. If not, create one and put data in it
    cwd = os.getcwd()
    json_file = cwd + "/run.json"
    return json_file

def warning_message(warning):
    print(colors.RED + "\n[!] Warning: " + warning + colors.END + "\n")

def error_message(error, exit):
    if exit == True:
        print(colors.RED + "\n[!] Error has occured: " + error + "Exiting..." + colors.END + "\n")
        sys.exit()
    elif exit == False:
        print(colors.RED + "\n[!] Error has occured: " + error + colors.END + "\n")

def clear():
    subprocess.Popen( "cls" if platform.system() == "Windows" else "clear", shell=True)
    time.sleep(0.1)

def banner():
    print('                    ')
    print(colors.GREEN + colors.BOLD + '             /|         ,  ')
    print('           ,///        /|  ')
    print('          // //     ,///   ')
    print('         // //     // //   ')
    print('        || ||    // //   ' + '  ,--,  .-. .-.,---.  ,---.  ,---.     .---..-.   .-.,---.    .--.  _______ ')
    print('        // //     || ||  ' + ".' .')  | | | || .-'  | .-'  | .-'    ( .-._)\ \_/ )/| .-.\  / /\ \|__   __|")
    print('        || ||   // // ' + "   |  |(_) | `-' || `-.  | `-.  | `-.   (_) \    \   (_)| `-'/ / /__\ \ )| |")
    print('        || ||  // //  ' + "   \  \    | .-. || .-'  | .-'  | .-'   _  \ \    ) (   |   (  |  __  |(_) |")
    print('        || || || ||   ' + "    \  `-. | | |)||  `--.|  `--.|  `--.( `-'  )   | |   | |\ \ | |  |)|  | |")
    print('         \\,\|,|\_//   ' + "     \____\/(  (_)/( __.'/( __.'/( __.' `----'   /(_|   |_| \)\|_|  (_)  `-'")
    print('          \\)\)\\|/     ' + '       (__)   (__)   (__)   (__)             (__)        (__)')
    print('         )-."" .-(         ')
    print('         //^\` `/^\\        ' + colors.END + colors.BOLD + '[' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']   Backdoor Generator for Remote Access  [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.GREEN + colors.BOLD + '        //  |   |  \\       ' + colors.END + colors.BOLD + '[' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']' + colors.VIOLET + colors.BOLD + '          Created by:' + colors.RED + ' kyryloren          ' + colors.END + colors.BOLD + '[' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.GREEN + colors.BOLD + '      ,/_| ' + colors.END + colors.BOLD + '0' + colors.GREEN + colors.BOLD + '| _ | ' + colors.END + colors.BOLD + '0' + colors.GREEN + colors.BOLD + '|_\,    ' + colors.END + colors.BOLD + '[' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']' + colors.VIOLET + colors.BOLD + '             Version:' + colors.RED + ' 1.0.0' + colors.END + colors.BOLD + '              [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.GREEN + colors.BOLD + '    /`    `"=.v.="`    `\\  ' + colors.END + colors.BOLD + '[' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']' + colors.VIOLET + colors.BOLD + '      Github:' + colors.RED + colors.BOLD + ' https://git.io/Jeoco' + colors.END + colors.BOLD + '       [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.GREEN + colors.BOLD + '   /`    _."{_,_}"._    `\\ ' + colors.END + colors.BOLD + '[' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']' + colors.VIOLET + colors.BOLD + '      Follow me on Twitter:' + colors.RED + ' @0V01d' + colors.END + colors.BOLD + '       [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.GREEN + colors.BOLD + '  `/`  ` \  |||  / `  `\`  ' + colors.END + colors.BOLD + '[' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']                                         [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.GREEN + colors.BOLD + '   `",_  \\=^~^=//  _,"`    ' + colors.END + colors.BOLD + '[' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']        Rats can eat cheese too!         [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.GREEN + colors.BOLD + '       "=,\"-=-"/,=         ' + colors.END + colors.BOLD + '[' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + '] ._____________________________________. [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.GREEN + colors.BOLD + "           '---'           " + colors.END + colors.BOLD + '\_.-------------------------------------------._/' + colors.END)
    print('                             ')
    print('                             ')

def main_menu_help():
    print("")
    print(colors.CYAN + "+--------------------------------------------------+")
    print(colors.CYAN + "|" + colors.GREEN + " Main Menu Help Commands:" + colors.CYAN + "                         |")
    print(colors.CYAN + "+--------------------------------------------------+")
    print(colors.CYAN + "|  " + colors.END + "help or ?: " + colors.GREEN + "This help message" + colors.CYAN + "                    |")
    print(colors.CYAN + "|  " + colors.END + "generate: " + colors.GREEN + "Switch to the cheesyrat generator" + colors.CYAN + "     |")
    print(colors.CYAN + "|  " + colors.END + "listen: " + colors.GREEN + "Switch to the cheesyrat listener" + colors.CYAN + "        |")
    print(colors.CYAN + "|  " + colors.END + "clear: " + colors.GREEN + "Clear the screen" + colors.CYAN + "                         |")
    print(colors.CYAN + "|  " + colors.END + "banner: " + colors.GREEN + "Print the banner" + colors.CYAN + "                        |")
    print(colors.CYAN + "|  " + colors.END + "credits: " + colors.GREEN + "View the credits" + colors.CYAN + "                       |")
    print(colors.CYAN + "|  " + colors.END + "quit or exit: " + colors.GREEN + "Exit the cheesyrat framework" + colors.CYAN + "      |")      
    print(colors.CYAN + "+--------------------------------------------------+")
    print("")

def input_func(text):
    py_version=platform.python_version()
    
    if py_version[0] == "3":
        Ans = input(text)
    else:
        print(error_message("Looks like you're not running Python 3!", exit=True))
    return Ans

def credits():
    subprocess.call(['clear'])
    print(colors.RED + '==========================================================')
    print(colors.END + colors.BOLD + '                         Credits:                         ')
    print(colors.RED + '==========================================================')
    print(colors.END + colors.BOLD + '\nSpecial Thanks To:')
    print(colors.RED + colors.BOLD + '\nOffensive Security')
    print(colors.VIOLET + colors.BOLD + '\nhttps://www.offensive-security.com/')
    print(colors.YELLOW + colors.BOLD + "\nhttps://www.kali.org/")
    print(colors.RED + colors.BOLD + "\nhttps://github.com")
    print("")

def append_runjson(context, name_to_append):
    with open(get_json_file()) as json_file:
        data = json.load(json_file)
        for p in data[context]:
            return p[name_to_append]

def exit_function():
    if append_runjson("session_info", "is_sessions_open") == "false":
        print(colors.GREEN + "\n\nThank you for shopping with cheesyrat. Come again soon :)\n\n" + colors.END)
        sys.exit()
    elif append_runjson("session_info", "is_sessions_open") == "true":
        error_message("Cannot exit, there are sessions open.", exit=False)

