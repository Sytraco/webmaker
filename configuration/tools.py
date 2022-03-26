import os, sys, json, subprocess

none = "\033[0m"
light_green = "\033[1;32m"
yellow = "\033[1;33m"
redB = "\033[1;31m"
hspace, cspace = " ", 2 # (space coefficient)

CURRENT_PATH = os.path.realpath(__file__)
PROJECT_DIR = "/".join(CURRENT_PATH.split("/")[:-2])

def function_commands():

    with open(f"{PROJECT_DIR}/commands.json", "r") as jsonfile:
        commands = json.load(jsonfile)

    # Blank line
    print("")

    # Usage function
    print(f"Usage:\n{hspace*cspace}webmaker <command> [options]\n")
    
    # Function commands
    print("Commands:")
    [print(f"{hspace*cspace}{command}\t\t{description}") for command, description in commands.items()]


def loadable_project(path):

    # Loading all available projects
    projects = []
    for folder in os.listdir(path=path):
        try:
            projects.append(folder) if "base" in os.listdir(path=os.path.join(path, folder)) else True
        except NotADirectoryError:
            pass
    print(" ".join(projects))


def git_repository():
    pass

if __name__ == "__main__":
    try:
        globals()[sys.argv[1]](sys.argv[2])
    except IndexError:
        globals()[sys.argv[1]]()

# np.savez --> stocke des tableaux dans un fichier