from django.db import connection, transaction
import datetime

cursor = connection.cursor()

def add_review(user_id, mid, summary):
    cursor.execute("""INSERT INTO Review VALUES('%s', '%s', '%s', '%s');""" % (user_id, mid, summary, datetime.datetime.now()))

def change_rating(user_id, mid, rating):
    cursor.execute("""UPDATE Rates SET rating = %s WHERE user_id = %s AND mid = %s;""" % (rating, user_id, mid))

def likes_movie(user_id, mid):
    cursor.execute("""INSERT INTO LikesMovie VALUES('%s', '%s');""" % (user_id, mid))
    
def not_likes_movie(user_id, mid):
    cursor.execute("""DELETE FROM LikesMovie WHERE user_id = %s AND mid = %s;""" % (user_id, mid))
    
def add_friend(user_id1, user_id2):
    cursor.execute("""INSERT INTO isFriend VALUES('%s', '%s');""" % (user_id1, user_id2))
    
def remove_friend(user_id1, user_id2):
    cursor.execute("""DELETE FROM isFriend WHERE uid1 = %s AND uid2 = %s;""" % (user_id1, user_id2))

def find_movie_by_title(title, mpaa):
    cursor.execute("""SELECT m.mid FROM Movie m WHERE m.name LIKE '%%%s%%' and m.MPAA < %s;""" % (title, mpaa))
    return cursor.fetchall()

def find_movie_by_rating(rating1, rating2=None, mpaa=None):
    query = 'SELECT m.mid FROM Movie m WHERE m.avgRating '
    if rating2 == None:
        query += '= %s' % (rating1)
    else:
        query += '>= %s AND m.avgRating <= %s' % (rating1, rating2) 
    
    if mpaa <> None:
        query += ' AND m.MPAA < %s;' % (mpaa)
    else:
        query += ';'
    
    cursor.execute("""%s""" % query)
    return cursor.fetchall()

def find_movie_by_year(year1, year2=None, mpaa=None):
    query = 'SELECT m.mid FROM Movie m WHERE m.year '
    if year2 == None:
        query += '= %s' % (year1)
    else:
        query += '>= %s AND m.year <= %s' % (year1, year2)
    
    if mpaa <> None:
        query += ' AND m.MPAA < %s;' % (mpaa)
    else:
        query += ';'
    
    cursor.execute("""%s""" % query)
    return cursor.fetchall()

def find_all_movie_by_person_list(peopleList, mpaa=None):
    query = 'SELECT m.mid FROM Movie m, isInvolved iv, Person p WHERE m.mid = iv.mid AND p.pid = iv.pid AND ('
    for person in peopleList:
        query += ' p.name LIKE \'%%%s%%\' or ' % (person)
    query = query.rstrip(' or ')
    query += ')'
    if mpaa <> None:
        query += ' AND m.MPAA < 7;'
    else:
        query += ';' 
    cursor.execute("""%s""" % query)
    return cursor.fetchall()

def find_movie_by_all_persons(peopleList, mpaa=None):
    query = ''
    cursor.execute("""%s""" % query)
    return cursor.fetchall()
        
def top_k_search(value_k, mpaa=None):
    query = 'SELECT m.mid FROM Movie m '
    if mpaa <> None:
        query += 'WHERE m.MPAA < %s ' % (mpaa)
    query += 'ORDER BY m.avgRating DESC, m.numOfRatings DESC LIMIT %s;' % (value_k)
    cursor.execute("""%s""" % query)
    return cursor.fetchall()

def find_user(name):
     cursor.execute("""SELECT u.user_id FROM Users u WHERE u.login LIKE '%%%s%%' or u.name LIKE '%%%s%%';""" % (name, name))
     return cursor.fetchall()