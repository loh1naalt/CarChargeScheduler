
CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT/*('user', 'admin')*/
);

CREATE TABLE user_cars(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER,
    carname TEXT,
    FOREIGN KEY(id_user) REFERENCES users(id)
);

CREATE TABLE stations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    addressname TEXT,
    channels_per_station INTEGER
);

CREATE TABLE "channels" (
	"id"	INTEGER,
	"id_station"	INTEGER,
	"title"	TEXT,
	"price"	REAL,
	"occupancy"	INTEGER,
	"occupiedby"	TEXT,
	FOREIGN KEY("id_station") REFERENCES "stations"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);

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
);

CREATE TABLE "reported_users_list" (
	"id"	INTEGER,
	"id_station"	INTEGER,
	"station_address"	TEXT,
	"id_channel"	INTEGER,
	"id_user"	INTEGER,
	"additional_tip"	TEXT,
	FOREIGN KEY("id_user") REFERENCES "users"("id"),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_channel") REFERENCES "channels"("id"),
	FOREIGN KEY("station_address") REFERENCES "station"("addressname")
	FOREIGN KEY("id_station") REFERENCES "station"("id")
);

