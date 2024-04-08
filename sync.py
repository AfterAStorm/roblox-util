# Studio Implants #
# 
# Roblox file additions
# 
# sync.py #

# Settings #

# Roblox Client
ImplantClientSettings = True
TargetFPS = 165 # set fps cap

# Roblox Client/Studio
ImplantFiles = True # will copy files from the current working directory (cwd) into content folders

# Other
DeleteEmptyVersionFolders = True # if a folder doesn't have a studio or client exe it it, it'll be deleted

# Debug
PrintDebug = True

# Code #

from shutil import copy2, copytree, rmtree
from os import getenv, listdir, mkdir, getcwd, name, environ
from os.path import join, exists, isfile
#from argparse import ArgumentParser

#parser = ArgumentParser()
#parser.add_argument("")

started_with_doubleclick = name == 'nt' and 'PROMPT' not in environ

if started_with_doubleclick:
    # little gui prompt #
    
    YES = ["y", "yes"]
    NO  = ["n", "no"]
    
    def yesno(prompt: str, default: bool = False) -> bool:
        result = input(prompt).lower()
        if result in YES:
            return True
        elif result in NO:
            return False
        return default
    
    def intprompt(prompt: str, default: int = 0) -> int:
        result = input(prompt)
        if result.isdigit():
            return int(result)
        return default
    
    print(" : Studio Implant :")
    print()
    ImplantClientSettings = yesno("Implant client settings [for client]? (Y/n) ", True)
    if ImplantClientSettings:
        TargetFPS = intprompt("  Target FPS? (165) ", 165)
    
    ImplantFiles = yesno("Implant files from the current working directory [into content, will overwrite]? (Y/n) ", True)
    DeleteEmptyVersionFolders = yesno("Delete empty version folders? (Y/n) ", True)
    PrintDebug = True
    print()

# define debug
def debug(*message):
    if PrintDebug:
        print(*message)

# find appdata and version folder
appdata = getenv("LOCALAPPDATA")
versions = join(appdata, "Roblox\\Versions")

# define version type
class VersionType:
    Empty = 0
    Studio = 1
    Client = 2

# get version type func
def get_version_type(folder: str) -> int | VersionType:
    studio_exe = join(folder, "RobloxStudioBeta.exe")
    if isfile(studio_exe):
        return VersionType.Studio
    
    client_exe = join(folder, "RobloxPlayerBeta.exe")
    if isfile(client_exe):
        return VersionType.Client
    return VersionType.Empty

# define implant
def implant_directory(folder: str):
    # get version
    type = get_version_type(folder)
    
    # delete empty
    if type == VersionType.Empty:
        if DeleteEmptyVersionFolders:
            debug("Deleting empty version", folder)
            rmtree(folder)
        return
    
    # implant client settings for clients
    if type == VersionType.Client and ImplantClientSettings:
        debug("Implanting client settings into version", folder)
        if not exists(join(folder, "ClientSettings")):
            mkdir(join(folder, "ClientSettings"))
        with open(join(folder, "ClientSettings", "ClientAppSettings.json"), "w") as f:
            f.write('{"DFIntTaskSchedulerTargetFps": ' + str(TargetFPS) + '}')
    
    # check if we can implant
    if not ImplantFiles:
        return
    debug("Implanting files into version", folder)
    
    content = join(folder, "content")
    
    # implant current directory (excluding ourselves)
    for path in listdir(getcwd()):
        filepath = join(getcwd(), path)
        if filepath == __file__:
            continue
        if isfile(path): # copy file
            copy2(filepath, content)
        else: # copy directory
            copytree(filepath, join(content, path), dirs_exist_ok=True)

# loop through directory
for path in listdir(versions):
    if isfile(path):
        continue # not a versino folder, probably an installer
    if path.find("version-") < 0:
        if not path.find("built-in function dir"):
            debug(f"Invalid directory found! Named: \"{dir}\"")
        continue # invalid directory
    
    implant_directory(join(versions, path)) # implant
debug() # print empty line when done