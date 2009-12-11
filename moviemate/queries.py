from django.db import connection, transaction
import datetime

def get_movie_by_id(mid):
    cursor = connection.cursor()
    cursor.execute("""SELECT m.name, m.year, m.avgRating, m.numOfRatings, g.genre
                      FROM Movie m, Genre g, isType i
                      WHERE m.mid='%s' and i.mid=m.mid and g.gid = i.gid""" % mid)
    row = cursor.fetchone()
    cursor.close()
    return row

def add_review(user_id, mid, summary):
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO Review VALUES('%s', '%s', '%s', '%s');""" % (user_id, mid, summary, datetime.datetime.now()))
    transaction.commit_unless_managed()
    cursor.close()
    
def get_reviews(mid):
    cursor = connection.cursor()
    cursor.execute("""SELECT u.name, r.summary, r.timestamp FROM Users u, Review r WHERE r.mid = '%s'
                          and u.user_id = r.user_id ORDER BY r.timestamp DESC""" % mid)
    row = cursor.fetchall()
    cursor.close()
    return row

def change_rating(user_id, mid, rating):
    cursor = connection.cursor()
    cursor.execute("""UPDATE Rates SET rating = '%s' WHERE user_id = '%s' AND mid = '%s';""" % (rating, user_id, mid))
    transaction.commit_unless_managed()
    cursor.close()
    
def add_rating(user_id, mid, rating):
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO Rates(user_id, mid, rating) VALUES('%s', '%s', '%s');""" % (user_id, mid, rating))
    cursor.execute("""UPDATE Movie SET numOfRatings = numOfRatings+1 WHERE mid = %s;""" % (mid))
    transaction.commit_unless_managed()
    cursor.close()
    
def get_rating(user_id, mid):
    cursor = connection.cursor()
    cursor.execute("""SELECT rating FROM Rates WHERE user_id = '%s' and mid = '%s'""" % (user_id, mid))
    row = cursor.fetchone()
    cursor.close()
    return row

def likes_movie(user_id, mid):
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO LikesMovie VALUES('%s', '%s');""" % (user_id, mid))
    transaction.commit_unless_managed()
    cursor.close()
    
def not_likes_movie(user_id, mid):
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM LikesMovie WHERE user_id = %s AND mid = %s;""" % (user_id, mid))
    transaction.commit_unless_managed()
    cursor.close()

def add_friend(user_id1, user_id2):
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO isFriend VALUES('%s', '%s');""" % (user_id1, user_id2))
    transaction.commit_unless_managed()
    cursor.close()

def remove_friend(user_id1, user_id2):
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM isFriend WHERE uid1 = %s AND uid2 = %s;""" % (user_id1, user_id2))
    transaction.commit_unless_managed()
    cursor.close()

def find_movie_by_title(title, mpaa=None):
    cursor = connection.cursor()
    query = "SELECT * FROM Movie m WHERE m.name LIKE '%%%%%s%%%%'" % (title)
    if mpaa <> None:
        query += ' AND (m.MPAA < %s OR m.MPAA IS NULL);' % (mpaa)
    else:
        query += ';'
    cursor.execute("%s" % query)
    row = cursor.fetchall()
    cursor.close()
    return row

def find_movie_by_rating(rating1, rating2=None, mpaa=None):
    cursor = connection.cursor()
    query = 'SELECT * FROM Movie m WHERE m.avgRating '
    if rating2 == None:
        query += '= %s' % (rating1)
    else:
        query += '>= %s AND m.avgRating <= %s' % (rating1, rating2) 
    
    if mpaa <> None:
        query += ' AND (m.MPAA < %s OR m.MPAA IS NULL);' % (mpaa)
    else:
        query += ';'
    
    cursor.execute("""%s""" % query)
    row = cursor.fetchall()
    cursor.close()
    return row

def find_movie_by_year(year1, year2=None, mpaa=None):
    cursor = connection.cursor()
    query = 'SELECT * FROM Movie m WHERE m.year '
    if year2 == None:
        query += '= \'%s\'' % (year1)
    else:
        query += '>= \'%s\' AND m.year <= \'%s\'' % (year1, year2)
    
    if mpaa <> None:
        query += ' AND (m.MPAA < %s OR m.MPAA IS NULL);' % (mpaa)
    else:
        query += ';'
    
    cursor.execute("""%s""" % (query))
    row = cursor.fetchall()
    cursor.close()
    return row

