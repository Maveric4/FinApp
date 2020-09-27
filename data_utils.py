import mariadb


class Database:
    def __init__(self, db_name):
        try:
            self.db_name = db_name
            self.conn = self.connect()
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        except Exception as e:
            print("Cannot connect to database.")
            print(e)

    def connect(self):
        try:
            return mariadb.connect(
                user="root",
                password="root",
                host="localhost",
                database=self.db_name,
                port=3306)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

    def get_data_from_table(self, table_name):
        self.cur.execute(f"SELECT * FROM {self.db_name}.{table_name}")
        return self.cur.fetchall()
        # for (ID, name) in self.cur:
        #     print(f"First Name: {ID}, Last Name: {name}")

    def add_category(self, category, table_name="categories"):
        self.cur.execute(f"INSERT INTO {self.db_name}.{table_name} (Name) VALUES (%s)", [category.name])

    def get_categories(self):
        data = self.get_data_from_table(table_name="categories")
        return [cat[1] for cat in data]

    def remove_category(self, category_name, table_name="categories"):
        self.cur.execute(f"DELETE FROM {self.db_name}.{table_name} WHERE Name = ?", [category_name])


if __name__ == "__main__":
    db = Database(db_name="finapp")
    from models.category import Category
    cat = Category(None)
    db.remove_category(cat.name)
    print(db.get_categories())


