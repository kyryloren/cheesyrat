#!/usr/bin/env python3

"""
Able to call this by doing: cheesyrat.py --config
"""

import platform
import os
import sys
import pwd

def generateConfig(options):
    # General
    config = """#!/usr/bin/python

##################################################################################################
#
# Cheesyrat configuration file
#
##################################################################################################


#################################################
#
# General system options
#
#################################################
"""
    print("\nCheesyrat Configuration:")

    # OS
    config += '# OS to use (Kali/Backtrack/Debian/Windows)\n'
    config += 'OPERATING_SYSTEM="' + options['OPERATING_SYSTEM'] + '"\n\n'
    print("[*] OPERATING_SYSTEM = " + options['OPERATING_SYSTEM'])

    # OS (Linux)
    config += '# Specific Linux distro\n'
    # Check /etc/issue for the exact linux distro
    issue = open("/etc/issue").read()
    if issue.startswith("Debian"):
        config += 'DISTRO="Debian"\n\n'
    else:
        config += 'DISTRO="Linux"\n\n'

    # Cheesyrat path
    config += '# Cheesyrat install path\n'
    config += 'CHEESYRAT_PATH="' + options['CHEESYRAT_PATH'] + '"\n\n'
    print( "[*] CHEESYRAT_PATH = " + options['CHEESYRAT_PATH'] )

    # Wine's path
    config += '# Wine environment\n'
    config += 'WINEPREFIX="' + options["WINEPREFIX"] + '"\n\n'
    print( "[*] WINEPREFIX = " + options["WINEPREFIX"] )

    # Temp path
    config += '# Path to temporary directory\n'
    config += 'TEMP_PATH="' + options["TEMP_PATH"] + '"\n\n'
    print( "[*] TEMP_PATH = " + options["TEMP_PATH"] )

    # PyInstaller's path
    config += '# The path to pyinstaller, for example: %s\n' % ( options['PYINSTALLER_PATH'] )
    config += 'PYINSTALLER_PATH="' + options['PYINSTALLER_PATH'] + '"\n\n'
    print( "[*] PYINSTALLER_PATH = " + options['PYINSTALLER_PATH'] )

    # Padding between sections
    print ( "\n" )

    # Veil-Evasion
    config += """

#################################################
#
# Cheesyrat specific options
#
#################################################
"""
    print( "\nCheesyrat Specific Configuration Options:" )

    # Payload path
    source_path = os.path.expanduser( options["PAYLOAD_SOURCE_PATH"] )
    config += '# Path to output the source of payloads\n'
    config += 'PAYLOAD_SOURCE_PATH="' + source_path + '"\n\n'
    print( "[*] PAYLOAD_SOURCE_PATH = " + source_path )

    # Compile path
    compiled_path = os.path.expanduser( options["PAYLOAD_COMPILED_PATH"] )
    config += '# Path to output compiled payloads\n'
    config += 'PAYLOAD_COMPILED_PATH="' + compiled_path +'"\n\n'
    print( "[*] PAYLOAD_COMPILED_PATH = " + compiled_path )

    # Handler path
    handler_path = os.path.expanduser( options["HANDLER_PATH"] )
    config += '# Where to generate a msf handler script\n'
    config += 'HANDLER_PATH="' + handler_path + '"\n\n'
    print( "[*] HANDLER_PATH = " + handler_path )

    # Shoud we save handlers on exit
    config += '# Should we save the runtime handlers before we exit?\n'
    config += 'SAVE_HANDLERS_ON_EXIT="' + options['SAVE_HANDLERS_ON_EXIT'] + '"\n\n'
    print("[*] SAVE_HANDLERS_ON_EXIT = " + options['SAVE_HANDLERS_ON_EXIT'])

    # Create the output compiled path if it doesn't exist
    if not os.path.exists( handler_path ):
        os.makedirs( handler_path )
        print( "[*] Path Created: '" + handler_path )

    # Create the output source path if it doesn't exist
    if not os.path.exists( source_path ):
        os.makedirs( source_path )
        print( "[*] Path Created: '" + source_path )

    # Create the output compiled path if it doesn't exist
    if not os.path.exists( compiled_path ):
        os.makedirs( compiled_path )
        print( "[*] Path Created: '" + compiled_path )

    # Save config
    if platform.system() == "Linux":
        # create the output compiled path if it doesn't exist
        if not os.path.exists("/etc/cheesyrat/"):
            os.makedirs("/etc/cheesyrat/")
            print( "[*] Path '/etc/cheesyrat/' Created")
        f = open("/etc/cheesyrat/settings.py", 'w')
        f.write(config)
        f.close()
        os.chmod("/etc/cheesyrat/settings.py", 0o0755)
        print("\n\n[*] Configuration File Written To: '/etc/cheesyrat/settings.py'\n")
    else:
        print("[!] ERROR: PLATFORM NOT CURRENTLY SUPPORTED")
        sys.exit()


