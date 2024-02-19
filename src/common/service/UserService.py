import sqlite3


class UserService:
    def __init__(self):
        self.connection = sqlite3.connect("ccs.db")
        self.cursor = self.connection.cursor()

    def create_table(self):
        create_table_query = """
        CREATE TABLE users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT
        )
        """

        self.cursor.execute(create_table_query)
        return "Table 'users' created successfully"

    def insert_data(self, username, password, role):
        self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                            (username, password, role))
        self.connection.commit()

    def query_data(self):
        select_query = "SELECT * FROM users"

        self.cursor.execute(select_query)

        for row in self.cursor.fetchall():
            return f"ID: {row[0]}, Username: {row[1]}, Password: {row[2]}, Role: {row[3]}"

    def update_data(self, target, id, username, password, role):
        match target:
            case 'username':
                self.cursor.execute("UPDATE users SET username = ? WHERE id = ?",
                                    (username, id))
            case 'password':
                self.cursor.execute("UPDATE users SET password = ? WHERE id = ?",
                                    (password, id))
            case 'role':
                self.cursor.execute("UPDATE users SET role = ? WHERE id = ?",
                                    (role, id))
        self.connection.commit()

    def delete_data(self, username):
        self.cursor.execute("DELETE FROM users WHERE username = ?", username)
        self.connection.commit()
