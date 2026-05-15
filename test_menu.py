import unittest
from unittest.mock import patch, mock_open
from io import StringIO
import sys
from Restaurant_App.menu import MenuManager

class TestMenuManager(unittest.TestCase):
    def setUp(self):
        # Patch open to mock file operations
        self.mock_open = mock_open(read_data="code,name,price\n1,Pizza,250\n2,Burger,150\n")
        self.patcher = patch("builtins.open", self.mock_open)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_load_menu_success(self):
        manager = MenuManager()
        self.assertEqual(len(manager.menu), 2)
        self.assertEqual(manager.menu[0]['name'], 'Pizza')

    def test_load_menu_file_not_found(self):
        # Simulate FileNotFoundError by stopping patch and patching open to raise error
        self.patcher.stop()
        with patch("builtins.open", side_effect=FileNotFoundError):
            manager = MenuManager()
            self.assertEqual(manager.menu, [])

        # Restart patch for other tests
        self.patcher.start()

    @patch('builtins.input', side_effect=['3', 'Pasta', '200'])
    def test_add_item(self, mock_input):
        manager = MenuManager()
        initial_count = len(manager.menu)
        with patch.object(manager, 'save_menu') as mock_save:
            manager.add_item()
            self.assertEqual(len(manager.menu), initial_count + 1)
            self.assertEqual(manager.menu[-1]['name'], 'Pasta')
            mock_save.assert_called_once()

    def test_view_menu_output(self):
        manager = MenuManager()
        captured_output = StringIO()
        sys.stdout = captured_output
        manager.view_menu()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Pizza", output)
        self.assertIn("Burger", output)

if __name__ == '__main__':
    unittest.main()