if __name__ == '__main__':

    options = {}

    # Check for root access
    if os.geteuid() != 0:
        print( "\n[!] ERROR: Not root. Requesting...\n" )
        os.execvp( "sudo", ["sudo"] + ["python"] + sys.argv )
        sys.exit()

    if platform.system() == "Linux":
        # Check /etc/issue for the exact linux distro
        issue = open( "/etc/issue" ).read()

        # General options
        options["OPERATING_SYSTEM"] = "Linux"
        options["PYINSTALLER_PATH"] = "/var/lib/cheesyrat/PyInstaller-3.2.1/" # via /config/setup.sh
        options["TEMP_PATH"] = "/tmp/cheesyrat/"
        options["WINEPREFIX"] = "/var/lib/cheesyrat/wine/"
        CHEESYRAT_PATH = "/".join( os.getcwd().split( "/" )[:-1] ) + "/"
        options["CHEESYRAT_PATH"] = CHEESYRAT_PATH

        # Cheesyrat specific options
        options["HANDLER_PATH"] = "/var/lib/cheesyrat/output/handlers/"
        options["PAYLOAD_COMPILED_PATH"] = "/var/lib/cheesyrat/output/compiled/"
        options["PAYLOAD_SOURCE_PATH"] = "/var/lib/cheesyrat/output/source/"
        options['SAVE_HANDLERS_ON_EXIT'] = "true"

        # Kali
        if issue.startswith( ("Kali", "Parrot") ):
            options["OPERATING_SYSTEM"] = "Kali"
        # BackTrack
        elif issue.startswith( "BackTrack" ):
            options["OPERATING_SYSTEM"] = "BackTrack"

        # Check the paths are correct (WINEPREFIX)
        while not os.path.isdir( options["TEMP_PATH"] ):
            path = input( "[*] Please enter the directory of your system's temp path (e.g. /tmp/): " )
            path = str(path)
            options["TEMP_PATH"] = path
        if not options["TEMP_PATH"].endswith('/'):
            options["TEMP_PATH"] += "/"

        # Check the paths are correct (CHEESYRAT_PATH)
        while not os.path.isdir( options["CHEESYRAT_PATH"] ):
            print( "\n[*] Can't find the cheesyrat path?   Run: %s --force --silent" % ( os.path.abspath("./config/setup.sh" ) ) )
            path = str(path)
            path = input( "[*] Please enter the directory to Cheesyrat (e.g. /opt/cheesyrat/): " )
            options["CHEESYRAT_PATH"] = path
        if not options["CHEESYRAT_PATH"].endswith('/'):
            options["CHEESYRAT_PATH"] += "/"

        # Check the paths are correct (PYINSTALLER_PATH)
        while not os.path.isdir( options["PYINSTALLER_PATH"] ):
            print( "\n [i] Can't find PyInstaller?   Run: %s --force --silent" % ( os.path.abspath("./config/setup.sh" ) ) )
            path = input( " [>] Please enter the directory of PyInstaller (e.g. %s): " % ( options["PYINSTALLER_PATH"] ) )
            path = str(path)
            options["PYINSTALLER_PATH"] = path
        if not options["PYINSTALLER_PATH"].endswith('/'):
            options["PYINSTALLER_PATH"] += "/"

        # Check the paths are correct (WINEPREFIX)
        while not os.path.isdir( options["WINEPREFIX"] ):
            print( "\n[*] Can't find WINE profile?   Run: %s --force --silent" % ( os.path.abspath("./config/setup.sh" ) ) )
            path = input( "[*] Please enter the directory of Veil's WINE profile (e.g. %s): " % ( options["WINEPREFIX"] ) )
            path = str(path)
            options["WINEPREFIX"] = path
        if not options["WINEPREFIX"].endswith('/'):
            options["WINEPREFIX"] += "/"
    # Unsupported platform...
    else:
        print( "[!] ERROR: PLATFORM NOT CURRENTLY SUPPORTED" )
        sys.exit()

    generateConfig(options)
