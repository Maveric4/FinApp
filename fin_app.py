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
from models.expense import Expense
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
        self.addNewExpenseButton.clicked.connect(self.add_new_expense)

    def clear_addExpense_UI(self):
        self.priceEdit.setText("")
        self.expenseDescriptionEdit.setText("")

    def set_addCategory_UI(self):
        self.addCategoryButton.clicked.connect(self.add_new_category)
        self.categoryListViewModel = QtGui.QStandardItemModel()
        self.categoriesListView.setModel(self.categoryListViewModel)
        for i in self.db.get_categories():
            item = QtGui.QStandardItem(i)
            self.categoryListViewModel.appendRow(item)
        self.deleteCategoryButton.clicked.connect(self.delete_category)

    def set_showExpenses_UI(self):
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideLeft)
        table_data, column_names = self.db.get_expenses()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        for row_number, row_data in enumerate(table_data):
            self.tableWidget.insertRow(row_number)
            for col_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(data)))

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

    def add_new_expense(self):
        desc = self.expenseDescriptionEdit.toPlainText().strip()
        price = self.priceEdit.toPlainText().strip().replace(",", ".")
        date = self.expenseDateEdit.date().toPyDate()
        category = Category(self.categoryComboBox.currentText())
        if desc == "" and price == "":
            show_dialog("Description or price is empty", "New Expense")
        elif category.name == "Choose category":
            show_dialog("Choose category", "New Expense")
        else:
            self.db.add_expense(Expense(desc, float(price), date, category))
            self.infoTopLabel.setText(f"Expense '{desc}' added")
            self.clear_addExpense_UI()

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
    app_f.set_showExpenses_UI()
    app_f.set_addCategory_UI()
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
