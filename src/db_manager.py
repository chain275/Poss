import sqlite3

class db_manager:

    def __init__(self,db_name="menu.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.db_init()

    def db_init(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu (
                category TEXT,
                item_name TEXT,
                price REAL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customizations (
                category TEXT,
                option_type TEXT,
                option_value TEXT
            )
        ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Size_shortcuts
                 (shortcut TEXT PRIMARY KEY,
                  description TEXT NOT NULL)''')
    
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Ice_shortcuts
                 (shortcut TEXT PRIMARY KEY,
                  description TEXT NOT NULL)''')
    
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Sugar_shortcuts
                 (shortcut TEXT PRIMARY KEY,
                  description TEXT NOT NULL)''')


        self.cursor.execute("SELECT COUNT(*) FROM menu")
        a = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM customizations")
        b = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM customizations")
        c = self.cursor.fetchone()[0]



        if a > 0 and b > 0 and c > 0:
            return

        menu_data = {
            "Milk_tea": {
                "Classical_milk_tea": 30.00,
                "Brown_sugar_milk_tea": 40.00,
                "Kiwi_milk_tea": 50.00,
                "Strawberry_creamy_tea": 45.00
            },
            "Fruit_tea": {
                "Kiwi_jasmin": 35.00,
                "Lemonade_tea": 25.00,
                "Lemon_black_tea": 30.00,
                "Peach_tea": 25.00
            },
            "IceCream_cup": {
                "Super_boba_sundae": 45.00,
                "Super_mango_sundae": 40.00,
                "Oreo_sundae": 35.00,
                "Super_strawberry_sundae": 30.00
            },
            "Dessert": {
                "Ice_Cream": 15.00,
            }
        }

        customization_data = {
            "Milk_tea": {
                "Size": ["Regular size", "Large size (+$5)", "Extra Large size (+$10)"],
                "Ice": ["Regular Ice", "Light Ice", "Extra Ice"],
                "Sugar": ["50%", "70%", "100%"],
            },
            "Fruit_tea": {
                "Size": ["Regular size", "Large size (+$5)", "Extra Large size (+$10)"],
                "Ice": ["Regular Ice", "Light Ice", "Extra Ice"],
                "Sugar": ["50%", "70%", "100%"]
            },
            "IceCream_cup": {
                "Size": ["Regular size", "Large size (+$5)", "Extra Large size (+$10)"],
            },
            "Dessert": {
            }
        }

        for category, items in menu_data.items():
            for item_name, price in items.items():
                self.cursor.execute("INSERT INTO menu (category, item_name, price) VALUES (?, ?, ?)", 
                            (category, item_name, price))

        print("Database 'menu.db' created successfully")

        for category, options in customization_data.items():
            for option_type, option_values in options.items():
                for option_value in option_values:
                    self.cursor.execute("INSERT INTO customizations (category, option_type, option_value) VALUES (?, ?, ?)", 
                                (category, option_type, option_value))

        print("Database 'customizations.db' created successfully")

        size_data = [
        ("R", "Regular size"),
        ("L", "Large size (+$5.0)"),
        ("EL", "Extra Large size (+$10.00)")
        ]

        self.cursor.executemany('INSERT OR REPLACE INTO Size_shortcuts VALUES (?, ?)', size_data)
    
        ice_data = [
            ("R", "Regular Ice"),
            ("L", "Light Ice"),
            ("E", "Extra Ice")
        ]

        self.cursor.executemany('INSERT OR REPLACE INTO Ice_shortcuts VALUES (?, ?)', ice_data)
        
        sugar_data = [
            ("50", "50%"),
            ("70", "70%"),
            ("100", "100%")
        ]

        self.cursor.executemany('INSERT OR REPLACE INTO Sugar_shortcuts VALUES (?, ?)', sugar_data)

        print("customizations Database created successfully")

        self.connection.commit()
        
        return True


    def fetch_menu_data(self):
        
        self.cursor.execute("SELECT category, item_name, price FROM menu")
        rows = self.cursor.fetchall()
        
        menu_data = {}
        for category, item_name, price in rows:
            if category not in menu_data:
                menu_data[category] = {}
            menu_data[category][item_name] = price
        
        return menu_data
    

    def fetch_customization_data(self):
        
        self.cursor.execute("SELECT category, option_type, option_value FROM customizations")
        rows = self.cursor.fetchall()
        
        customization_data = {}
        for category, option_type, option_value in rows:
            if category not in customization_data:
                customization_data[category] = {}
            if option_type not in customization_data[category]:
                customization_data[category][option_type] = []
            customization_data[category][option_type].append(option_value)
        
        return customization_data
    
    def get_size_shortcuts(self):
        self.cursor.execute('SELECT * FROM Size_shortcuts')
        results = {row[0]: row[1] for row in self.cursor.fetchall()}
        return results

    def get_ice_shortcuts(self):
        self.cursor.execute('SELECT * FROM Ice_shortcuts')
        results = {row[0]: row[1] for row in self.cursor.fetchall()}
        return results

    def get_sugar_shortcuts(self):
        self.cursor.execute('SELECT * FROM Sugar_shortcuts')
        results = {row[0]: row[1] for row in self.cursor.fetchall()}
        return results


    
    def close_db(self):
        self.connection.close()

