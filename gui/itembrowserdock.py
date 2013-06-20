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

from PyQt4.QtCore import SIGNAL, pyqtSignature, pyqtSignal, Qt
from PyQt4.QtGui import QDockWidget, QIcon
from qgis.core import QgsPoint, QgsRectangle, QgsFeatureRequest, QgsFeature
from qgis.gui import QgsRubberBand

from ..core.mysettings import MySettings
from ..ui.ui_itembrowser import Ui_itembrowser


class ItemBrowserDock(QDockWidget, Ui_itembrowser):
    dockRemoved = pyqtSignal(str)

    def __init__(self, iface, layer, currentFeature):
        self.iface = iface
        self.layer = layer
        self.renderer = self.iface.mapCanvas().mapRenderer()
        self.settings = MySettings()
        QDockWidget.__init__(self)
        self.setupUi(self)

        self.setWindowTitle("ItemBrowser: %s" % layer.name())
        if layer.hasGeometryType() is False:
            self.panCheck.setChecked(False)
            self.panCheck.setEnabled(False)
            self.scaleCheck.setChecked(False)
            self.scaleCheck.setEnabled(False)

        self.previousButton.setArrowType(Qt.LeftArrow)
        self.nextButton.setArrowType(Qt.RightArrow)
        icon = QIcon(":/plugins/itembrowser/icons/openform.png")
        self.editFormButton.setIcon(icon)

        self.rubber = QgsRubberBand(self.iface.mapCanvas())
        self.layer.selectionChanged.connect(self.selectionChanged)
        self.layer.layerDeleted.connect(self.close)

        self.selectionChanged()
        self.listCombo.setCurrentIndex(currentFeature)

    def closeEvent(self, e):
        self.rubber.reset()
        self.layer.selectionChanged.disconnect(self.selectionChanged)
        if self.settings.value("saveSelectionInProject"):
            self.layer.setCustomProperty("itemBrowserSelection", repr([]))
        self.dockRemoved.emit(self.layer.id())
          
    def selectionChanged(self):
        self.cleanBrowserFields()
        self.rubber.reset()
        nItems = self.layer.selectedFeatureCount()
        if nItems < 2:
            self.close()
            self.layer.emit(SIGNAL("browserNoItem()"))
            return
        self.browseFrame.setEnabled(True)
        self.subset = self.layer.selectedFeaturesIds()
        if self.settings.value("saveSelectionInProject"):
            self.layer.setCustomProperty("itemBrowserSelection", repr(self.subset))
        for fid in self.subset:
            self.listCombo.addItem("%u" % fid)

    def cleanBrowserFields(self):
        self.currentPosLabel.setText('0/0')
        self.listCombo.clear()
          
    def panScaleToItem(self, feature):
        if self.panCheck.isChecked() is False:
            return
        featBobo = feature.geometry().boundingBox()
        # if scaling and bobo has width and height (i.e. not a point)
        if self.scaleCheck.isChecked() and featBobo.width() != 0 and featBobo.height() != 0:
            featBobo.scale(self.settings.value("scale"))
            ul = self.renderer.layerToMapCoordinates(self.layer, QgsPoint(featBobo.xMinimum(), featBobo.yMaximum()))
            ur = self.renderer.layerToMapCoordinates(self.layer, QgsPoint(featBobo.xMaximum(), featBobo.yMaximum()))
            ll = self.renderer.layerToMapCoordinates(self.layer, QgsPoint(featBobo.xMinimum(), featBobo.yMinimum()))
            lr = self.renderer.layerToMapCoordinates(self.layer, QgsPoint(featBobo.xMaximum(), featBobo.yMinimum()))
            x = (ul.x(), ur.x(), ll.x(), lr.x())
            y = (ul.y(), ur.y(), ll.y(), lr.y())
            x0 = min(x)
            y0 = min(y)
            x1 = max(x)
            y1 = max(y)
        else:
            panTo = self.renderer.layerToMapCoordinates(self.layer, featBobo.center())
            mapBobo = self.iface.mapCanvas().extent()
            xshift = panTo.x() - mapBobo.center().x()
            yshift = panTo.y() - mapBobo.center().y()
            x0 = mapBobo.xMinimum() + xshift
            y0 = mapBobo.yMinimum() + yshift
            x1 = mapBobo.xMaximum() + xshift
            y1 = mapBobo.yMaximum() + yshift
        self.iface.mapCanvas().setExtent(QgsRectangle(x0, y0, x1, y1))
        self.iface.mapCanvas().refresh()

    def getCurrentItem(self):
        i = self.listCombo.currentIndex()
        if i == -1:
            return None
        f = QgsFeature()
        if self.layer.getFeatures(QgsFeatureRequest().setFilterFid(self.subset[i])).nextFeature(f):
            return f
        else:
            raise NameError("feature not found")

    @pyqtSignature("on_previousButton_clicked()")
    def on_previousButton_clicked(self):
        i = self.listCombo.currentIndex()
        n = max(0, i-1)
        self.listCombo.setCurrentIndex(n)
          
    @pyqtSignature("on_nextButton_clicked()")
    def on_nextButton_clicked(self):
        i = self.listCombo.currentIndex()
        c = self.listCombo.count()
        n = min(i+1, c-1)
        self.listCombo.setCurrentIndex(n)

    @pyqtSignature("on_listCombo_activated(int)")
    def on_listCombo_currentIndexChanged(self, i):
        if self.settings.value("saveSelectionInProject"):
            self.layer.setCustomProperty("itemBrowserCurrentItem", i)

    @pyqtSignature("on_listCombo_currentIndexChanged(int)")
    def on_listCombo_currentIndexChanged(self, i):
        feature = self.getCurrentItem()
        if feature is None: 
            return
        self.rubber.reset()
        if self.listCombo.count() > 1:
            width = self.settings.value("rubberWidth")
            color = self.settings.value("rubberColor")
            self.rubber.setColor(color)
            self.rubber.setWidth(width)
            self.rubber.setToGeometry(feature.geometry(), self.layer)
        # scale to feature
        self.panScaleToItem(feature)
        # Update browser
        self.currentPosLabel.setText("%u/%u" % (i+1, len(self.subset)))
        # emit signal
        self.layer.emit(SIGNAL("browserCurrentItem(long)"), feature.id())
          
    @pyqtSignature("on_panCheck_stateChanged(int)")
    def on_panCheck_stateChanged(self, i):
        if self.panCheck.isChecked():
            self.scaleCheck.setEnabled(True)
            feature = self.getCurrentItem()
            if feature is None:
                return
            self.panScaleToItem(feature)
        else:
            self.scaleCheck.setEnabled(False)
               
    @pyqtSignature("on_scaleCheck_stateChanged(int)")
    def on_scaleCheck_stateChanged(self, i):
        if self.scaleCheck.isChecked():
            feature = self.getCurrentItem()
            if feature is None: 
                return
            self.panScaleToItem(feature)

    @pyqtSignature("on_editFormButton_clicked()")
    def on_editFormButton_clicked(self):
        self.iface.openFeatureForm(self.layer, self.getCurrentItem())
