import subprocess
import os
import string
import time
import sys
import platform
import json
from lib import colors

def get_run_json_file():
    #Add check to see if exists. If not, create one and put data in it
    cwd = os.getcwd()
    json_file = cwd + "/lib/run.json"
    return json_file

def get_config_json_file():
    cwd = os.getcwd()
    json_file = cwd + "/lib/config.json"
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
    print(colors.CYAN + "|" + colors.GREEN + "  Main Menu Help Commands:" + colors.CYAN + "                        |")
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

def generate_menu_help():
    print("")
    print(colors.CYAN + "+--------------------------------------------------+")
    print(colors.CYAN + "|" + colors.GREEN + "  Generate Menu Help Commands:" + colors.CYAN + "                    |")
    print(colors.CYAN + "+--------------------------------------------------+")
    print(colors.CYAN + "|  " + colors.END + "help or ?: " + colors.GREEN + "This help message" + colors.CYAN + "                    |")
    print(colors.CYAN + "|  " + colors.END + "options: " + colors.GREEN + "List the options for the payload" + colors.CYAN + "       |")
    print(colors.CYAN + "|  " + colors.END + "generate: " + colors.GREEN + "Generate payload" + colors.CYAN + "                      |")
    print(colors.CYAN + "|  " + colors.END + "clear: " + colors.GREEN + "Clear the screen" + colors.CYAN + "                         |")
    print(colors.CYAN + "|  " + colors.END + "back: " + colors.GREEN + "Return to main menu" + colors.CYAN + "                       |")
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
    print(colors.CYAN + "+----------------------------------------------------------+")
    print(colors.CYAN + "|" + colors.GREEN + "  Credits:" + colors.CYAN + "                                                |")
    print(colors.CYAN + "+----------------------------------------------------------+")
    print(colors.CYAN + "|  " + colors.END + "This framework was created by @kyryloren" + colors.CYAN + "                |")
    print(colors.CYAN + "|  " + colors.END + "Github: " + colors.GREEN + "https://github.com/kyryloren" + colors.CYAN + "                    |")
    print(colors.CYAN + "+----------------------------------------------------------+")
    print(colors.CYAN + "|" + colors.GREEN + "  Notable Mensions:" + colors.CYAN + "                                       |")
    print(colors.CYAN + "+----------------------------------------------------------+")      
    print(colors.CYAN + "|  " + colors.END + "Offensive Security: " + colors.GREEN + "https://www.offensive-security.com" + colors.CYAN + "  |")
    print(colors.CYAN + "|  " + colors.END + "Kali Linux: " + colors.GREEN + "https://www.kali.org" + colors.CYAN + "                        |")
    print(colors.CYAN + "|  " + colors.END + "Fat Rat: " + colors.GREEN + "https://github.com/StreetSec/FatRat" + colors.CYAN + "            |")
    print(colors.CYAN + "+----------------------------------------------------------+")
    print("")

def payload_options():
    print("")
    print("Payload options (cheesyrat/windows/reverse_tcp)")
    print("")
    data =[['Name', 'Current Setting', 'Required', 'Description'], ['----', '---------------', '--------', '-----------'], 
    ['LHOST', append_json("lhost", get_config_json_file()), 'yes', 'The connect back address'], 
    ['LPORT', append_json("lport", get_config_json_file()), 'yes', 'The connect back port']]
    col_width = [max(map(len, col)) for col in zip(*data)]
    for row in data:
        print("  ".join((val.ljust(width) for val, width in zip(row, col_width))))
    print("")

def append_json(name_to_append, file):
    with open(file) as json_file:
        data = json.load(json_file)
        return data[name_to_append]

def update_json(name_to_append, value, file):
    jsonFile = open(file, "r")
    data = json.load(jsonFile)
    jsonFile.close()

    data[name_to_append] = value

    jsonFile = open(file, 'w+')
    jsonFile.write(json.dumps(data))
    jsonFile.close()

def exit_function():
    if append_json("is_sessions_open", get_run_json_file()) == "false":
        print(colors.GREEN + "\n\nThank you for shopping with cheesyrat. Come again soon :)\n\n" + colors.END)
        sys.exit()
    elif append_json("is_sessions_open", get_run_json_file()) == "true":
        error_message("Cannot exit, there are sessions open.", exit=False)

