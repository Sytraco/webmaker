#!/usr/bin/env python3

import numpy as np, sys, os

class Parameter:

    var_positions = {
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


if __name__ == "__main__":

    app_name = sys.argv[1]
    path = os.getcwd()

    with open(path + "/settings.py", "r") as settings:
        lines = settings.readlines()

        INSTALLED_APPS = Parameter(name="INSTALLED_APPS", content=lines, step=8)
        INSTALLED_APPS.add_item(item="'website.apps.WebsiteConfig'", position=1)
        INSTALLED_APPS.add_item(item=f"'{app_name}'")

        DATABASES = Parameter(name="DATABASES", content=lines, step=6)
        DATABASES.replace_item(item="ENGINE", new_content="django.db.backends.postgresql")
        DATABASES.replace_item(item="NAME", new_content=f"{app_name}")
        DATABASES.add_item(item="'PASSWORD': ''")
        DATABASES.add_item(item="'HOST': ''")
        DATABASES.add_item(item="'PORT': '5432'")

        LANGUAGE_CODE = Parameter(name="LANGUAGE_CODE", content=lines, step=1)
        LANGUAGE_CODE.replace_item(item="LANGUAGE_CODE", new_content='fr-FR')

        TIME_ZONE = Parameter(name="TIME_ZONE", content=lines, step=1)
        TIME_ZONE.replace_item(item="TIME_ZONE", new_content='Europe/Paris')

        END_FILE = """\nSTATICFILES_DIRS = [\n    os.path.join(BASE_DIR, "static")\n]\nINTERNAL_IPS = ['127.0.0.1']"""

    with open(path + "/settings.py", "w") as settings:

        lines[11] = "import os\n"

        for param in [INSTALLED_APPS, DATABASES, LANGUAGE_CODE, TIME_ZONE]:
            step = param.var_positions[f"{param.name}"]
            lines[step:step + param.length] = param.parameters

        settings.writelines(lines)

        settings.write(END_FILE)