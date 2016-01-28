import sys
import getpass
WINUSER = getpass.getuser()

OSTYPE = "c:/"

MAIN_PATCH = OSTYPE + 'Users/%s/Documents/maya/2016/scripts/Zoidberg/' % WINUSER
RESURCES_PATCH = MAIN_PATCH + "ui/resources/"

print MAIN_PATCH
if not sys.path.count(MAIN_PATCH):
    sys.path.append(MAIN_PATCH)
