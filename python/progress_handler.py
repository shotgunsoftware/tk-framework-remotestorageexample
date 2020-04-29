from sgtk.platform.qt import QtCore, QtGui
from .ui import resources_rc

class ProgressNotificationDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(ProgressNotificationDialog, self).__init__(parent=parent, f=QtCore.Qt.FramelessWindowHint)

        self.setModal(True)
        self.setWindowTitle("Remote Storage Process")

        self._msg_label = QtGui.QLabel("Test", parent=self)

        self._download_label = QtGui.QLabel(parent=self)
        self._download_label.setPixmap(QtGui.QPixmap(":/icons/down.png"))
        self._download_label.setScaledContents(True)
        self._download_label.setMaximumSize(32, 32)
        self._download_label.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        self._upload_label = QtGui.QLabel(parent=self)
        self._upload_label.setPixmap(QtGui.QPixmap(":/icons/up.png"))
        self._upload_label.setScaledContents(True)
        self._upload_label.setMaximumSize(32, 32)
        self._upload_label.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        self._layout = QtGui.QHBoxLayout()
        self._layout.addWidget(self._download_label)
        self._layout.addWidget(self._upload_label)
        self._layout.addWidget(self._msg_label)
        self.setLayout(self._layout)

    def show_upload_msg(self, msg):
        self._download_label.setVisible(False)
        self._upload_label.setVisible(True)
        self._show_message(msg)

    def show_download_msg(self, msg):
        self._download_label.setVisible(True)
        self._upload_label.setVisible(False)
        self._show_message(msg)

    def _show_message(self, msg):
        self._msg_label.setText(msg)
        self.show()
        QtCore.QCoreApplication.processEvents()