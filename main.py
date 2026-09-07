import sys, json, os
os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl, QAbstractListModel, Qt, QModelIndex, pyqtProperty
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine

class ExpenseModel(QAbstractListModel):
    DescriptionRole = Qt.ItemDataRole.UserRole + 1
    AmountRole = Qt.ItemDataRole.UserRole + 2
    CategoryRole = Qt.ItemDataRole.UserRole + 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self._expenses = []

    def rowCount(self, parent=QModelIndex()): return len(self._expenses)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid(): return None
        exp = self._expenses[index.row()]
        if role == self.DescriptionRole: return exp["description"]
        elif role == self.AmountRole: return exp["amount"]
        elif role == self.CategoryRole: return exp["category"]
        return None

    def roleNames(self): return {self.DescriptionRole: b"description", self.AmountRole: b"amount", self.CategoryRole: b"category"}
    
    def addExpense(self, desc, amount, cat):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._expenses.append({"description": desc, "amount": amount, "category": cat})
        self.endInsertRows()

    def removeExpense(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._expenses[row]
        self.endRemoveRows()

    def getExpenses(self): return self._expenses
    def setExpenses(self, expenses):
        self.beginResetModel()
        self._expenses = expenses
        self.endResetModel()

class ExpenseManager(QObject):
    totalChanged = pyqtSignal(float)

    def __init__(self, model):
        super().__init__()
        self._model = model
        self._total = 0.0
        self.filepath = "expenses.json"
        self.loadData()

    @pyqtProperty(float, notify=totalChanged)
    def total(self): return self._total

    @pyqtSlot(str, str, str)
    def addExpense(self, desc, amount_str, cat):
        try:
            amount = float(amount_str.replace(',', '.'))
            self._model.addExpense(desc, amount, cat)
            self._calc()
            self.saveData()
        except ValueError: pass

    @pyqtSlot(int)
    def removeExpense(self, index):
        self._model.removeExpense(index)
        self._calc()
        self.saveData()

    def _calc(self):
        self._total = sum(item["amount"] for item in self._model.getExpenses())
        self.totalChanged.emit(self._total)

    def saveData(self):
        with open(self.filepath, "w", encoding="utf-8") as f: json.dump(self._model.getExpenses(), f, ensure_ascii=False, indent=4)

    def loadData(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                self._model.setExpenses(json.load(f))
                self._calc()

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    model = ExpenseModel()
    manager = ExpenseManager(model)
    engine.rootContext().setContextProperty("expenseModel", model)
    engine.rootContext().setContextProperty("expenseManager", manager)
    engine.load(QUrl.fromLocalFile("main.qml"))
    sys.exit(app.exec())