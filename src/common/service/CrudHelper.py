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


            

    
class sort_channel:
    def __init__(self):
        pass


