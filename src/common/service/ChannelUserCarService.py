import sqlite3


class channel_usercarservice:
    def __init__(self):
        self.connection = sqlite3.connect("ccs.db")
        self.cursor = self.connection.cursor()

    def create_table(self):
        create_table_query = """
        CREATE TABLE channel_usercars(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_channel INTEGER, 
            id_user INTEGER,
            id_user_car INTEGER,
            startcharge TEXT, /*("YYYY-MM-DD HH:MM:SS.SSS")*/
            endcharge TEXT, /*("YYYY-MM-DD HH:MM:SS.SSS")*/
            FOREIGN KEY (id_channel) REFERENCES channels(id),
            FOREIGN KEY (id_user) REFERENCES users(id),
            FOREIGN KEY (id_user_car) REFERENCES user_cars(id)
        )
        """

        self.cursor.execute(create_table_query)
        return "Table 'users' created successfully"

    def insert_data(self, id_channel, id_user, id_user_car, startcharge, endcharge):
        self.cursor.execute("INSERT INTO channel_usercars (id_channel, id_user, id_user_car, startcharge, endcharge)" 
                            "VALUES (?, ?, ?, ?, ?)",
                            (id_channel, id_user, id_user_car, startcharge, endcharge))
        self.connection.commit()

    def query_data(self):
        select_query = "SELECT * FROM channel_usercars"

        self.cursor.execute(select_query)

        for row in self.cursor.fetchall():
            return f"ID: {row[0]}, ChannelID: {row[1]}, UserID: {row[2]}, CarID: {row[3]}" \
                   f", StartCharge:{row[4]} ,EndCharge{row[5]}"

    def update_data(self, target, id, id_channel, id_user, id_user_car, startcharge, endcharge):
        match target:
            case 'id_channel':
                self.cursor.execute("UPDATE channel_usercars SET id_channel = ? WHERE id = ?",
                                    (id_channel, id))
            case 'id_user':
                self.cursor.execute("UPDATE channel_usercars SET id_user = ? WHERE id = ?",
                                    (id_user, id))
            case 'id_user_car':
                self.cursor.execute("UPDATE channel_usercars SET id_user_car = ? WHERE id = ?",
                                    (id_user_car, id))
            case 'channels_per_station':
                self.cursor.execute("UPDATE channel_usercars SET startcharge = ? WHERE id = ?",
                                    (startcharge, id))
            case 'channels_per_station':
                self.cursor.execute("UPDATE channel_usercars SET endcharge = ? WHERE id = ?",
                                    (endcharge, id))

        self.connection.commit()

    def delete_data(self, id_user):
        self.cursor.execute("DELETE FROM channel_usercars WHERE title = ?", id_user)
        self.connection.commit()

