import os
import shutil
import urllib.request
import zipfile
import time

def get_highest_version(unprocessed_versions):
    versions = [ tuple(map(int, (v.split(".")))) for v in unprocessed_versions]
    return unprocessed_versions[versions.index(max(versions))]
    


def install_patch(rootfpath):
    print("Getting app version and installation path...")
    paths = [f.path for f in os.scandir(rootfpath) if f.is_dir() and (os.path.basename(os.path.normpath(f))).startswith("app-")]
    highest = get_highest_version([os.path.basename(os.path.normpath(f)).replace('app-', '') for f in paths])
    resources_folder = os.path.join(rootfpath, "app-" + highest, "resources")
    print("Found resources folder!" + resources_folder)
    if os.path.isdir(os.path.join(resources_folder, "app")):
        print("Deleting preexisting app folder...")
        shutil.rmtree(os.path.join(resources_folder, "app"))
    print("Downloading patch...")
    #retrieve patch from my own repo cause discord returns 403 error (you can compare the files https://cdn.discordapp.com/attachments/410788958277074944/821690118468272168/patch.zip.)
    urllib.request.urlretrieve("https://github.com/PreciousWarrior/WindowsBDPatcher/raw/main/patch.zip", os.path.join(resources_folder, "patch.zip"))
    print("Extracting patch...")
    with zipfile.ZipFile(os.path.join(resources_folder, "patch.zip"), "r") as zip_ref:
        zip_ref.extractall(resources_folder)
    print("Patch successfully installed.")
    print("Cleaning up...")
    os.remove(os.path.join(resources_folder, "patch.zip"))
    print("Restarting Discord...")
    os.system("TASKKILL /F /IM discord.exe")
    time.sleep(1)
    discordfp = os.path.join(rootfpath, "app-"+highest, "Discord.exe")
    os.system("start " + discordfp)

    




def main():
    intro= "This script will download and install the BetterDiscord Windows patch by DevilBro for people having problems with BD not working on the latest discord version. This patch works on Stable, PTB and Canary. \n\n BD Support Server-: https://discord.gg/0Tmfo5ZbOR8bKrMJ\n Patch (https://discord.com/channels/86004744966914048/119918741516451840/821728188383100929) by DevilBro#4401\n Script by IamPrecious#4508\n Prerequisites-: you need to have discord installed and open at least one time. \n\n"

    choice = input(intro + "Please enter your discord installation type. For most people, this will be stable. (Your installation type can be found all the way down in the settings!)\n 1-: Stable, \n 2-: PTB, \n 3-: Canary, \n 4-: Custom Location \n")

    try:
        int_choice = int(choice)
    except ValueError:
        return print("Please run the script again and enter a valid number corresponding to your installation.")
    
    if int_choice == 1:
        install_patch(os.path.join(os.getenv('LOCALAPPDATA'), "Discord"))
    elif int_choice == 2:
        install_patch(os.path.join(os.getenv('LOCALAPPDATA'), "DiscordPTB"))
    elif int_choice == 3:
        install_patch(os.path.join(os.getenv('LOCALAPPDATA'), "DiscordCanary"))
    elif int_choice == 4:
        path = input("Please enter the root discord installation path: ")
        install_patch(path)
    else:
        print("Please run the script again and enter a number between 1 and 4")

main()