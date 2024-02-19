import sqlite3


class StationService:
    def __init__(self):
        self.connection = sqlite3.connect("ccs.db")
        self.cursor = self.connection.cursor()

    def create_table(self):
        create_table_query = """
        CREATE TABLE stations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            addressname TEXT,
            channels_per_station INTEGER
        )
        """

        self.cursor.execute(create_table_query)
        return "Table 'users' created successfully"

    def insert_data(self, title, address_name, channels_per_station):
        self.cursor.execute("INSERT INTO stations (title, addressname, channels_per_station) VALUES (?, ?, ?)",
                            (title, address_name, channels_per_station))
        self.connection.commit()

    def query_data(self):
        select_query = "SELECT * FROM stations"

        self.cursor.execute(select_query)

        for row in self.cursor.fetchall():
            return f"ID: {row[0]}, Title: {row[1]}, Address Name: {row[2]}, Channels per station: {row[3]}"

    def update_data(self, target, id, title, address_name, channels_per_station):
        match target:
            case 'title':
                self.cursor.execute("UPDATE stations SET title = ? WHERE id = ?",
                                    (title, id))
            case 'addressname':
                self.cursor.execute("UPDATE stations SET addressname = ? WHERE id = ?",
                                    (address_name, id))
            case 'channels_per_station':
                self.cursor.execute("UPDATE stations SET channels_per_station = ? WHERE id = ?",
                                    (channels_per_station, id))
        self.connection.commit()

    def delete_data(self, title):
        self.cursor.execute("DELETE FROM stations WHERE title = ?", title)
        self.connection.commit()
