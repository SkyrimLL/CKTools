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
    print("Processing... " + pattern + " To: " + outputdir)
    regexpattern = fnmatch.translate(pattern)
    prog = re.compile(regexpattern)
    # print("     Mover: " + mover)
    totalfilecount = 0
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
        totalfilecount = totalfilecount + filecount
        if filecount != 0:
            print("     " + str(filecount) + " files in " + root)

    if totalfilecount == 0:
        print("     ... NO MATCH in " + root)


def deployfiles(sourcelist, destinationlist, modassetslist):
    for asset in modassetslist.keys():
        filepatternlist = modassetslist[asset]
        for source in sourcelist:
            for destination in destinationlist:
                for filepattern in filepatternlist:
                    trymakedir(destination)
                    docopy(source + asset, destination + asset, filepattern)
                    print("----")


def deployCKTools():
    print("========= CKTools")
    sourcefolder = "E:\\Documents\\Source\\CKTools\\"
    targetfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\CKTools\\"
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\CKTools\\"

    modassets = {}
    modassets["DeployCKFiles\\"] = ['deployCkFiles.py']
    modassets["GetGithubReleases\\"] = ['getGithubReleases.py']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deploySD():
    print("========= Sanguine Debauchery")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\Sanguine-Debauchery-Plus\\Dev\\Loose\\Data\\"
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SanguineDebauchery\\Data\\"

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

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\Sanguine-Debauchery-Plus\\Dev\\SDResources\\Data\\"
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SanguineDebauchery\\Data\\"

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

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deploySLD():
    print("========= SL Dialogues")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\SexLab-Dialogues\\Dev\\BSA\\Data\\"
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SexLab_Dialogues\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SLD_*.*', 'SLD_*.*']
    modassets["meshes\\actors\\character\\SL_Dialogues\\"] = ['*.*']
    modassets["meshes\\clutter\\SL_Dialogues\\"] = ['*.*']
    modassets["textures\\clutter\\SL_Dialogues\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\SexLab-Dialogues\\Dev\\Loose\\Data\\"
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SexLab_Dialogues\\Data\\"

    modassets = {}
    modassets["SEQ\\"] = ['SexLab_Dialogues.seq']
    modassets["Interface\\SexLab_Dialogues\\"] = ['*.*']
    modassets[""] = ['SexLab_Dialogues.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deploySLSD():
    print("========= Sisterhood of Dibella")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"
    targetfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\Dibella-Sisterhood\\Dev\\BSA\\Data\\"
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\SisterhoodOfDibella\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SL_Dibella_*.*']
    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\SexLab_DibellaCult.esp\\"] = ['*.*']
    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\Skyrim.esm\\"] = ['0001E82C.NIF', '0001E765.NIF', '000133A5.NIF', '000133B0.NIF', '000133B7.NIF', '0001335F.NIF', '00013386.NIF']
    modassets["meshes\\armor\\SL_Dibella\\"] = ['*.*']
    modassets["meshes\\clutter\\SL_Dibella\\"] = ['*.*']
    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\SexLab_DibellaCult.esp\\"] = ['*.*']
    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\Skyrim.esm\\"] = ['0001E82C.*', '0001E765.*', '000133A5.*', '000133B0.*', '000133B7.*', '0001335F.*', '00013386.*']
    modassets["textures\\armor\\SL_Dibella\\"] = ['*.*']
    modassets["textures\\clutter\\SL_Dibella\\"] = ['*.*']
    modassets["textures\\ashara\\Dimonized dress\\Skirt\\"] = ['*.*']
    modassets["textures\\azmoscreens\\"] = ['mrs3_gold*', 'ss*.*']
    modassets["textures\\azmoscreens\\statues\\"] = ['*.*']
    modassets["textures\\cubemaps\\"] = ['chitin_e_ebony.dds', 'quickskydark_eGD.dds']
    modassets["textures\\kasprutz\\armor\\bdo_kibelius\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\Dibella-Sisterhood\\Dev\\Loose\\Data\\"
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\SisterhoodOfDibella\\Data\\"

    modassets = {}
    modassets["SEQ\\"] = ['SexLab_DibellaCult.seq']
    modassets[""] = ['SexLab_DibellaCult.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    # ----
    print("========= Sisterhood of Dibella - Sisters addon")
    targetfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\Dibella-Sisterhood-Sisters\\Dev\\BSA\\Data\\"
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\SisterhoodOfDibella\\Data\\"

    modassets = {}
    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\SexLab_DibellaCult_Sisters.esp\\"] = ['*.*']
    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\Skyrim.esm\\"] = ['0001E82C.NIF', '0001E765.NIF', '000133A5.NIF', '000133B0.NIF', '000133B7.NIF', '0001335F.NIF', '00013386.NIF']
    modassets["meshes\\armor\\SL_Dibella_Sisters\\"] = ['*.*']
    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\SexLab_DibellaCult_Sisters.esp\\"] = ['*.*']
    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\Skyrim.esm\\"] = ['0001E82C.*', '0001E765.*', '000133A5.*', '000133B0.*', '000133B7.*', '0001335F.*', '00013386.*']
    modassets["textures\\armor\\SL_Dibella_Sisters\\"] = ['*.*']
    modassets["textures\\armor\\SL_Dibella\\"] = ['dibella_sister_outfit.dds','femalebody_1_s.dds','lilly.dds','lilly_n.dds','travel_hood.dds']
    modassets["textures\\armor\\Gatti\\"] = ['*.*']
    modassets["textures\\Ashara\\Imperial Wedding outfit\\"] = ['*.*']
    modassets["textures\\fox011\\f046\\"] = ['*.*']
    modassets["textures\\SexyLingerieSet\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\Dibella-Sisterhood-Sisters\\Dev\\Loose\\Data\\"
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\SisterhoodOfDibella\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SL_DibellaSisters*.*']
    modassets["SEQ\\"] = ['SexLab_DibellaCult_Sisters.seq']
    modassets[""] = ['SexLab_DibellaCult_Sisters.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

def deployAlicia():
    print("========= Alicia")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"
    targetfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\Alicia-PainSlut\\Dev\\BSA\\Data\\"
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Alicia\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['Alicia_*.*']

    modassets["sound\\Voice\\AliciaPainSlut.esp\\_Alicia_VOICE\\"] = ['*.*']

    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\AliciaPainSlut.esp\\"] = ['*.*']
    modassets["meshes\\actors\\character\\AliciaPainSlut\\"] = ['*.*']
    modassets["meshes\\armor\\AliciaPainSlut\\"] = ['*.*']
    modassets["meshes\\armor\\AliciaSanguineFollowers\\"] = ['*.*']
    modassets["meshes\\clutter\\AliciaPainSlut\\"] = ['*.*']
    modassets["meshes\\weapons\\AliciaPainSlut\\"] = ['*.*']

    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\AliciaPainSlut.esp\\"] = ['*.*']
    modassets["textures\\actors\\character\\AliciaPainSlut\\"] = ['*.*']
    modassets["textures\\_sd_\\shrine\\"] = ['*.*']
    modassets["textures\\armor\\AliciaPainSlut\\"] = ['*.*']
    modassets["textures\\azmoscreens\\"] = ['mrs3_gold*', 'ss*.*']
    modassets["textures\\azmoscreens\\statues\\"] = ['*.*']
    modassets["textures\\baronb\\dragon\\"] = ['*.*']
    modassets["textures\\clutter\\AliciaPainSlut\\"] = ['*.*']
    modassets["textures\\weapons\\AliciaPainSlut\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\02 - Releases\\Alicia-PainSlut\\Dev\\Loose\\Data\\"
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Alicia\\Data\\"

    modassets = {}
    modassets["SEQ\\"] = ['AliciaPainSlut.seq']
    modassets[""] = ['AliciaPainSlut.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


if __name__ == '__main__':

    # ===== CK Tools
    deployCKTools()

    # ===== Sanguine Debauchery +
    # deploySD()

    # ===== SL Dialogues
    # deploySLD()

    # ===== Sisterhood of Dibella
    # deploySLSD()

    # ===== Alicia
    deployAlicia()
