# This script will copy files from a source directory (skyrim/Data folder) to two target directories: one for backups and preparing BSA files and one for source control (github)

# Code adapted from: https://gist.github.com/Sleepingwell/6070119

# QUICK REFERENCES to Python resources
# https://docs.python.org/2/library/shutil.html
# https://www.pythonforbeginners.com/os/python-the-shutil-module
# http://xahlee.info/python/python_path_manipulation.html

""" 
Check the sample mods_manifest_sample.json file.
Rename to mods_manifest.json before use.
- All paths should end with a separator ( Remember to escape \\ on Windows. )

"""

import re
import os
import os.path
import shutil
import fnmatch
import filecmp
import json
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

debug = False

def deployModGroup(mods_data, mod_group_name):
    deployMods(mods_data, mod_group_name,"all")


def deployMod(mods_data, mod_group_name, mod_name):
    deployMods(mods_data, mod_group_name, mod_name)


def deployAllMods(mods_data):
    deployMods(mods_data, "all","all")


def deployMods(mods_data, mod_group_name, mod_name):
    mod_group_list = mods_data["mod_groups"]
    mod_group_match = 0
    mod_match = 0

    for this_mod_group in mod_group_list:  
        # print(this_mod_group)

        if (mod_group_name=="all") or (mod_group_name==this_mod_group['name']):
            mod_group_match += 1

            for this_mod in this_mod_group['mods']:  
                # print(this_mod)

                if ((mod_name=="all") or (mod_name==this_mod['name'])) and not (this_mod['mode']=="skip"):
                    mod_match += 1

                    if not (this_mod['name']==""):
                        print(f"{Fore.BLUE}========= " + this_mod_group['name'] + " - " + this_mod['name'] + f"{Style.RESET_ALL}")

                    source_folder = this_mod["source_folder"]
                    release_folder = this_mod["release_folder"]
                    github_folder = this_mod["github_folder"]
                    mod_assets = this_mod["assets"] 
                    mode = this_mod["mode"]

                    # print(source_folder)
                    # print(release_folder)
                    # print(github_folder)
                    # print(mod_assets)
                    # print(mode)

                    deployfiles([source_folder], [release_folder, github_folder], mod_assets, mode)

                elif (this_mod['mode']=="skip"):
                    if not (this_mod['name']==""):
                        print(f"{Fore.YELLOW}========= " + this_mod_group['name'] + " - " + this_mod['name'] + f" -- SKIPPED {Style.RESET_ALL}")

    if (mod_group_match == 0):
            print(f"{Fore.YELLOW}:: No mod group deployed{Style.RESET_ALL}")

    if (mod_match == 0):
            print(f"{Fore.YELLOW}:: No mods deployed{Style.RESET_ALL}")


def deployfiles(source_list, destination_list, modassets_list, mode):
    for asset in modassets_list:
        filepattern_list = asset["file_patterns"]

        for source in source_list:
            for destination in destination_list:
                for filepattern in filepattern_list:
                    if not (destination==""):
                        if not debug:
                            trymakedir(destination)

                    if (not os.path.exists(source + asset["path"])):
                        print(f"{Fore.RED}>> Invalid Source folder: " + source + asset["path"]+ f"{Style.RESET_ALL}")
                    else:
                        if not (destination==""):
                            if not debug:
                                docopy(source + asset["path"], destination + asset["path"], filepattern, mode)
                            else:
                                print("> Source: " + source + asset["path"])
                                print("> Target: " + destination + asset["path"])
                                print("> Pattern: " + filepattern)

# BUG: This function doesn't copy files if they already exist in the target folder with a different case than the originals
#      They are just skipped for some reason. Forcing the use of no case didn't help.
def docopy(inputdir, outputdir, pattern, mode):
    foundfiles = ""
    regexpattern = fnmatch.translate(pattern)
    prog = re.compile(regexpattern)

    # print("Source: "+ inputdir)
    # print("Target: "+ outputdir)
    if not debug:
        trymakedir(outputdir)

    totalfilecount = 0
    for (root, dirs, files) in os.walk(inputdir):
        filecount = 0 
        for fn in files:
            m = prog.match(fn)
            if m:
                targetdir = join(outputdir, os.path.relpath(root, inputdir))
                if not debug:
                    trymakedir(targetdir)
                
                # Exclude some files
                if (fn != "Thumbs.db") and (not (".vortex_backup" in fn)):
                    # If file is newer, or if filesize is different in case os .esp (because of load order)
                    copyfileflag = False
                    # print("Looking for: "+ join(root, fn))
                    # print(":: into    : "+ join(targetdir, fn))
 
                    if (not os.path.exists(join(targetdir, fn))):
                        foundfiles = foundfiles + "\n" + "Found new file " + join(targetdir, fn)
                        copyfileflag = True
                    elif (os.path.exists(join(root, fn)) and os.path.exists(join(targetdir, fn))):
                        if (os.path.getmtime(join(root, fn)) > os.path.getmtime(join(targetdir, fn))):
                            # Copy newer files - updated recently
                            foundfiles = foundfiles + "\n" + "Updating newer file " + join(targetdir, fn)
                            copyfileflag = True
                        elif (not filecmp.cmp(join(root, fn), join(targetdir, fn))):
                            # Copy new or missing files
                            foundfiles = foundfiles + "\n" + "Updating different file " + join(targetdir, fn)
                            copyfileflag = True
                        # elif (".esp" in fn) or (".esm" in fn):
                           # Force copy of esp and esm files (because of timestamps used for load order)
                           # foundfiles = foundfiles + "\n" + "Updating file " + join(targetdir, fn)
                           # copyfileflag = True

                    if (copyfileflag):
                        if not debug:
                            shutil.copy(join(root, fn), join(targetdir, fn))

                        # Disabled for issues with time
                        # if (".esp" in fn) or (".esm" in fn):
                        #    os.utime(join(targetdir, fn), None)
                        filecount = filecount + 1
        totalfilecount = totalfilecount + filecount
        if filecount != 0: 
            print("Processing... " + pattern + " To: " + outputdir + foundfiles)
            print("     " + str(filecount) + " files in " + root)


def join(*args):
    return os.path.normpath(os.path.join(*args))


def trymakedir(path):
    try:
        os.makedirs(path)
    except Exception as e:
        # print(e)
        if not os.path.exists(path):
            raise Exception('>>> Failed to create output directory: ' + path)

 
if __name__ == '__main__':
    colorama_init()

    with open('mods_manifest.json', 'r') as f:
        mods_data = json.load(f)

    # creating set of keys that we want to compare
    root_keys_check = set(["mod_groups"]) 
    
    if root_keys_check.issubset(mods_data.keys()):
        deployAllMods(mods_data)       
        # deployMod(mods_data, 'MOD UTILITIES', 'CKTOOLS')
        # deployModGroup(mods_data, 'MOD UTILITIES')

    else:
        print(f"{Fore.RED}>>>Error: Key mod_groups is missing from mods_manifest.json file{Style.RESET_ALL}")
            


