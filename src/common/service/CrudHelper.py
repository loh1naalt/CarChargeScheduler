import sqlite3, sys

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
            

    
class channel_usercars:
    def __init__(self, username_id):
        self.username_id = username_id
        cursor.execute("SELECT * FROM channel_usercars")
        self.data = cursor.fetchall()
    
    def sync_user(self):
        if self.data != None:
            for item in self.data:
                if item[2] == self.username_id:
                    return 0
            else:
                if self.username_id != None:
                    cursor.execute(f"INSERT INTO channel_usercars (id_user) VALUES ({self.username_id})")
                    connection.commit()
                    return 0
                else:
                    pass
        else:
            return 'error'

    def sync_user_channel(self):
        pass




def channel_station_parrent_id_to_name():
    cursor.execute("SELECT * FROM stations")
    station_names = {row[0]:str(row[1]) for row in cursor.fetchall()}
    return station_names
            
#if __name__ == '__main__':
    #print(username_to_id('loh1na'))
