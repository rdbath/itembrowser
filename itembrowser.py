from __future__ import print_function
from __future__ import absolute_import
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

from builtins import object
from qgis.PyQt.QtCore import QUrl, Qt
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon, QDesktopServices
from qgis.core import QgsMapLayer, QgsProject

from .core.mysettings import MySettings
from .gui.mysettingsdialog import MySettingsDialog
from .gui.itembrowserdock import ItemBrowserDock

from . import resources


class itemBrowser(object):
    def __init__(self, iface):
        self.iface = iface
        self.settings = MySettings()
        self.docks = {}

    def initGui(self):
        # browse action
        self.browserAction = QAction(QIcon(":/plugins/itembrowser/icons/itembrowser.svg"),
                                     "Browse selected items of current layer", self.iface.mainWindow())
        self.browserAction.setEnabled(False)
        self.browserAction.triggered.connect(lambda x: self.openBrowserDock())  # prevent passing "False" to the method
        self.iface.addToolBarIcon(self.browserAction)
        self.iface.addPluginToMenu("&Item Browser", self.browserAction)
        # settings
        self.uisettingsAction = QAction(QIcon(":/plugins/itembrowser/icons/settings.svg"), "settings",
                                        self.iface.mainWindow())
        self.uisettingsAction.triggered.connect(self.showSettings)
        self.iface.addPluginToMenu("&Item Browser", self.uisettingsAction)     
        # help
        self.helpAction = QAction(QIcon(":/plugins/itembrowser/icons/help.svg"), "Help", self.iface.mainWindow())
        self.helpAction.triggered.connect(lambda: QDesktopServices().openUrl(QUrl("http://3nids.github.io/itembrowser")))
        self.iface.addPluginToMenu("&Item Browser", self.helpAction)

        self.iface.currentLayerChanged.connect(self.currentLayerChanged)
        self.iface.mapCanvas().selectionChanged.connect(self.currentLayerChanged)
        QgsProject.instance().readProject.connect(self.reloadSession)

        self.currentLayerChanged(self.iface.activeLayer())
              
    def unload(self):
        self.iface.currentLayerChanged.disconnect(self.currentLayerChanged)
        self.iface.mapCanvas().selectionChanged.disconnect(self.currentLayerChanged)
        QgsProject.instance().readProject.disconnect(self.reloadSession)
        self.iface.removePluginMenu("&Item Browser", self.browserAction)
        self.iface.removePluginMenu("&Item Browser", self.uisettingsAction)
        self.iface.removePluginMenu("&Item Browser", self.helpAction)
        self.iface.removeToolBarIcon(self.browserAction)
        
    def currentLayerChanged(self, layer):
        enable = (layer is not None
                  and layer.type() == QgsMapLayer.VectorLayer
                  and layer.isSpatial()
                  and len(layer.selectedFeatureIds()) > 1)
        self.browserAction.setEnabled(enable)

    def openBrowserDock(self, layer=None, currentFeature=0):
        if layer is None:
            layer = self.iface.mapCanvas().currentLayer()
        if layer is None:
            return
        if layer.id() in self.docks:
            #print "layer already docked"
            return
        dock = ItemBrowserDock(self.iface, layer, currentFeature)
        dock.dockRemoved.connect(self.dockRemoved)
        if self.settings.value("dockArea") == 1:
            self.iface.addDockWidget(Qt.RightDockWidgetArea, dock)
        else:
            self.iface.addDockWidget(Qt.LeftDockWidgetArea, dock)
        self.docks[layer.id()] = dock

    def dockRemoved(self, layerid):
        del self.docks[layerid]

    def reloadSession(self):
        # fix_print_with_import
        #print("item browser reloaded")
        if not self.settings.value("saveSelectionInProject"):
            return
        for layer in self.iface.mapCanvas().layers():
            exec("selection = %s" % layer.customProperty("itemBrowserSelection", "[]"))
            if len(selection) > 0:
                currentFeature = int(layer.customProperty("itemBrowserCurrentItem", 0))
                layer.setSelectedFeatures(selection)
                if len(layer.selectedFeatureIds()) < 1:
                    return
                if layer.id() in self.docks:
                    self.docks[layer.id()].setCurrentItem(currentFeature)
                else:
                    self.openBrowserDock(layer, currentFeature)

    def showSettings(self):
        MySettingsDialog().exec_()




