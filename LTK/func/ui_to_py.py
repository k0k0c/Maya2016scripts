import LTK.config as config
import pysideuic as uic
import sys
import os
from subprocess import call

LTK_PATCH = config.LTK_PATCH
LGT_UI_PATCH = 'ui/qtd/'
LGT_PYUI_PATCH = 'ui/pyuic/'
file_ui_list = []
file_pyui_list = []
file_qrc_list = []

def rebuild_pyui_file(filename):
    uifile_patch = LTK_PATCH + LGT_UI_PATCH + filename
    pyfile_patch = LTK_PATCH + LGT_PYUI_PATCH + filename.split(".")[0] + ".py"
    uifile_time = os.path.getmtime(uifile_patch)
    pyfile_time = os.path.isfile(pyfile_patch) == True and os.path.getmtime(pyfile_patch) or 0
    if pyfile_time < uifile_time:
        uifile = open(uifile_patch, "r")
        pyfile = open(pyfile_patch, "w")
        uic.compileUi(uifile, pyfile)
        print "RECOMPILE: " + LTK_PATCH + LGT_UI_PATCH + filename
        uifile.close()
        pyfile.close()


def rebuild_qrc_file(filename):
    qrcfile_patch = LTK_PATCH + LGT_UI_PATCH + filename
    pyfile_patch = LTK_PATCH + LGT_PYUI_PATCH + filename.split(".")[0] + "_rc.py"
    qrc_time = os.path.getmtime(qrcfile_patch)
    pyfile_time = os.path.isfile(pyfile_patch) == True and os.path.getmtime(pyfile_patch) or 0
    if pyfile_time < qrc_time:
        call("pyside-rcc -o %s -py2 %s" % (pyfile_patch, qrcfile_patch))
        print "RECOMPILE: " + LTK_PATCH + LGT_UI_PATCH + qrcfile_patch


for file in os.listdir(LTK_PATCH + LGT_UI_PATCH):
    if file.endswith(".ui"):
        file_ui_list.append(file)

for file in os.listdir(LTK_PATCH + LGT_PYUI_PATCH):
    if file.endswith(".py"):
        file_pyui_list.append(file)

for file in os.listdir(LTK_PATCH + LGT_UI_PATCH):
    if file.endswith(".qrc"):
        file_qrc_list.append(file)


def init(ui=file_ui_list, qrc=file_qrc_list, pyui=file_pyui_list, lines=None):
    # print "__Recompile_Ui__"
    if not lines:
        lines = []
    init_file = open(LTK_PATCH + LGT_PYUI_PATCH + '__init__.py', 'w')
    lines.append(str("__all__ = ['%s']" % "', '".join(i.split('.')[0] for i in pyui if i != '__init__.py')))
    lines += ["import %s" % (i.split('.')[0]) for i in pyui if i != '__init__.py']
    lines += ["reload(%s)" % (i.split('.')[0]) for i in pyui if i != '__init__.py']
    for i in lines:
        init_file.write("%s\n" % i)
    init_file.close()
    for file in ui:
        rebuild_pyui_file(file)
    for file in qrc:
        rebuild_qrc_file(file)


if __name__ == "__main__": init()
