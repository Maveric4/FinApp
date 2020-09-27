from PyQt5.QtWidgets import QMessageBox

# from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout,
# class CustomDialog(QDialog):
#
#     def __init__(self, windowTitle="Title", *args, **kwargs):
#         super(CustomDialog, self).__init__(*args, **kwargs)
#
#         self.setWindowTitle(windowTitle)
#
#         QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
#
#         self.buttonBox = QDialogButtonBox(QBtn)
#         self.buttonBox.accepted.connect(self.accept)
#         self.buttonBox.rejected.connect(self.reject)
#
#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.buttonBox)
#         self.setLayout(self.layout)


def show_dialog(msg="", title="Message Box"):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(msg)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        return 1
    else:
        return 0
