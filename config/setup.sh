#!/bin/bash

## Global variables
BOLD="\033[01;01m"     # Highlight
RED="\033[01;31m"      # Issues/Errors
GREEN="\033[01;32m"    # Success
YELLOW="\033[01;33m"   # Warnings/Information
RESET="\033[00m"       # Normal

os="$( awk -F '=' '/^ID=/ {print $2}' /etc/os-release 2>&- )"

if [ "${os}" == "arch" ] \
|| [ "${os}" == "blackarch" ] \
|| [ "${os}" == "debian" ] \
|| [ "${os}" == "deepin" ] \
|| [ "${os}" == "elementary" ] \
|| [ "${os}" == "kali" ] \
|| [ "${os}" == "linuxmint" ] \
|| [ "${os}" == "\"void\"" ] \
|| [ "${os}" == "ubuntu" ]; then
  trueuser="$( who | tr -d '\n' | cut -d' ' -f1 )"
else
  ## If this is blank, we're actually root
  trueuser="$( who am i | cut -d' ' -f1 )"
fi

## If this is blank, we're actually root
if [ "${trueuser}" == "" ]; then
  trueuser="root"
fi

if [ "${trueuser}" != "root" ]; then
  userhomedir="$( echo /home/${trueuser} )"
else
  userhomedir="${HOME}"
fi

userprimarygroup="$( id -Gn "${trueuser}" | cut -d' ' -f1 )"
arch="$( uname -m )"
if [ "${os}" == "\"void\"" ]; then
  osversion="$(uname -r)"
else
  osversion="$( awk -F '=' '/^VERSION_ID=/ {print $2}' /etc/os-release 2>&- | sed 's/"//g' )"
fi
if [ "${os}" == "\"void\"" ]; then
  osmajversion="$(uname -a | cut -f3 -d\ | cut -f-2 -d.)"
else
  osmajversion="$( awk -F '["=]' '/^VERSION_ID=/ {print $3}' /etc/os-release 2>&- | cut -d'.' -f1 )"
fi

cheesyratdir="/var/lib/cheesyrat"
outputdir="${cheesyratdir}/output"
dependenciesdir="${cheesyratdir}/setup-dependencies"
rootdir=$( cd "$( dirname "${BASH_SOURCE[0]}" )/../" && pwd )
winedir="${cheesyratdir}/wine"
winedrive="${winedir}/drive_c"
replace="\\"
prefix="Z:"
nukewinedir=""
silent=false
force=false
arg=""
errors=""

## ====================================================================
## END OF GLOBAL VARIABLES
## ====================================================================

func_title(){
  echo " =========================================================================="
  echo "              Cheesyrat (Setup Script) | [Updated]: 11-26-2019"
  echo " =========================================================================="
  echo "                   https://github.com/kyryloren/cheesyrat"
  echo " =========================================================================="
  echo ""
  echo "                    os = ${os}"
  echo "             osversion = ${osversion}"
  echo "          osmajversion = ${osmajversion}"
  echo "                  arch = ${arch}"
  echo "              trueuser = ${trueuser}"
  echo "      userprimarygroup = ${userprimarygroup}"
  echo "           userhomedir = ${userhomedir}"
  echo "               rootdir = ${rootdir}"
  echo "          cheesyratdir = ${cheesyratdir}"
  echo "             outputdir = ${outputdir}"
  echo "       dependenciesdir = ${dependenciesdir}"
  echo "               winedir = ${winedir}"
  echo "             winedrive = ${winedrive}"
  echo ""
}

function ctrl_c() {
  echo -e "\n\n${RED}Quitting...${RESET}\n"
  exit 2
}

