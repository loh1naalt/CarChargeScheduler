import sqlite3, sys, time


def execute_query_with_retry(query, params=None):
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        try:
            connection = sqlite3.connect("instance/ccs.db", check_same_thread=False)
            cursor = connection.cursor()
            if params is not None:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            # Commit the transaction
            connection.commit()
            cursor.close()
            connection.close()
            break
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                attempts += 1
                time.sleep(0.1)  # Wait for a short duration before retrying
            else:
                raise
    else:
        raise Exception("Failed to execute query after multiple attempts")

def fetch_query_with_retry(query):
    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        try:
            connection = sqlite3.connect("instance/ccs.db", check_same_thread=False)
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            return data

        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                attempts += 1
                time.sleep(0.1)  # Wait for a short duration before retrying
            else:
                raise
    else:
        raise Exception("Failed to execute query after multiple attempts")


class username:
    def __init__(self):
        pass

    def username_to_id(self, vaule):
        data = fetch_query_with_retry("SELECT * FROM users")
        for row in data:
            if row[1] == vaule:
                return row[0]

            
    def id_to_username(self, vaule):
        data = fetch_query_with_retry("SELECT * FROM users")
        for row in data:
            if row[0] == vaule:
                return row[1]


            

    
class channel_usercars:
    def __init__(self, username_id):
        self.data = fetch_query_with_retry("SELECT * FROM channel_usercars")
        self.username_id = username_id
    
    def sync_user(self):
        if self.data != None:
            for item in self.data:
                if item[2] == self.username_id:
                    return 0
                
            if self.username_id != None:
                execute_query_with_retry("INSERT INTO channel_usercars (id_user) VALUES (?)",
                               (self.username_id, ))
                return 0
            else:
                return 0
        else:
            return 'error'

    def sync_user_channel(self, channel_id):
        if self.data is not None:
            for item in self.data:
                # return f'username id is: {self.username_id}, channel_id is {channel_id}'
                if self.username_id == item[2]:
                    if item[1] != channel_id:
                        execute_query_with_retry("INSERT INTO channel_usercars (id_user, id_channel) VALUES (?, ?)",
                                                 (self.username_id, channel_id))
                        return 0
                    elif channel_id is not None and item[1] is None:
                        execute_query_with_retry("UPDATE channel_usercars SET id_channel = ? WHERE id_user = ?",
                                                 (int(channel_id), int(self.username_id)))
                        return 0
            return 0

        else:
            return 'error'
    def clear_user_channel(self, channel_id):
        if self.data is not None:
            username_ids = []
            for i in self.data:
                username_ids.append(i[2])
            for item in self.data:
                if self.username_id == item[2]:
                    if username_ids.count(self.username_id) > 1:
                        execute_query_with_retry("DELETE from channel_usercars WHERE id NOT IN (SELECT MIN(id) "
                                                 "FROM channel_usercars GROUP BY id_user)", )
                        return 0
                    elif channel_id is not None and item[1] is not None:
                        execute_query_with_retry("UPDATE channel_usercars SET id_channel = ? WHERE id_user = ?",
                                                 (None, int(self.username_id)))
                        return 0

            return 0

        else:
            return 'error'
    
    def sync_usercars(self, car_id):
        if self.data != None:
            for item in self.data:
                if item[3] == car_id:
                    return 0
                
            if car_id != None:
                execute_query_with_retry("UPDATE channel_usercars SET ? WHERE id_user = ?",
                               (car_id, self.username_id))
                return 0
            else:
                return 0
        else:
            return 'error'





def channel_station_parrent_id_to_name():
    cursor.execute("SELECT * FROM stations")
    station_names = {row[0]:str(row[1]) for row in cursor.fetchall()}
    return station_names
            
#if __name__ == '__main__':
    #print(username_to_id('loh1na'))
