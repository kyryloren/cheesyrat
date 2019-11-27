<h1 align="center">THIS PROJECT IS NOT OUT YET. PLEASE PRESS WATCH TO BE NOTIFIED FOR A FUTURE RELEASE</h1>

<p align="center">
  <img src="https://i.imgur.com/jCd2xsO.png">
</p>

<h1 align="center">cheesyrat framework</h1>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.4.0-brightgreen.svg">
  </a>
  <a href="https://github.com/kyryloren/cheesyrat/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/License-GNU-lightgrey.svg">
  </a>
  <a href="https://github.com/kyryloren/cheesyrat">
    <img src="https://img.shields.io/badge/Release-DEVELOPMENT-red.svg">
  </a>
    <a href="https://opensource.org">
    <img src="https://img.shields.io/badge/Open%20Source-%E2%9D%A4-brightgreen.svg">
  </a>
</p>

<p align="center">
  cheesyrat allow you to generate payloads and control someone's Windows computer remotley.
</p>

<p align="center">
  :books: This project was created only for learning purposes. I am not responsible for any damage that this causes.
</p>

## Description:
Cheesyrat is an easy tool used to generate a peristent backdoor for remote access to a Windows machine. This tool creates malware with custom coded payloads that can be then easily executed on a Windows machine. The malware that is created with this tool has a high ability to __bypass__ most present-day antivirus detection. This project is still a __work in progress__ so there is a high chance of multiple bugs.

## Features (to be expected) :key::
- [x] Script kiddie friendly
- [x] All windows shell and powershell commands
- [x] Persistent
- [x] Take screenshots of victim's computer
- [x] Download files
- [x] Upload files
- [x] View system information
- [x] Crash victim's PC
- [x] Lock victim's computer screen
- [x] Shutdowm or restart victim's computer
- [x] Retrieve stored web browser passwords, cookies, and accounts
- [x] Keylogger
- [x] More to be expected

## How to Install :arrow_down::
__Tested On:__ [![Kali)](https://www.google.com/s2/favicons?domain=https://www.kali.org/)](https://www.kali.org) **Kali Linux - Rolling Edition** and [![Ubuntu)](https://www.google.com/s2/favicons?domain=ubuntu.com)](https://www.ubuntu.com) **Ubuntu - Latest Version**

**NOTE**
- Installation must be done with superuser, AKA root. This is usually default on Kali Linux. If you know that your linux distribution needs sudo to run, please add the prefix ```sudo``` for all your commands to run as sudo, or change the roor user before beginning.
1. ```sudo git clone https://github.com/kyryloren/cheesyrat.git```
2. ```sudo cd cheesyrat/config/ && chmod +x ./setup.sh```
3. ```sudo ./setup.sh```

## How to Use :question::
1. ```cd cheesyrat/```
2. ```./cheesyrat.py [OPTIONS]```
2. Follow the on-screen intructions.
3. Type ```help``` for help

## Config files :pushpin::
- The files located in the ```/cheesyrat/config/``` directory are crucial for installing this framework correctly and are copied to ```/etc/cheesyrat/settings.py``` after proper execeution. The setup and config files include all the major dependencies needed for this project including Wine, Python, and certain pip packages.
- The ```setup.sh``` files has to modes to run on: silent and force. Neither one of these modes are mandatory and you may use either one as you wish.
```
--force ~ If something goes wrong, this will overwrite detecting any previous installs. Useful when there is a setup package update.
--silent ~ This will perform an unattended installation of everything, as it will automate all the steps, so there is no interaction for the user.
```

## Screenshots: COMING SOON


## Contact :email::
**dev@kyryloorlov.com**

## Bugs :beetle::
**Please submit any issues that you find

## Buy me a coffee <img src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg">
<p>
  <a href="https://www.buymeacoffee.com/kyryloren">
  </a>
</p>

## Credits:
- Logo icons made by www.flaticon.com from www.flaticon.com
- Code written by kyryloren with some help from stackoverflow ;p
