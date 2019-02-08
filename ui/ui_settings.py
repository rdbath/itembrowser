# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_settings.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(292, 223)
        self.gridLayout = QtWidgets.QGridLayout(Settings)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Settings)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(Settings)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.saveSelectionInProject = QtWidgets.QCheckBox(Settings)
        self.saveSelectionInProject.setChecked(True)
        self.saveSelectionInProject.setObjectName("saveSelectionInProject")
        self.gridLayout.addWidget(self.saveSelectionInProject, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.rubberWidth = QtWidgets.QDoubleSpinBox(Settings)
        self.rubberWidth.setToolTip("")
        self.rubberWidth.setDecimals(1)
        self.rubberWidth.setSingleStep(1.0)
        self.rubberWidth.setProperty("value", 2.0)
        self.rubberWidth.setObjectName("rubberWidth")
        self.gridLayout.addWidget(self.rubberWidth, 3, 1, 1, 1)
        self.scale = QtWidgets.QSpinBox(Settings)
        self.scale.setMinimum(1)
        self.scale.setMaximum(15)
        self.scale.setProperty("value", 5)
        self.scale.setObjectName("scale")
        self.gridLayout.addWidget(self.scale, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Settings)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Settings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(Settings)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.dockArea = QtWidgets.QComboBox(Settings)
        self.dockArea.setObjectName("dockArea")
        self.dockArea.addItem("")
        self.dockArea.addItem("")
        self.gridLayout.addWidget(self.dockArea, 0, 1, 1, 1)
        self.rubberColor = QgsColorButton(Settings)
        self.rubberColor.setObjectName("rubberColor")
        self.gridLayout.addWidget(self.rubberColor, 4, 1, 1, 1)

        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Item Browser :: settings"))
        self.label_2.setText(_translate("Settings", "Rubberband size"))
        self.label.setText(_translate("Settings", "Rubberband color"))
        self.saveSelectionInProject.setText(_translate("Settings", "save selection in project"))
        self.label_3.setText(_translate("Settings", "Scaling"))
        self.label_4.setText(_translate("Settings", "Dock area"))
        self.dockArea.setItemText(0, _translate("Settings", "left"))
        self.dockArea.setItemText(1, _translate("Settings", "right"))
        self.rubberColor.setColorDialogTitle(_translate("Settings", "Select Color for rubber band"))

from qgis.gui import QgsColorButton
