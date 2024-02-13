import sqlite3


class channelservice:
    def __init__(self):
        self.connection = sqlite3.connect("your_database_name.db")
        self.cursor = self.connection.cursor()

    def create_table(self):
        create_table_query = """        
        CREATE TABLE channels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_station INTEGER,
            title TEXT,
            price REAL,
            occupancy INTEGER, /*('true', 'false')*/
            FOREIGN KEY(id_station) REFERENCES channels(id)
        )

        """

        self.cursor.execute(create_table_query)
        return "Table 'users' created successfully"

    def insert_data(self, id_station, title, price, occupancy):
        self.cursor.execute("INSERT INTO channels (id_station, title, price, occupancy) "
                            "VALUES (?, ?, ?, ?)",
                            (id_station, title, price, occupancy))
        self.connection.commit()

    def query_data(self):
        select_query = "SELECT * FROM channels"

        self.cursor.execute(select_query)

        for row in self.cursor.fetchall():
            return f"ID: {row[0]}, Station_id: {row[1]}, Title: {row[2]}, price: {row[3]}" \
                  f", Occupancy(0 - True, 1 - False): {row[4]}"

    def update_data(self, target, id_station, title, price, occupancy):
        match target:
            case 'title':
                self.cursor.execute("UPDATE channels SET id_station = ? WHERE id = ?",
                                    (title, id_station))
            case 'price':
                self.cursor.execute("UPDATE channels SET addressname = ? WHERE id = ?",
                                    (price, id_station))
            case 'occupancy':
                self.cursor.execute("UPDATE channels SET channels_per_station = ? WHERE id = ?",
                                    (occupancy, id_station))
        self.connection.commit()

    def delete_data(self, id_station):
        self.cursor.execute("DELETE FROM channels WHERE title = ?", id_station)
        self.connection.commit()
