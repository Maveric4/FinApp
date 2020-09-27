# pyuic5 -x FinApp_v1.ui -o designer.py
## Update designer file
from crypt_utils import update_UI
update_UI()


def catch_exceptions(t, val, tb):
    QtWidgets.QMessageBox.critical(None,
                                   "An exception was raised",
                                   "Exception type: {}, Exception value: {}".format(t, val))
    old_hook(t, val, tb)


## Imports
from PyQt5 import QtCore, QtGui, QtWidgets

from designer import Ui_MainWindow
import sys
from data_utils import Database
from models.category import Category
from warning import show_dialog

old_hook = sys.excepthook
sys.excepthook = catch_exceptions


class AppFin(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database(db_name="finapp")

    def add_logging_func(self):
        self.passwordEdit.hide()
        self.loginEdit.hide()
        self.LogInButton.hide()
        # self.LogInButton.clicked.connect(self.login)
        # self.tabWidget.hide()

    def set_addExpense_UI(self):
        self.expenseDateEdit.setCalendarPopup(True)
        self.expenseDateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.categoryComboBox.addItems(self.db.get_categories())

    def set_AddCategory_UI(self):
        self.addCategoryButton.clicked.connect(self.add_new_category)
        self.categoryListViewModel = QtGui.QStandardItemModel()
        self.categoriesListView.setModel(self.categoryListViewModel)
        for i in self.db.get_categories():
            item = QtGui.QStandardItem(i)
            self.categoryListViewModel.appendRow(item)
        self.deleteCategoryButton.clicked.connect(self.delete_category)

    def login(self):
        if self.loginEdit.toPlainText() == "dan" and self.passwordEdit.toPlainText() == "dan":
            self.passwordEdit.hide()
            self.loginEdit.hide()
            self.LogInButton.hide()
            self.tabWidget.show()

    def add_new_category(self):
        new_category = Category(self.categoryNameEdit.toPlainText().strip())
        if new_category.name == "":
            show_dialog("Category is empty", "Category")
        elif new_category.name in self.db.get_categories():
            show_dialog("Category exists already", "Category")
        else:
            self.db.add_category(new_category)
            item = QtGui.QStandardItem(new_category.name)
            self.categoryListViewModel.appendRow(item)
            self.categoryComboBox.addItem(new_category.name)
            self.categoryNameEdit.setText("")

    def delete_category(self):
        selected_item = self.categoriesListView.selectedIndexes()[0]
        self.db.remove_category(selected_item.data())
        self.categoryListViewModel.removeRow(selected_item.row())
        self.categoryComboBox.clear()
        self.categoryComboBox.addItems(self.db.get_categories())


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    app_f = AppFin()
    app_f.setupUi(MainWindow)
    app_f.add_logging_func()
    app_f.set_addExpense_UI()
    app_f.set_AddCategory_UI()
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
