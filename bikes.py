import sqlite3
from turtle import distance

db = sqlite3.connect("bikes.db")
db.isolation_level = None


def distance_of_user(user):
    
    distance = db.execute("SELECT SUM(distance) 
                          FROM Trips, Users 
                          WHERE Trips.user_id=Users.id 
                          AND Users.name=?", [user]).fetchone()
                          
    return distance[0]

def speed_of_user(user):
    
    t_dist = db.execute("SELECT SUM(distance), SUM(duration) 
                        FROM Trips, Users 
                        WHERE Trips.user_id=Users.id 
                        AND Users.name=?", [user]).fetchone()
                        
    return round((t_dist[0]/1000)/(t_dist[1]/60), 2)

def duration_in_each_city(day):
    
    cities = db.execute("SELECT C.name, SUM(T.duration) 
                        FROM Trips T, Cities C, Stops S 
                        WHERE T.from_id=S.id AND S.city_id=C.id AND T.day=? 
                        GROUP BY C.name", [day]).fetchall()
                        
    return cities

def users_in_city(city):
    
    users_amount = db.execute("SELECT COUNT(DISTINCT T.user_id) 
                              FROM Trips T, Cities C, Stops S 
                              WHERE T.from_id=S.id AND S.city_id=C.id 
                              AND C.name=?", [city]).fetchone()
                              
    return users_amount[0]

def trips_on_each_day(city):
    
    amount = db.execute("SELECT T.day, COUNT(*) 
                        FROM Trips T, Cities C, Stops S 
                        WHERE T.from_id=S.id AND S.city_id=C.id AND C.name=? 
                        GROUP BY T.day", [city]).fetchall()
                        
    return amount

def most_popular_start(city):
    
    fav_stop = db.execute("SELECT S.name, COUNT(T.from_id) 
                          FROM Trips T, Cities C, Stops S 
                          WHERE S.city_id=C.id AND T.from_id=S.id AND C.name=? 
                          GROUP BY S.name ORDER BY 2 DESC", [city]).fetchall()
                          
    return fav_stop[0]
