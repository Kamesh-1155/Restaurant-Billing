import csv

MENU_FILE = "menu.csv"

class MenuManager:
    def __init__(self):
        self.menu = []
        self.load_menu()

    def load_menu(self):
        try:
            with open(MENU_FILE, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.menu = [
                    {
                        "code": row["code"].strip(),
                        "name": row["name"].strip(),
                        "price": (row["price"].strip())
                    }
                    for row in reader
                ]
        except FileNotFoundError:
            self.menu = []