func_check_env() {
    ## We check if sudo package is installed. If not, we don't continue
    which sudo >/dev/null 2>&-
    if [ "$?" -ne "0" ]; then
      echo ""
      echo -e " ${RED}[ERROR]: This setup script requires sudo!${RESET}"
      echo -e " ${YELLOW}         Please install and configure sudo then run this setup again.${RESET}"
      echo -e " ${YELLOW}         Example: For Debian/Ubuntu: apt-get install -y sudo${RESET}"
      echo -e " ${YELLOW}                  For Fedora 22+: dnf -y install sudo${RESET}"
      exit 1
    fi

    ## Feedback to user
    [ "${silent}" == "true" ] && echo -e "[*] ${YELLOW}Silent Mode${RESET}: ${GREEN}Enabled${RESET}"
    [ "${force}" == "true" ] &&  echo -e "[*]  ${YELLOW}Force Mode${RESET}: ${GREEN}Enabled${RESET}"

    ## Double check install (if not silent)
    echo -e "\n\n[!] ${BOLD}Are you sure you wish to install cheesyrat?${RESET}\n"
    echo -en "Continue with installation? ([${BOLD}y${RESET}]es/[${BOLD}s${RESET}]ilent/[${BOLD}n${RESET}]o): "
    if [ "${silent}" == "true" ]; then
      echo -e "${GREEN}S${RESET}\n"
    else
      read -p '' install
      install=$(echo "${install}" | tr '[:upper:]' '[:lower:]')
      echo

      if [ "${install}" == 's' ] || [ "${install}" == 'silent' ]; then
        silent=true
      elif [ "${install}" != 'y' ] && [ "${install}" != 'yes' ]; then
        echo -e "\n\n${RED}[ERROR]: Installation aborted by user${RESET}\n"
        exit 1
      fi
    fi

    ## Install architecture dependent dependencies
    func_package_deps

    ## Check if (Wine) Python is already installed
    if [ "${force}" == "false" ] && [ -f "${winedrive}/Python34/python.exe" ] && [ -f "${winedrive}/Python34/DLLs/python3.dll" ] \
    && [ -f "${winedrive}/Python34/Lib/site-packages/win32/win32api.pyd" ]; then
      echo -e "\n\n[*] ${YELLOW}(Wine) Python is already installed... Skipping...${RESET}\n"
    else
      func_python_deps
    fi

    ## Finally, update the config
    if [ "${force}" == "false" ] && [ -f "/etc/cheesyrat/settings.py" ] && [ -d "${outputdir}" ]; then
      echo -e "\n\n[*] ${YELLOW}Settings already detected... Skipping...${RESET}\n"
    else
      func_update_config
    fi

    ## Function done
    echo -e "\n\n[*] ${YELLOW}Finished environment checks${RESET}\n"
}

