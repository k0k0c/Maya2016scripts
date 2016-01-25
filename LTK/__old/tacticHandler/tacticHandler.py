#! /usr/bin/env python
# -*- coding: utf-8 -*-

# tacticHandler.py
# Main Window calls
import sys

sys.path.append('\\\\SERVER-3D\\Project\\lib\\setup\\maya\\maya_scripts_rfm4\\LGT\\tacticHandler')

import ui.ui_main

reload(ui.ui_main)

ui.ui_main.startup()