# Copyright (C) 2013 Simon Knapp
#
# This program is free software; you can redistribute it and/or
# modify it under the any terms you wish.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# To run this, type:
#
# python move_files.py <move|copy> <input directory> <output directory> [regexp]
#
# at a command prompt. If the first argument is move, then files will be moved
# otherwise files will be copied. It doesn't matter what directory structure
# is found under the input directory, the entire directory tree is walked and
# every file in every sub-directory will be checked.
#
# If no regular expression (4th argument) is provided, the one shown is used, but note that
# the named parameters must be suitable for the constructor of File.

import re
import os 
import shutil
import fnmatch


def join(*args):
    return os.path.normpath(os.path.join(*args))

def trymakedir(path):
    try:
        os.makedirs(path)
    except Exception as e:
        # print(e)
        if not os.path.exists(path):
            raise Exception('failed to create output directory: ' + path)


def docopy(inputdir, outputdir, pattern):
    print("Processing... " + pattern)
    # print(" From: " + inputdir)
    print(" To: " + outputdir)
    regexpattern = fnmatch.translate(pattern)
    prog = re.compile(regexpattern)
    # print("     Mover: " + mover)
    for (root, dirs, files) in os.walk(inputdir):
        # print(dirs)
        # print(files)

        filecount = 0
        for fn in files:
            # print(os.path.join(root, fn))
            # print("   File:" + fn)
            m = prog.match(fn)
            if m:
                targetdir = join(outputdir, os.path.relpath(root, inputdir))
                trymakedir(targetdir)
                # print(targetdir)
                # print("   File:" + fn)
                shutil.copy(join(root, fn), join(targetdir, fn))
                filecount = filecount + 1
        if filecount != 0:
            print("     " + root)
            print("     ... " + str(filecount) + " files")

def deployfiles(sourcelist, destinationlist, modassetslist):
    for asset in modassetslist.keys():
        filepatternlist = modassetslist[asset]
        for source in sourcelist:
            for destination in destinationlist:
                for filepattern in filepatternlist:
                    docopy(source + asset, destination + asset, filepattern)
                    print("----")

def deployCKTools():
    print("========= CKTools")
    SourceF = "E:\\Documents\\Source\\CKTools\\"

    TargetF = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\CKTools\\"
    GitHubF = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\CKTools\\"

    modassets = {}
    modassets["DeployCKFiles\\"] = ['deployCkFiles.py']

    deployfiles([SourceF], [TargetF, GitHubF], modassets)