## Install architecture dependent dependencies
func_package_deps(){
  echo -e "\n\n[*] ${YELLOW}Initializing package installation${RESET}\n"

  ## Start dependency install
  echo -e "\n\n[*] ${YELLOW}Installing dependencies${RESET}\n"
  if [ "${os}" == "debian" ] \
  || [ "${os}" == "deepin" ] \
  || [ "${os}" == "kali" ] \
  || [ "${os}" == "linuxmint" ] \
  || [ "${os}" == "parrot" ] \
  || [ "${os}" == "ubuntu" ]; then
    ## Silent mode?
    [ "${silent}" == "true" ] && arg=" DEBIAN_FRONTEND=noninteractive" || arg=""

    ## Update APT
    echo -e "[*] ${YELLOW}Updating APT${RESET}\n"
    sudo apt-get -qq update
    if [[ "$?" -ne "0" ]]; then
      msg="Failed with apt-get update (1): $?"
      errors="${errors}\n${msg}"
      echo -e " ${RED}[ERROR] ${msg}${RESET}\n"
    fi

    # sudo                   - its everywhere
    # unzip                  - used for de-compressing files during setup
    # git                    - used for setup and keeping up-to-date
    # python3-*              - python payloads
    sudo ${arg} apt-get install -y sudo unzip git python3
    if [[ "$?" -ne "0" ]]; then
      msg="Failed with installing dependencies (1): $?"
      errors="${errors}\n${msg}"
      echo -e "${RED}[ERROR] ${msg}${RESET}\n"
    fi

    if [ "${os}" == "debian" ] || [ "${os}" == "kali" ] || [ "${os}" == "parrot" ]; then
      echo -e "\n\n[*] ${YELLOW}Installing Python's pycrypto (via apt)...${RESET}\n"
      sudo ${arg} apt-get install -y python3-crypto
      if [[ "$?" -ne "0" ]]; then
        msg="Failed with installing dependencies (6): $?"
        errors="${errors}\n${msg}"
        echo -e "${RED}[ERROR] ${msg}${RESET}\n"
      fi
    else
      echo -e "\n\n[*] ${YELLOW}Installing Python's pycrypto (via pip3)...${RESET}\n"
      sudo ${arg} apt-get install -y python3-pip
      if [[ "$?" -ne "0" ]]; then
        msg="Failed with installing dependencies (7): $?"
        errors="${errors}\n${msg}"
        echo -e "${RED}[ERROR] ${msg}${RESET}\n"
      fi

      pip3 install pycrypto
      if [[ "$?" -ne "0" ]]; then
        msg="Failed with installing pip3 (1): $?"
        errors="${errors}\n${msg}"
        echo -e "${RED}[ERROR] ${msg}${RESET}\n"
      fi
    fi

  elif [ "${os}" == "void" ]; then
    ## Update XBPS
    echo -e "[*] ${YELLOW}Updating XBPS${RESET}\n"
    sudo xbps-install -Suy
    if [[ "$?" -ne "0" ]]; then
      msg="Failed with xbps-install -Suy (1): $?"
      echo -e "${RED}[ERROR] ${msg}${RESET}\n"
    fi
    sudo xbps-install -uy sudo unzip git python3
    if [[ "$?" -ne "0" && "$?" -ne "6" ]]; then
      if grep -v "up to date"; then
        msg="Failed with installing dependencies (1): $?"
        errors="${errors}\n${msg}"
        echo -e "${RED}[ERROR] ${msg}${RESET}\n"
      fi
    fi
    echo -e "\n\n[*] ${YELLOW}Installing Python's pycrypto (via pip3)...${RESET}\n"
    sudo xbps-install -uy python3-pip
    if [[ "$?" -ne "0" && "$?" -ne "6" ]]; then
      if grep -v "up to date"; then
        msg="Failed with installing dependencies (8): $?"
        errors="${errors}\n${msg}"
        echo -e "${RED}[ERROR] ${msg}${RESET}\n"
      fi
    fi
    sudo pip3 install pycrypto
    if [[ "$?" -ne "0" ]]; then
      if grep -vq "already satisfied"; then
        msg="Failed with installing pip3 (1): $?"
        errors="${errors}\n${msg}"
        echo -e "${RED}[ERROR] ${msg}${RESET}\n"
      fi
    fi

  elif [ "${os}" == "elementary" ]; then
    ## Silent mode?
    [ "${silent}" == "true" ] && arg=" DEBIAN_FRONTEND=noninteractive" || arg=""

    ## Update APT
    echo -e "[*] ${YELLOW}Updating APT${RESET}\n"
    sudo apt-get -qq update
    if [[ "$?" -ne "0" ]]; then
      msg="Failed with apt-get update (2): $?"
      errors="${errors}\n${msg}"
      echo -e "${RED}[ERROR] ${msg}${RESET}\n"
    fi

    sudo ${arg} apt-get install -y unzip wget git python python-crypto python-pefile python-pip python3-pip winbind python3-crypto
    if [[ "$?" -ne "0" ]]; then
      msg="Failed with installing dependencies (2): $?"
      errors="${errors}\n${msg}"
      echo -e "${RED}[ERROR] ${msg}${RESET}\n"
    fi

  elif [ "${os}" == "centos" ] || [ "${os}" == "fedora" ] || [ "${os}" == "rhel" ]; then
    sudo ${arg} dnf -y install unzip wget git python python-crypto python-pefile python-pip ca-certificates python3-pip winbind
    if [[ "$?" -ne "0" ]]; then
      msg="Failed with installing dependencies (3): $?"
      errors="${errors}\n${msg}"
      echo -e "${RED}[ERROR] ${msg}${RESET}\n"
    fi

  elif [ "${os}" == "blackarch" ]; then
    sudo pacman -Sy ${arg} --needed python2-pip wget unzip python python2 python-crypto ca-certificates python-pip 
    if [[ "$?" -ne "0" ]]; then
      msg="Failed with installing dependencies (4): $?"
      errors="${errors}\n${msg}"
      echo -e "${RED}[ERROR] ${msg}${RESET}\n"
    fi

    ## Install pefile for python2 using pip, rather than via AUR as the package is currently broken.
    sudo pip2 install pefile
    if [[ "$?" -ne "0" ]]; then
      msg="Failed with pip2 install (1): $?"
      errors="${errors}\n${msg}"
      echo -e "${RED}[ERROR] ${msg}${RESET}\n"
    fi

  elif [ "${os}" == "arch" ]; then
    AUR_packages()
    {
      if [ $1 == 'yay' ]; then
        if [ "${silent}" == true ]; then
          yay -S mingw-w64-binutils mingw-w64-crt mingw-w64-gcc mingw-w64-headers mingw-w64-winpthreads --noconfirm
        else
          yay -S mingw-w64-binutils mingw-w64-crt mingw-w64-gcc mingw-w64-headers mingw-w64-winpthreads
        fi
      elif [ $1 == 'yaourt' ]; then
        if [ "${silent}" == true ]; then
          yaourt -S mingw-w64-binutils mingw-w64-crt mingw-w64-gcc mingw-w64-headers mingw-w64-winpthreads --noconfirm
        else
          yaourt -S mingw-w64-binutils mingw-w64-crt mingw-w64-gcc mingw-w64-headers mingw-w64-winpthreads
        fi
      fi
    }
    sudo pacman -Sy ${arg} --needed python2-pip wget unzip ruby python python-crypto gcc-go ca-certificates python-pip
    if [ $(id -u) -eq 0 ]; then
      echo "\n\n Insert your non-root user:\n"
      read $nonrootuser
      su - $nonrootuser
    fi
    if pacman -Qs yay > /dev/null ; then
      AUR_packages "yay"
    elif pacman -Qs yaourt > /dev/null ; then
      AUR_packages "yaourt"
    else
      git clone https://aur.archlinux.org/yay.git ~/Downloads/yay
      makepkg -si ~/Downloads/yay
      rm -rf ~/Downloads/yay
      sudo pacman -Syyu
      AUR_packages "yay"
      echo -e "\n\n[*]${BOLD}Yay has been installed to install some dependencies.${RESET}\n"
      echo -en "     Do you want to keep yay installed? ([${BOLD}y${RESET}]es/[${BOLD}s${RESET}]ilent/[${BOLD}N${RESET}]o): "
      
      if [ "${keepyay} == 'y'" ] || [ "${keepyay} == 'yes'" ]; then
        echo -e "\n\n${GREN}yay will remain installed on your system. \n"
      elif [ "${install}" == 'n' ] || [ "${install}" == 'no' ]; then
        echo -e "\n\n${RED}yay will be removed from your system.\n"
        sudo pacman -Rns yay
      fi
    fi

    ## Install pefile for python2 using pip, rather than via AUR as the package is currently broken.
    sudo pip2 install pefile
    if [[ "$?" -ne "0" ]]; then
      msg="Failed with pip2 install (1): $?"
      errors="${errors}\n${msg}"
      echo -e "${RED}[ERROR] ${msg}${RESET}\n"
    fi
  fi


  ## Clone down the required install files
  echo -e "\n\n[*] ${YELLOW}Pulling down binary dependencies${RESET}\n"
  [ "${force}" == "true" ] && rm -rf "${dependenciesdir}"
  ## Pulling down from github, if it fails, pull local folder
  if [ -d "${dependenciesdir}" ]; then
    echo -e "[*] ${YELLOW}Already detected folder: ${BOLD}${dependenciesdir}${RESET}\n"
    echo -e "[*] ${YELLOW}Trying to git pull${RESET}\n"
    pushd "${dependenciesdir}" >/dev/null
    sudo git reset --hard HEAD >/dev/null
    sudo git clean -fd >/dev/null
    sudo git pull
    if [[ "$?" -ne "0" ]]; then
      msg="Failed with git pull: $?"
      errors="${errors}\n${msg}"
      echo -e " ${RED}[ERROR] ${msg}${RESET}\n"
    fi
    popd >/dev/null
  else
    echo -e "[*] ${YELLOW}Empty folder... git cloning${RESET}\n"
    sudo mkdir -p "${dependenciesdir}"
    sudo rm -rf "${dependenciesdir}"
    sudo git clone https://github.com/kyryloren/cheesyrat-dependencies.git "${dependenciesdir}"
    if [[ "$?" -ne "0" ]]; then
      msg="Failed with git clone: $?"
      errors="${errors}\n${msg}"
      echo -e " ${RED}[ERROR] ${msg}${RESET}\n"
    fi
  fi


  ## Begin Wine install for multiple architectures
  ## Always install 32-bit support for 64-bit architectures
  ## <wine>
  echo -e "\n\n[*] ${YELLOW}Installing Wine${RESET}\n"


  ## Debian based distributions
  if [ "${os}" == "debian" ] \
  || [ "${os}" == "deepin" ] \
  || [ "${os}" == "kali" ] \
  || [ "${os}" == "linuxmint" ] \
  || [ "${os}" == "parrot" ] \
  || [ "${os}" == "ubuntu" ]; then
    ## Silent mode?
    [ "${silent}" == "true" ] \
      && arg=" DEBIAN_FRONTEND=noninteractive" \
      || arg=""

      if [ "${arch}" == "x86_64" ]; then
        ## Check to see if we already have i386
        tmp="$( dpkg --print-foreign-architectures | grep '^i386$' )"

        ## If we do NOT have it, add it
        if [[ "${tmp}" == "" ]]; then
          echo -e "\n\n[*] ${YELLOW}Adding i386 architecture to x86_64 system for Wine${RESET}\n"
          sudo dpkg --add-architecture i386

          echo -e "[*] ${YELLOW}Updating APT${RESET}\n"
          sudo apt-get -qq update
          if [[ "$?" -ne "0" ]]; then
            msg="Failed with apt-get update (3): $?"
            errors="${errors}\n${msg}"
            echo -e "${RED}[ERROR] ${msg}${RESET}\n"
          fi
        ## Already have i386 added
        else
          echo -e "[*] ${YELLOW}Already have x86 architecture added...${RESET}\n"
        fi
      echo -e "\n\n[*] ${YELLOW}Installing Wine 32-bit and 64-bit binaries (via APT)${RESET}\n"
      if [ "${os}" == "ubuntu" ] \
      || [ "${os}" == "linuxmint" ]; then
        ## Special urghbuntu derivative snowflakes. Now with even *more* special.
        if [ "${osmajversion}" -ge "17" ] \
        && [ "${os}" == "ubuntu" ]; then
          # Wine package was renamed in Arty
          sudo ${arg} apt-get -y -qq install wine-stable
                    else
          sudo ${arg} apt-get -y -qq install wine wine1.6 wine1.6-i386
                    fi
        if [[ "$?" -ne "0" ]]; then
          msg="Failed with installing wine (1): $?"
          errors="${errors}\n${msg}"
          echo -e "${RED}[ERROR] ${msg}${RESET}\n"
        fi
      else
        ## Anything that isn't ubuntu or ubuntu-derived
        sudo ${arg} apt-get -y -qq install wine wine64 wine32
        if [[ "$?" -ne "0" ]]; then
          msg="Failed with installing wine (2): $?"
          errors="${errors}\n${msg}"
          echo -e "${RED}[ERROR] ${msg}${RESET}\n"
        fi
      fi
    elif [ "${arch}" == "x86" ] \
    || [ "${arch}" == "i686" ]; then
      sudo apt-get -qq update
      if [[ "$?" -ne "0" ]]; then
        msg="Failed with apt-get update (4): $?"
        errors="${errors}\n${msg}"
        echo -e "${RED}[ERROR] ${msg}${RESET}\n"
      fi

      sudo ${arg} apt-get -y -qq install wine32
      if [[ "$?" -ne "0" ]]; then
        msg="Failed with installing wine (3): $?"
        errors="${errors}\n${msg}"
        echo -e "${RED}[ERROR] ${msg}${RESET}\n"
      fi
    else
      ## Dead code. We really shouldn't end up here, but, you never know...
      echo -e "${RED}[ERROR]: Architecture ${arch} is not supported!\n${RESET}\n"
      exit 1
    fi

  ## Elementary OS x86_64
  elif [ "${os}" == '"elementary"' ]; then
    echo -e "\n\n[*] ${YELLOW}Installing Wine on Elementary OS (via APT)${RESET}\n"
    sudo ${arg} apt-get -y -qq install wine wine1.6 wine1.6-amd64
    if [[ "$?" -ne "0" ]]; then
      msg="Failed with installing wine (4): $?"
      errors="${errors}\n${msg}"
      echo -e "${RED}[ERROR] ${msg}${RESET}\n"
    fi

  ## Red Hat based distributions
  elif [ "${os}" == "fedora" ] || [ "${os}" == "rhel" ] || [ "${os}" == "centos" ]; then
    echo -e "\n\n[*] ${YELLOW}Installing Wine 32-bit on x86_64 System (via DNF)${RESET}\n"
    sudo dnf install -y wine.i686 wine
    if [[ "$?" -ne "0" ]]; then
      msg="Failed with installing wine (5): $?"
      errors="${errors}\n${msg}"
      echo -e "${RED}[ERROR] ${msg}${RESET}\n"
    fi
  elif [ "${os}" == "arch" ] || [ "${os}" == "blackarch" ]; then
    echo -e "\n\n[*] ${YELLOW}Installing Wine 32-bit on x86_64 System (via PACMAN)${RESET}\n"
    if grep -Fxq "#[multilib]" /etc/pacman.conf; then
      echo "[multilib]\nInclude = /etc/pacman.d/mirrorlist" >> /etc/pacman.conf
    fi

    sudo pacman -Syu ${args} --needed --noconfirm wine wine-mono wine_gecko git
    if [[ "$?" -ne "0" ]]; then
      msg="Failed with installing wine (6): $?"
      errors="${errors}\n${msg}"
      echo -e "${RED}[ERROR] ${msg}${RESET}\n"
    fi

  ## Void Linux
  elif [ "${os}" == '"void"' ]; then
    sudo xbps-install -uy wine-32bit wine-mono wine-gecko
    if [[ "$?" -ne "0" ]]; then
      if grep -v "up to date"; then
        msg="Failed with installing wine (7): $?"
        errors="${errors}\n${msg}"
        echo -e "{RED}[ERROR] ${msg}${RESET}\n"
      fi
    fi
  fi

  if [ -d "${winedir}" ]; then
    echo -e "\n\n[*] ${BOLD}[ALERT]${RESET}: Existing Cheesyrat Wine environment detected at: ${BOLD}${winedir}${RESET}\n"
    echo -en "     Do you want to nuke it? ([${BOLD}y${RESET}]es/[${BOLD}N${RESET}]o): "
    if [ "${silent}" == "true" ]; then
      echo -e "${GREEN}Y${RESET}\n"
    else
      read -p '' nukewinedir
      nukewinedir=$(echo "${nukewinedir}" | tr '[:upper:]' '[:lower:]')
      echo
    fi

    if [ "${nukewinedir}" == 'y' ] || [ "${nukewinedir}" == 'yes' ] || [ "${silent}" == 'true' ]; then
      echo -e "[*] ${YELLOW}Deleting existing Cheesyrat Wine environment...${RESET}\n"
      sudo rm -rf "${winedir}"
    else
      echo -e "[*] ${YELLOW}Maintaining current Cheesyrat Wine environment...${RESET}\n"
    fi
  fi


  ## For creating wine environment on newer distros
  if [ -f "/usr/bin/wineboot" ]; then
    winebootexists=true
    sudo mkdir -p "${winedrive}/"
    sudo chown -R "${trueuser}:" "${winedir}"
  else
    winebootexists=false
  fi


  if [ ! -d "${winedir}" ] || [ "${nukewinedir}" == 'y' ] || [ "${nukewinedir}" == 'yes' ] || [ "${silent}" == 'true' ]; then
    echo -e "[*] ${YELLOW}Creating new Cheesyrat Wine environment in: ${BOLD}${winedir}${RESET}\n"

    echo -e "[*] ${YELLOW}Initializing the Cheesyrat Wine environment...${RESET}\n"
    ## x64
    if [ "${arch}" == "x86_64" ]; then
      ## First time running wine, need to run a dummy file to create files
      [ "${winebootexists}" == "true" ] \
        && sudo -u "${trueuser}" WINEARCH=win32 WINEPREFIX="${winedir}" wineboot -u \
        || sudo -u "${trueuser}" WINEARCH=win32 WINEPREFIX="${winedir}" wine cmd.exe /c ipconfig >/dev/null
    ## x86
    elif [ "${arch}" == "x86" ] \
    || [ "${arch}" == "i686" ]; then
      sudo -u "${trueuser}" WINEPREFIX="${winedir}" wineboot -u
    fi

    if [ -d "${winedrive}" ]; then
      echo -e "[*] ${GREEN}Cheesyrat Wine environment successfully created!${RESET}\n"
    else
      msg="Cheesyrat Wine environment could not be found!"
      errors="${errors}\n${msg}"
      echo -e "${RED}[ERROR] ${msg}${RESET}\n"

      msg="Check for existence of ${winedrive}"
      errors="${errors}\n${msg}"
      echo -e "${RED}[ERROR] ${msg}${RESET}\n"
    fi
  fi

  ## Function done
  echo -e "\n\n[*] ${YELLOW}Finished package installation${RESET}\n"
}

