__author__ = 'korovkin_m'
import sys

OSTYPE = "c:/"
if sys.platform != "win32":
    OSTYPE = "/Server-3d/Project"

LTK_PATCH = OSTYPE + 'Users/MikhailKorovkin/Documents/maya/2016/scripts/LTK/'

if not sys.path.count(LTK_PATCH):
    sys.path.append(LTK_PATCH)
