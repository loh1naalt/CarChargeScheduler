import sqlite3


class UserCarService:
    def __init__(self):
        self.connection = sqlite3.connect("your_database_name.db")
        self.cursor = self.connection.cursor()

    def create_table(self):
        create_table_query = """
        CREATE TABLE user_cars(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER,
            carname TEXT,
            FOREIGN KEY(id_user) REFERENCES user_cars(id)
        )

        """

        self.cursor.execute(create_table_query)
        print("Table 'user_cars' created successfully")

    def insert_data(self, id_user, car_name):
        self.cursor.execute("INSERT INTO user_cars (id_user, carname) VALUES (?, ?)",
                            (id_user, car_name))
        self.connection.commit()

    def query_data(self):
        select_query = "SELECT * FROM user_cars"

        self.cursor.execute(select_query)

        for row in self.cursor.fetchall():
            print(f"ID: {row[0]}, UserID: {row[1]}, Car Name: {row[2]}")

    def update_data(self, target, id, id_user, car_name):
        match target:
            case 'user_id':
                self.cursor.execute("UPDATE user_cars SET id_user = ? WHERE id = ?",
                                    (id_user, id))
            case 'password':
                self.cursor.execute("UPDATE user_cars SET car_name = ? WHERE id = ?",
                                    (car_name, id))
        self.connection.commit()

    def delete_data(self, id_user):
        self.cursor.execute("DELETE FROM user_cars WHERE id = ?", id_user)
        self.connection.commit()