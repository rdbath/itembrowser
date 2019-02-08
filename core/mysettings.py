#-----------------------------------------------------------
#
# Item Browser is a QGIS plugin which allows you to browse a multiple selection.
#
# Copyright    : (C) 2013 Denis Rouzaud
# Email        : denis.rouzaud@gmail.com
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this progsram; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------

from qgis.PyQt.QtGui import QColor
from ..qgissettingmanager import SettingManager, Scope, Bool, String, Stringlist, Integer, Double, Color, Enum

pluginName = "itembrowser"


class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, pluginName)

        # global settings
        self.add_setting(Integer("dockArea", Scope.Global, 0))  # 0: right, 1: left
        self.add_setting(Bool("saveSelectionInProject", Scope.Global, True))
        self.add_setting(Integer("scale", Scope.Global, 4))
        self.add_setting(Double("rubberWidth", Scope.Global, 2))
        self.add_setting(Color("rubberColor", Scope.Global, QColor(255, 0, 0, 150), True))

