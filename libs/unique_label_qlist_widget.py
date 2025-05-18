# -*- encoding: utf-8 -*-

from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets

class EscapableQListWidget(QtWidgets.QListWidget):
    def keyPressEvent(self, event):
        super(EscapableQListWidget, self).keyPressEvent(event)
        if event.key() == Qt.Key_Escape:
            self.clearSelection()


class UniqueLabelQListWidget(EscapableQListWidget):
    def __init__(self, parent=None, mainwindow=None):
        super(UniqueLabelQListWidget, self).__init__(parent)
        self.mainwindow = mainwindow  # Store reference to main window
        self.itemDoubleClicked.connect(self.onItemDoubleClicked)
        
    def onItemDoubleClicked(self, item):
        """Handle double click event on key list items"""
        key_cls = item.data(Qt.UserRole)
        
        # Use mainwindow if provided, otherwise fall back to parent()
        target = self.mainwindow if hasattr(self, 'mainwindow') and self.mainwindow else self.parent()
        
        if hasattr(target, 'updateSelectedShapeKeyCls'):
            target.updateSelectedShapeKeyCls(key_cls)
            
    def mousePressEvent(self, event):
        super(UniqueLabelQListWidget, self).mousePressEvent(event)
        if not self.indexAt(event.pos()).isValid():
            self.clearSelection()

    def findItemsByLabel(self, label, get_row=False):
        items = []
        for row in range(self.count()):
            item = self.item(row)
            if item.data(Qt.UserRole) == label:
                items.append(item)
                if get_row:
                    return row
        return items

    def createItemFromLabel(self, label):
        item = QtWidgets.QListWidgetItem()
        item.setData(Qt.UserRole, label)
        return item

    def setItemLabel(self, item, label, color=None):
        qlabel = QtWidgets.QLabel()
        if color is None:
            qlabel.setText(f"{label}")
        else:
            qlabel.setText(
                '<font color="#{:02x}{:02x}{:02x}">●</font> {} '.format(*color, label)
            )
        qlabel.setAlignment(Qt.AlignBottom)

        # item.setSizeHint(qlabel.sizeHint())
        item.setSizeHint(QSize(25, 25))

        self.setItemWidget(item, qlabel)
