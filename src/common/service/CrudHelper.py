import sqlite3, os

connection = sqlite3.connect("instance/ccs.db", check_same_thread=False)
cursor = connection.cursor()

class username:
    def __init__(self, vaule):
        self.vaule = vaule    

    def username_to_id(self):
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            if row[1] == self.vaule:
                return row[0]
            
    def id_to_username(self):
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            if row[0] == self.vaule:
                return row[1]
    
def Update_channel_usercars(id_channel, id_user, id_user_car, startcharge, endcharge):
        cursor.execute("INSERT INTO channel_usercars (id_channel, id_user, id_user_car, startcharge, endcharge)" 
                            "VALUES (?, ?, ?, ?, ?)",
                            (id_channel, id_user, id_user_car, startcharge, endcharge))
        connection.commit()

def channel_station_parrent_id_to_name():
    cursor.execute("SELECT * FROM stations")
    station_names = {row[0]:str(row[1]) for row in cursor.fetchall()}
    return station_names
            
#if __name__ == '__main__':
    #print(username_to_id('loh1na'))