def deploySD():
    print("========= Sanguine Debauchery")
    SourceF = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    TargetF = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\Sanguine-Debauchery-Plus\\Dev\\Loose\\Data\\"
    GitHubF = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SanguineDebauchery\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['_sd*.*', '_SD*.*']
    modassets["SEQ\\"] = ['sanguinesDebauchery.SEQ']
    modassets["Interface\\_SD_\\"] = ['sanguine_rose.*']
    modassets["Interface\\Translations\\"] = ['sanguinesDebauchery*.*']
    modassets["meshes\\_sd_\\"] = ['_sd*.*', '*.*']
    modassets["meshes\\actors\\atronachflame\\"] = ['testfireatronach.nif']
    modassets["meshes\\actors\\atronachflame\\character assets\\"] = ['*.*']
    modassets["meshes\\actors\\canine\\"] = ['compressleveloverride.txt', 'dogstatic.nif', 'nocompressionoverride.txt', 'spublocksize.txt']
    modassets["meshes\\actors\\canine\\character assets dog\\"] = ['*.*']
    modassets["meshes\\actors\\canine\\character assets wolf\\"] = ['*.*']
    modassets["meshes\\actors\\chaurus\\"] = ['testchaurus.nif']
    modassets["meshes\\actors\\chaurus\\character assets\\"] = ['*.*']
    modassets["meshes\\actors\\falmer\\"] = ['falmerarmorstatic.nif', 'falmerstatic.nif']
    modassets["meshes\\actors\\falmer\\character assets\\"] = ['*.*']
    modassets["meshes\\actors\\spriggan\\"] = ['fxsprigganattachments.nif', 'fxsprigganattachmentsmatron.nif', 'fxsprigganswarm.nif', 'sprigganfxtestunified.nif']
    modassets["meshes\\actors\\spriggan\\character assets\\"] = ['*.*']
    modassets["meshes\\actors\\character\\animations\\sanguinesDebauchery\\"] = ['*.*']
    modassets["meshes\\actors\\character\\animations\\"] = ['idlehandsbehindback.hkx']
    modassets["meshes\\actors\\character\\behaviors\\"] = ['FNIS_sanguinesDebauchery_Behavior.hkx']
    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\sanguinesDebauchery.esp\\"] = ['*.*']
    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\Skyrim.esm\\"] = ['0003DC4A.NIF', '0003DC4E.NIF', '0003DC50.NIF','0003DC52.NIF']
    modassets[""] = ['sanguinesDebauchery.esp']

    deployfiles([SourceF], [TargetF, GitHubF], modassets)

    TargetF = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\Sanguine-Debauchery-Plus\\Dev\\SDResources\\Data\\"
    GitHubF = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SanguineDebauchery\\Data\\"

    modassets = {}
    modassets["textures\\_sd_\\"] = ['*.*']
    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\sanguinesDebauchery.esp\\"] = ['*.*']
    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\Skyrim.esm\\"] = ['0003DC4A.*', '0003DC4E.*', '0003DC50.*', '0003DC52.*']
    modassets["textures\\actors\\character\\slavetats\\sdplus\\"] = ['*.*']
    modassets["textures\\actors\\character\\slavetats\\"] = ['sdplus.json']
    modassets["textures\\azmoscreens\\"] = ['*.*']
    modassets["textures\\bondage\\"] = ['*.*']
    modassets["textures\\sextoys-calyps\\"] = ['*.*']
    modassets["textures\\Sheogorad\\daedric\\"] = ['*.*']
    modassets["textures\\ZaZ\\Gagz\\"] = ['*.*']
    modassets["textures\\ZaZ\\Restraints\\"] = ['*.*']

    deployfiles([SourceF], [TargetF, GitHubF], modassets)


def deploySLDialogues():
    print("========= SL Dialogues")
    SourceF = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    TargetF = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\SexLab-Dialogues\\Dev\\BSA\\Data\\"
    GitHubF = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SexLab_Dialogues\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SLD_*.*', 'SLD_*.*']
    modassets["meshes\\actors\\character\\SL_Dialogues\\"] = ['*.*']
    modassets["meshes\\clutter\\SL_Dialogues\\"] = ['*.*']
    modassets["textures\\clutter\\SL_Dialogues\\"] = ['*.*']

    deployfiles([SourceF], [TargetF, GitHubF], modassets)

    TargetF = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\SexLab-Dialogues\\Dev\\Loose\\Data\\"
    GitHubF = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SexLab_Dialogues\\Data\\"

    modassets = {}
    modassets["SEQ\\"] = ['SexLab_Dialogues.seq']
    modassets["Interface\\SexLab_Dialogues\\"] = ['*.*']
    modassets[""] = ['SexLab_Dialogues.esp']

    deployfiles([SourceF], [TargetF, GitHubF], modassets)


if __name__ == '__main__':
    # REFERENCES
    # https://gist.github.com/Sleepingwell/6070119
    # https://docs.python.org/2/library/shutil.html
    # https://www.pythonforbeginners.com/os/python-the-shutil-module
    # http://xahlee.info/python/python_path_manipulation.html

    # ===== TO DO
    # Set up github repo for script + issues
    # Separate base paths from mod paths
    # Move mod assets to a double array / loop through array in 'deployfiles'
    #   Look into how to use double arrays in Python
    # Add support for config files for base paths and mods assets
    #   Look into how to include files in Python
    # Get list of issues for a defined milestone to generate release notes
    #   Look into how to connect to github API in Python

    # ===== CK Tools
    deployCKTools()

    # ===== Sanguine Debauchery +
    deploySD()

    # ===== SL Dialogues
    deploySLDialogues()