#!/usr/bin/env python3

import numpy as np, sys, os
from tools import Parameter

### EDIT YOUR PREFERENCES HERE ###

LANGUAGE = 'fr-FR'
TIMEZONE = 'Europe/Paris'

PORT = "5432"
HOST = ""
PASSWORD = ""

REDIRECT_URI = '127.0.0.1'

###

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
        DATABASES.add_item(item=f"'PASSWORD': '{PASSWORD}'")
        DATABASES.add_item(item=f"'HOST': '{HOST}'")
        DATABASES.add_item(item=f"'PORT': '{PORT}'")

        LANGUAGE_CODE = Parameter(name="LANGUAGE_CODE", content=lines, step=1)
        LANGUAGE_CODE.replace_item(item="LANGUAGE_CODE", new_content=LANGUAGE)

        TIME_ZONE = Parameter(name="TIME_ZONE", content=lines, step=1)
        TIME_ZONE.replace_item(item="TIME_ZONE", new_content=TIMEZONE)

        END_FILE = f"""\nSTATICFILES_DIRS = [\n    os.path.join(BASE_DIR, "static")\n]\nINTERNAL_IPS = [{REDIRECT_URI}]"""

    with open(path + "/settings.py", "w") as settings:

        lines[11] = "import os\n"

        for param in [INSTALLED_APPS, DATABASES, LANGUAGE_CODE, TIME_ZONE]:
            step = param.var_positions[f"{param.name}"]
            lines[step:step + param.length] = param.parameters

        settings.writelines(lines)

        settings.write(END_FILE)