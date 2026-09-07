import unittest, os
from main import ExpenseModel, ExpenseManager

class TestTracker(unittest.TestCase):
    def setUp(self):
        self.model = ExpenseModel()
        self.manager = ExpenseManager(self.model)
        self.manager.filepath = "test.json"
        
    def tearDown(self):
        if os.path.exists("test.json"): os.remove("test.json")

    def test_logic(self):
        self.manager.addExpense("Кава", "65", "Продукти")
        self.assertEqual(self.model.rowCount(), 1)
        self.assertEqual(self.manager.total, 65.0)
        
        self.manager.addExpense("Помилка", "abc", "Інше")
        self.assertEqual(self.model.rowCount(), 1) 
        
        self.manager.removeExpense(0)
        self.assertEqual(self.model.rowCount(), 0)

if __name__ == '__main__': unittest.main()