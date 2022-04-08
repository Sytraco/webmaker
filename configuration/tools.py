import os, sys, json, numpy as np

### path initialization
CURRENT_PATH = os.path.realpath(__file__)
PROJECT_DIR = "/".join(CURRENT_PATH.split("/")[:-2])  + "/"
COLORSTYLE_FILE = PROJECT_DIR + "configuration/style.sh"

### space parameters
hspace = " "
cspace = 2


def import_colors():
    
    ''' load the colorstyle file used in the shell script as python variables '''

    with open(COLORSTYLE_FILE) as filestyle:
        for row in filestyle:
            # exec('color="color_code"') >> color = "color_code"
            exec(row.replace("\n", "")) if not "#" in row else False


class Parameter:

    ''' edit a given line of the setting.py file generated from Django '''

    var_positions = {

        # "label": line_position
        "BASE_DIR": 15,
        "SECRET_KEY": 22,
        "DEBUG": 25,
        "ALLOWED_HOSTS": 27,
        "INSTALLED_APPS": 32,
        "MIDDLEWARE": 41,
        "ROOT_URLCONF": 51,
        "TEMPLATES": 53,
        "WSGI_APPLICATION": 69,
        "DATABASES": 75,
        "AUTH_PASSWORD_VALIDATORS": 86,
        "LANGUAGE_CODE": 105,
        "TIME_ZONE": 107,
        "USE_I18N": 109,
        "USE_L10N": 111,
        "USE_TZ": 113,
        "STATIC_URL": 115,
    }

    def __init__(self, name, content, step):
        self.name = name
        self.lines = content
        self.element_position = self.var_positions[name]
        self.parameters = content[self.element_position:self.element_position + step]
        self.length = step

        if ("{" in self.parameters[0]) and ("}" in self.parameters[-1]):
            self.dtype = "dict"
            self.mul = 2
            self.space = "        "
        elif ("[" in self.parameters[0]) and ("]" in self.parameters[-1]):
            self.dtype = "list"
            self.mul = 1
            self.space = "    "
        else:
            self.dtype = "str"

    def add_item(self, item, position=None):

        self.new_line()

        def edit_content(content, self=self):

            opening_list = content[0:self.mul]
            closure_list = content[-self.mul:]

            data = content[self.mul:-self.mul]
            data.append(f"""{self.space}{item},\n""")

            if position is not None:
                data = np.roll(data, position).tolist()

            return opening_list + data + closure_list

        self.parameters = edit_content(self.parameters)
        self.length += 1

    def replace_item(self, item, new_content):
        for i, line in enumerate(self.parameters):
            if (item in line) and (self.dtype == "dict"):
                self.parameters[i] = f"        '{item}': '{new_content}',\n"
            elif (item in line) and (self.dtype == "str"):
                self.parameters[i] = f"{item} = '{new_content}'\n"

    def remove_item(self, item):
        for i, line in enumerate(self.parameters):
            if (item in line) and (self.dtype == "dict"):
                self.parameters.pop(i)
        self.length -= 1

    def new_line(self):
        Nline = self.element_position + self.length
        self.lines.insert(Nline, '\n')
        for key in self.var_positions.keys():
            if Nline < self.var_positions[key]:
                self.var_positions[key] += 1


def app_commands():

    ''' load and display application commands from .json file. '''

    jsonfile = open(f"{PROJECT_DIR}/commands.json", "r")
    commands = json.load(jsonfile)

    # Usage function
    print(f"\nUsage:\n{hspace*cspace}webmaker <command> [options]\n")
    
    # Commands display
    print("Commands:")
    [print(f"{hspace*cspace}{command}\t\t{description}") for command, description in commands.items()]

    jsonfile.close()


def loadable_projects(path):

    ''' scan all the available applications to run the server'''

    # Loading all available projects
    projects = []
    for folder in os.listdir(path=path):
        try:
            projects.append(folder) if "base" in os.listdir(path=os.path.join(path, folder)) else True
        except NotADirectoryError:
            pass
    print(" ".join(projects))


if __name__ == "__main__":

    # generalization of script functions to shell application
    try:
        globals()[sys.argv[1]](sys.argv[2])
    except IndexError:
        globals()[sys.argv[1]]()