## Install Python dependencies
func_python_deps(){
  ## Banner
  echo -e "\n\n[*] ${YELLOW}Initializing (OS + Wine) Python dependencies installation...${RESET}\n"

  ## Python (OS) - install-addons.sh
  ## In-case its 'First time run' for Wine (More information - http://wiki.winehq.org/Mono)
  #[[ "${silent}" == "true" ]] && bash "${dependenciesdir}/install-addons.sh"   #wget -qO - "http://winezeug.googlecode.com/svn/trunk/install-addons.sh"

  ## Install (Wine) Python main setup file
  echo -e "\n\n[*] ${YELLOW}Installing (Wine) Python...${RESET}\n"
  echo -e "[*] ${BOLD} Next -> Next -> Next -> Finished! ...Overwrite if prompt (use default values)${RESET}\n"
  sleep 1s

  [ "${silent}" == "true" ] \
    && arg=" TARGETDIR=C:\Python34 ALLUSERS=1 /q /norestart" \
    || arg=""
  sudo -u "${trueuser}" WINEPREFIX="${winedir}" wine msiexec /i "${dependenciesdir}/python-3.4.4.msi" ${arg}
  tmp="$?"
  if [[ "${tmp}" -ne "0" ]]; then
    msg="Failed to install (Wine) Python 3.4.4... Exit code: ${tmp}"
    errors="${errors}\n${msg}"
    echo -e "${RED}[ERROR] ${msg}${RESET}\n"
  fi

  ## Cool down
  sleep 3s

  ## Banner
  echo -e "\n\n[*] ${YELLOW}Installing (Wine) Python dependencies...${RESET}\n"
  pushd "${dependenciesdir}/" >/dev/null

  ## Install (Wine) Python extra setup files (PyWin32 & PyCrypto)
  for FILE in pywin32-220.win32-py3.4.exe pycrypto-2.6.1.win32-py3.4.exe; do
    echo -e "\n\n[*] ${YELLOW}Installing (Wine) Python's ${FILE}...${RESET}\n"
    echo -e "[*] ${BOLD} Next -> Next -> Next -> Finished! ...Overwrite if prompt (use default values)${RESET}\n"
    sleep 1s

    if [ "${silent}" == "true" ]; then
      ## Start fresh
      sudo rm -rf "PLATLIB/" "SCRIPTS/"
      ## Extract
      sudo unzip -q -o "${FILE}"
      ## Copy files to right location
      [ -e "PLATLIB" ] && sudo -u "${trueuser}" cp -rf PLATLIB/* "${winedrive}/Python34/Lib/site-packages/"
      [ -e "SCRIPTS" ] && sudo -u "${trueuser}" cp -rf SCRIPTS/* "${winedrive}/Python34/Scripts/"
      ## Run post install file
      [ -e "SCRIPTS/pywin32_postinstall.py" ] && sudo -u "${trueuser}" WINEPREFIX="${winedir}" wine "${winedir}/drive_c/Python34/python.exe" "${winedrive}/Python34/Scripts/pywin32_postinstall.py" "-silent" "-quiet" "-install" >/dev/null
      ## Due to pycrypto-2.6.1.win32-py3.4.exe not exacting cleaning, this will falsely trigger
      #tmp="$?"
      #if [[ "${tmp}" -ne "0" ]]; then
      #  msg="Failed to install ${FILE}... Exit code: ${tmp}"
      #  errors="${errors}\n${msg}"
      #  echo -e " ${RED}[ERROR] ${msg}${RESET}\n"
      #fi
      ## Clean up
      sudo rm -rf "PLATLIB/" "SCRIPTS/"
    else
      sudo -u "${trueuser}" WINEPREFIX="${winedir}" wine "${FILE}"
      tmp="$?"
      if [[ "${tmp}" -ne "0" ]]; then
        msg="Failed to install ${FILE}... Exit code: ${tmp}"
        errors="${errors}\n${msg}"
        echo -e "${RED}[ERROR] ${msg}${RESET}\n"
      fi
    fi
  done

  popd >/dev/null

  ## Install Python (OS) extra setup files (PyInstaller)
  echo -e "\n\n[*] ${YELLOW}Installing (OS) Python's PyInstaller (via TAR)${RESET}\n"
  if [ "${force}" == "false" ] \
  && [ -f "${cheesyratdir}/PyInstaller-3.2.1/pyinstaller.py" ]; then
    echo -e "\n\n[*] ${YELLOW}PyInstaller v3.2 is already installed... Skipping...${RESET}\n"
  else
    ## Install PyInstaller now
    file="${dependenciesdir}/PyInstaller-3.2.1.tar"
    shasum="$( openssl dgst -sha256 "${file}" | cut -d' ' -f2 )"
    if [ "${shasum}" == "4727314ddf95bfe4aed28b3b98e0175d469a36aff5eb7e2af3c3d2fffd662d2d" ]; then
      sudo rm -rf "${cheesyratdir}/PyInstaller-*"
      sudo mkdir -p "${cheesyratdir}"
      sudo tar -C "${cheesyratdir}" -xf "${file}"
    else
      msg="Bad hash for PyInstaller.tar.gz!"
      errors="${errors}\n${msg}"
      echo -e "${RED}[ERROR] ${msg}${RESET}\n"
    fi
  fi

  ## Use wine based pip to install dependencies
  echo -e "\n\n[*] ${YELLOW}Installing (Wine) Python's PIP pefile${RESET}\n"
  sudo -u "${trueuser}" WINEPREFIX="${winedir}" wine "${winedir}/drive_c/Python34/python.exe" "-m" "pip" "install" "--upgrade" "pip"
  tmp="$?"
  if [[ "${tmp}" -ne "0" ]]; then
    msg="Failed to run (wine) Python pip... Exit code: ${tmp}"
    errors="${errors}\n${msg}"
    echo -e "${RED}[ERROR] ${msg}${RESET}\n"
  fi

  sudo -u "${trueuser}" WINEPREFIX="${winedir}" wine "${winedir}/drive_c/Python34/python.exe" "-m" "pip" "install" "future"
  tmp="$?"
  if [[ "${tmp}" -ne "0" ]]; then
    msg="Failed to run (wine) Python pip future... Exit code: ${tmp}"
    errors="${errors}\n${msg}"
    echo -e "${RED}[ERROR] ${msg}${RESET}\n"
  fi

  sudo -u "${trueuser}" WINEPREFIX="${winedir}" wine "${winedir}/drive_c/Python34/python.exe" "-m" "pip" "install" "pefile"
  tmp="$?"
  if [[ "${tmp}" -ne "0" ]]; then
    msg="Failed to run (wine) Python pip pefile... Exit code: ${tmp}"
    errors="${errors}\n${msg}"
    echo -e "${RED}[ERROR] ${msg}${RESET}\n"
  fi


  ## Function done
  echo -e "\n\n[*] ${YELLOW}Finished (Wine + OS) Python dependencies installation${RESET}\n"
}

## Update Cheesyrat config
func_update_config(){
  echo -e "\n\n[*] ${YELLOW}Updating Cheesyrat configuration...${RESET}\n"
  cd "${rootdir}/config/"

  if [ -e /etc/cheesyrat/ ]; then
    echo -e "[*] ${YELLOW}Detected current Cheesyrat settings. Removing...${RESET}\n"
    sudo rm -rf /etc/cheesyrat/
  fi
  chmod +x config-update.py
  sudo -u "${trueuser}" sudo ./config-update.py
  pwd

  sudo mkdir -p "${outputdir}"

  ## Chown output directory
  if [ -d "${outputdir}" ]; then
    echo -e "\n\n[*] ${YELLOW}Ensuring this account (${trueuser}) owns cheesyrat output directory (${outputdir})...${RESET}\n"
    sudo chown -R "${trueuser}" "${outputdir}"
  else
    msg="Internal Issue. Couldn't create output folder..."
    errors="${errors}\n${msg}"
    echo -e " ${RED}[ERROR] ${msg}${RESET}\n"
  fi

  ## Ensure that user completely owns the wine directory
  echo -e "[*] ${YELLOW}Ensuring this account (${trueuser}) has correct ownership of ${winedir}${RESET}\n"
  sudo chown -R "${trueuser}":"${userprimarygroup}" "${winedir}"


  ## Function done
  echo -e "\n\n[*] ${YELLOW}Finished Cheesyrat configuration...${RESET}\n"
}


## Print banner
func_title


## Check architecture
if [ "${arch}" != "x86" ] \
&& [ "${arch}" != "i686" ] \
&& [ "${arch}" != "x86_64" ]; then
  echo -e " ${RED}[ERROR] Your architecture ${arch} is not supported!${RESET}\n\n"
  exit 1
fi


## Check OS
if [ "${os}" == "\"void\"" ]; then
  echo -e "[*] ${YELLOW}Void Linux ${osversion} ${arch} detected...${RESET}\n"
elif [ "${os}" == "kali" ]; then
  echo -e "[*] ${YELLOW}Kali Linux ${osversion} ${arch} detected...${RESET}\n"
elif [ "${os}" == "parrot" ]; then
  echo -e "[*] ${YELLOW}Parrot Security ${osversion} ${arch} detected...${RESET}\n"
elif [ "${os}" == "ubuntu" ]; then
  echo -e "[*] ${YELLOW}Ubuntu ${osversion} ${arch} detected...${RESET}\n"
  if [[ "${osmajversion}" -lt "15" ]]; then
    echo -e "${RED}[ERROR]: Veil is only supported On Ubuntu 15.10 or higher!${RESET}\n"
    exit 1
  fi
elif [ "${os}" == "linuxmint" ]; then
  echo -e "[*] ${YELLOW}Linux Mint ${osversion} ${arch} detected...${RESET}\n"
elif [ "${os}" == "deepin" ]; then
  echo -e "[*] ${YELLOW}Deepin ${osversion} ${arch} detected...${RESET}\n"
  if [[ "${osmajversion}" -lt "15" ]]; then
    echo -e "${RED}[ERROR]: Veil is only supported On Deepin 15 or higher!${RESET}\n"
    exit 1
  fi
elif [ "${os}" == '"elementary"' ]; then
  echo -e "[*] ${YELLOW}Elementary OS ${osversion} ${arch} detected...${RESET}\n"
elif [ "${os}" == "debian" ]; then
  if [[ "${osmajversion}" -lt "8" ]]; then
    echo -e "${RED}[ERROR]: Veil is only supported on Debian 8 (Jessie) or higher!${RESET}\n"
    exit 1
  fi
elif [ "${os}" == "fedora" ]; then
  echo -e "[*] ${YELLOW}Fedora ${osversion} ${arch} detected...${RESET}\n"
  [[ -z "$osmajversion" ]] && osmajversion=$osversion
  if [[ "${osmajversion}" -lt "22" ]]; then
    echo -e "${RED}[ERROR]: Veil is only supported on Fedora 22 or higher!${RESET}\n"
    exit 1
  fi
else
  os="$( awk -F '["=]' '/^ID=/ {print $2}' /etc/os-release 2>&- | cut -d'.' -f1 )"
  if [ "${os}" == "arch" ]; then
    echo -e "[*] ${YELLOW}Arch Linux ${arch} detected...${RESET}\n"
  elif [ "${os}" == "blackarch" ]; then
    echo -e "[*] ${YELLOW}BlackArch Linux ${arch} detected...${RESET}\n"
  elif [ "${os}" == "debian" ]; then
    echo -e "[!] ${YELLOW}Debian Linux sid/TESTING ${arch} *possibly* detected..."
    echo -e "     If you are not currently running Debian Testing, you should exit this installer!${RESET}\n"
  else
    echo -e "${RED}[ERROR] Unable to determine OS information. Exiting...${RESET}\n"
    exit 1
  fi
fi




########################################################################
## Actual setup execution
########################################################################



## Trap ctrl-c
trap ctrl_c INT

## Menu case statement
while [[ "${#}" -gt 0 && ."${1}" == .-* ]]; do
  opt="${1}";
  shift;
  case "$(echo ${opt} | tr '[:upper:]' '[:lower:]')" in
    ## Make sure not to nag the user
    -s|--silent)
    silent=true
    ;;

    ## Force clean install of (Wine) Python dependencies
    ## Bypass environment checks (func_check_env) to force install dependencies
    -f|--force)
    force=true
    ;;

    ## Print help menu
    -h|--help)
    echo ""
    echo "  usage: ${0} [OPTIONS]"
    echo ""
    echo "  positional arguments:"
    echo ""
    echo "  -f, --force     Force install of any dependencies"
    echo "  -s, --silent    Automates the installation"
    echo "  -h. --help      Show this help menu"
    echo ""
    exit 0
    ;;

    ## Run standard setup
    "")
    ;;

    *)
    echo -e "\n\n${RED}[ERROR] Unknown option: ${BOLD}$1${RESET}\n"
    exit 1
    ;;
   esac
done


## Run setup, maybe with -f and/or -s
func_check_env


if [ "${errors}" != "" ]; then
  echo -e " ${RED}[ERROR] There was issues installing the following:${RESET}\n"
  echo -e " ${BOLD}${errors}${RESET}\n"
fi


file="./cheesyrat.py --setup"
echo -e "\n\n[*] ${BOLD}If you have any errors${RESET} running Cheesyrat, run: '${BOLD}${file}' and select the nuke the wine folder option${RESET}\n"

echo -e "\n\n[*] ${GREEN}Done!${RESET}\n"

touch /usr/bin/cheesyrat


exit 0