def find_all_movies_by_person_list(peopleList, mpaa=None):
    cursor = connection.cursor()
    query = 'SELECT * FROM Movie m, isInvolved iv, Person p WHERE m.mid = iv.mid AND p.pid = iv.pid AND ('
    for person in peopleList:
        if person <> None:
            query += ' p.name LIKE \'%s\' or ' % (person)
    query = query.rstrip(' or ')
    query += ')'
    if mpaa <> None:
        query += ' AND (m.MPAA < %s OR m.MPAA IS NULL);' % (mpaa)
    else:
        query += ';' 
    cursor.execute("""%s""" % query)
    row = cursor.fetchall()
    cursor.close()
    return row

## NOT DONE
def find_movie_by_all_persons(peopleList, mpaa=None):
    cursor = connection.cursor()
    
    count = len(peopleList)
    
    subquery1 = '(SELECT iv1.mid FROM Person p1, isInvolved iv1 WHERE p1.pid = iv1.pid and p1.name LIKE \'%s\' and iv1.role <> \'Director\')' % peopleList[0]
    if count >= 2:
        subquery2 = '(SELECT iv2.mid FROM %s AS act1, isInvolved iv2, Person p2 WHERE act1.mid = iv2.mid and iv2.pid = p2.pid and p2.name LIKE \'%s\' and iv2.role <> \'Director\')' % (subquery1, peopleList[1])
    else:
        subquery2 = subquery1
        
    if count >= 3:
        subquery3 = '(SELECT iv3.mid FROM %s AS act2, isInvolved iv3, Person p3 WHERE act2.mid = iv3.mid and iv3.pid = p3.pid and p3.name LIKE \'%s\' and iv3.role <> \'Director\')' % (subquery2, peopleList[2])
    else:
        subquery3 = subquery2
    
    if count >= 4:
        subquery4 = '(SELECT iv4.mid FROM %s AS act3, isInvolved iv4, Person p4 WHERE act3.mid = iv4.mid and iv4.pid = p4.pid and p4.name LIKE \'%s\' and iv4.role <> \'Director\')' % (subquery3, peopleList[3])
    else:
        subquery4 = subquery3
    
    if count == 5:
        subquery5 = '(SELECT iv5.mid FROM %s AS act4, isInvolved iv5, Person p5 WHERE act4.mid = iv5.mid and iv5.pid = p5.pid and p5.name LIKE \'%s\' and iv5.role <> \'Director\')' % (subquery4, peopleList[4])
    else:
        subquery5 = subquery4
    
    query = 'SELECT * FROM %s AS act5, Movie m WHERE act5.mid = m.mid' % (subquery5)

    if mpaa <> None:
        query += ' AND (m.MPAA < %s OR m.MPAA IS NULL);' % (mpaa)
    else:
        query += ';'
    
    cursor.execute("""%s""" % query)
    row = cursor.fetchall()
    cursor.close()
    return row

def find_cast_for_director(director, mpaa=None):
    cursor = connection.cursor()
    subquery = '(SELECT iv.mid FROM Person p, isInvolved iv WHERE iv.pid = p.pid AND p.name LIKE \'%s\' AND iv.role = \'Director\')' % director
    query = 'SELECT DISTINCT iv2.pid, p.name FROM %s as m, isInvolved iv2, Person p WHERE m.mid = iv2.mid and iv2.pid = p.pid and iv2.role <> \'Director\'' % subquery
    if mpaa <> None:
        query += ' AND (m.MPAA < %s OR m.MPAA IS NULL);' % (mpaa)
    else:
        query += ';'
    cursor.execute("""%s""" % query)
    row = cursor.fetchall()
    cursor.close()
    return row
        
def top_k_search(value_k, mpaa=None):
    cursor = connection.cursor()
    query = 'SELECT * FROM Movie m '
    if mpaa <> None:
        query += 'WHERE m.MPAA < %s OR m.MPAA IS NULL ' % (mpaa)
    query += 'ORDER BY m.avgRating DESC, m.numOfRatings DESC LIMIT %s;' % (value_k)
    cursor.execute("""%s""" % query)
    row = cursor.fetchall()
    cursor.close()
    return row

def find_user(name):
    cursor = connection.cursor()
    cursor.execute("""SELECT u.user_id, u.login, u.name FROM Users u WHERE u.login LIKE '%%%%%s%%%%' or u.name LIKE '%%%%%s%%%%';""" % (name, name))
    row = cursor.fetchall()
    cursor.close()
    return row

def find_person(name):
    cursor = connection.cursor()
    cursor.execute("""SELECT p.pid, p.name FROM Person p WHERE p.name LIKE '%%%%%s%%%%';""" % (name))
    row = cursor.fetchall()
    cursor.close()
    return row
 
def sql_query(query):
    query.replace('%', '%%')
    #query.replace('\r\n', ' ')
    query = " ".join(query.splitlines())
    print query
    cursor = connection.cursor()
    cursor.execute("""%s""" % query)
    transaction.commit_unless_managed()
    row = cursor.fetchall()
    cursor.close()
    return row