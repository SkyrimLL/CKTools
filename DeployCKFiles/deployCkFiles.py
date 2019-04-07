# This script will copy files from a source directory (skyrim/Data folder) to two target directories: one for backups and preparing BSA files and one for source control (github)

# Code adapted from: https://gist.github.com/Sleepingwell/6070119

# QUICK REFERENCES to Python resources
# https://docs.python.org/2/library/shutil.html
# https://www.pythonforbeginners.com/os/python-the-shutil-module
# http://xahlee.info/python/python_path_manipulation.html

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
    modassets["GetGithubReleases\\"] = ['getGithubReleases.py']

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
    modassets["meshes\\actors\\canine\\character assets dog\\"] = ['skeleton.nif']
    modassets["meshes\\actors\\canine\\character assets wolf\\"] = ['skeleton.nif']
    modassets["meshes\\actors\\chaurus\\"] = ['testchaurus.nif']
    modassets["meshes\\actors\\chaurus\\character assets\\"] = ['skeleton.nif']
    modassets["meshes\\actors\\falmer\\"] = ['falmerarmorstatic.nif', 'falmerstatic.nif']
    modassets["meshes\\actors\\falmer\\character assets\\"] = ['skeleton.nif']
    modassets["meshes\\actors\\spriggan\\"] = ['fxsprigganattachments.nif', 'fxsprigganattachmentsmatron.nif', 'fxsprigganswarm.nif', 'sprigganfxtestunified.nif']
    modassets["meshes\\actors\\spriggan\\character assets\\"] = ['skeleton.nif']
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

    # ===== CK Tools
    deployCKTools()

    # ===== Sanguine Debauchery +
    deploySD()

    # ===== SL Dialogues
    deploySLDialogues()