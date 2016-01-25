from PyQt4 import uic
import sys
import os

LGT_PATCH = '//SERVER-3D/Project/lib/setup/maya/maya_scripts_rfm4/LGT/'
LGT_UI_PATCH = 'ui/'
file_ui_list = []
file_pyui_list = []

sys.path.append(LGT_PATCH)


def rebuild_lgt_pyui_file(filename):
    uifile_patch = LGT_PATCH + LGT_UI_PATCH + filename
    pyfile_patch = LGT_PATCH + LGT_UI_PATCH + filename.split(".")[0] + ".py"
    uifile_time = os.path.getmtime(uifile_patch)
    pyfile_time = os.path.getmtime(pyfile_patch)
    if pyfile_time < uifile_time:
        uifile = open(uifile_patch, "r")
        pyfile = open(pyfile_patch, "w")
        uic.compileUi(uifile, pyfile)
        print "RECOMPILE: " + LGT_PATCH + LGT_UI_PATCH + filename
        uifile.close()
        pyfile.close()
    else:
        print "ACTUAL:    " + LGT_PATCH + LGT_UI_PATCH + filename


for file in os.listdir(LGT_PATCH + LGT_UI_PATCH):
    if file.endswith(".ui"):
        file_ui_list.append(file)

def init():
    print "__Recompile_Ui__"
    for file in file_ui_list:
        rebuild_lgt_pyui_file(file)
