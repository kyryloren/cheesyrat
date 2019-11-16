#!/bin/bash

green=''
red='\033[0;31m'
green='\033[0;32m'
white='\033[1;37m'
orange='\033[0;33m'
reset='\033[0m'

banner () {
    echo "+------------------------------------------+"
    printf "|${white} %-40s |\n" "`date`"
    echo "|                                          |"
    printf "|${green} %-40s `tput sgr0`|\n" "$@"
    echo "+------------------------------------------+"
}

main () {
    clear_screen
    is_root
    is_internet
    banner "Starting cheesyrat installation..."
    sleep 3
    check_os
}

clear_screen () {
    printf "\033c"
}

is_root () {
    if [ "$EUID" -ne 0 ]
    then
        printf "\n${red}[!] Please run this script as root.${reset}\n\n"
        exit
    fi
}

is_internet () {
    if [! ping -q -w 1 -c 1 google.com] 2>/dev/null;
    then
        printf "\n${red}[!] Please connect to the internet to install.${reset}\n\n"
        exit
    fi
}

check_os () {
    if [ "($uname)" == "Darwin" ]; then
        printf "${red}[!] MacOS detected. Please run this program on a supporting Linux distribution.${reset}\n\n"
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        printf "${green}[*] Linux OS detected. Installing required packages...${reset}\n\n"
        install
    elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
        printf "${red}[!] Windows 32x OS detected. How and why are you running this here??${reset}\n\n"
    elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
        printf "${red}[!] Windows 64x OS detected. How and why are you running this here??${reset}\n\n"
    fi
}

install() {
    update
    python_setup
    wine_setup
    python_setup_wine
    pip_setup
    done_setup
}

update () {
    printf "\n${green}[*] Updating and upgrading packages. ${orange}This will take a while. Please be patcient.${reset}\n"
    apt-get -y update
    apt-get -y upgrade
    printf "\n\n${green}[*] Finished updating and upgrading packages! Moving on...${reset}\n\n"
    sleep 3
    clear_screen
}

python_setup () {
    if [ $(dpkg-query -W -f='${Status}' python3 2>/dev/null | grep -c "ok installed") -eq 0 ];
    then
        printf "${orange}[!] Python 3 installation not found. Installing it for you...${reset}\n"
        apt-get -qq -y install python3
        sleep 3
        printf "\n\n${green}[*] Done!${reset}\n"
        clear_screen
    elif [ $(dpkg-query -W -f='${Status}' python3 2>/dev/null | grep -c "ok installed") -eq 1 ];
    then
        printf "${green}[*] Python 3 found. Continuing setup...${reset}\n"
        sleep 3
    fi

    if [ $(dpkg-query -W -f='${Status}' python3-pip 2>/dev/null | grep -c "ok installed") -eq 0 ];
    then
        printf "${orange}[!] Pip for Python 3 not found. Installing it for you...${reset}\n"
        apt-get -qq -y install python3-pip
        sleep 3
        printf "\n\n${green}[*] Done!${reset}\n"
        clear_screen
    elif [ $(dpkg-query -W -f='${Status}' python3-pip 2>/dev/null | grep -c "ok installed") -eq 1 ];
    then
        printf "${green}[*] Pip for Python 3 found. Continuing setup...${reset}\n"
        sleep 3
    fi

    if [ $(dpkg-query -W -f='${Status}' wget 2>/dev/null | grep -c "ok installed") -eq 0 ];
    then
        printf "${orange}[!] Wget installation not found. How do you not have this...?? Installing it for you...${reset}\n"
        apt-get -qq -y install wget
        sleep 3
        printf "\n\n${green}[*] Done!${reset}\n"
        clear_screen
    elif [ $(dpkg-query -W -f='${Status}' wget 2>/dev/null | grep -c "ok installed") -eq 1 ];
    then
        printf "${green}[*] Wget found, whew. Checking wine...${reset}\n"
        sleep 3
    fi
}

wine_setup () {
    if [ $(dpkg-query -W -f='${Status}' wine 2>/dev/null | grep -c "ok installed") -eq 0 ];
    then
        printf "${orange}[!] Wine installation not found. Installing it for you...${reset}\n"
        apt-get -qq -y install wine
        sleep 3
        printf "\n\n${green}[*] Done!${reset}\n"
        clear_screen
    elif [ $(dpkg-query -W -f='${Status}' wine 2>/dev/null | grep -c "ok installed") -eq 1 ];
    then
        printf "${green}[*] Wine found. Setting it up...${reset}\n"
        sleep 3
    fi

    if [ ! -d "/tmp/cheesyrat" ];
    then
        mkdir /tmp/cheesyrat
    fi
    dpkg --add-architecture i386
    winecfg
    printf "${green}[*] Finished setting up wine. Setting up python for wine now...${reset}\n\n"
    sleep 3
    clear_screen
}

python_setup_wine () {
    printf "${green}[*] Installing and setting up python for wine. ${orange}This may take a while...${reset}\n"
    printf "${green}[*] For this python installation, please select ${white}Add Python 3.8 to PATH${reset}\n\n"
    sleep 5

    cd /tmp/cheesyrat
    wget "https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe"
    wine "python-3.8.0-amd64.exe"

    clear_screen
    printf "${orange}[!] We will run the installation script again for you. WHEN PROMPTED, PLEASE CLICK ${white}Repair${orange} this time${reset}\n"
    sleep 10
    wine "python-3.8.0-amd64.exe"

    clear_screen
    printf "${green}[*] Wine Python installation done.${reset}\n"
    printf "${green}[*] Continuing with wine pip installation....${reset}\n\n"
    sleep 4
}

pip_setup () {
    wine pip install pyinstaller
}

done_setup () {
    clear_screen
    printf "${green}[*] Finishing and cleaning up...${reset}"
    sleep 3
    cd ~
    if [ -d "/tmp/cheesyrat/" ];
    then
        rm -r /tmp/cheesyrat/
    fi
    clear_screen
    banner "Finished setup"
    printf "\n\n${green}[*] Finished setup for cheesyrat. You can now run ${white}cheesyrat${green} anywhere in the terminal to start the framework.${reset}\n\n"
    exit
}

main
