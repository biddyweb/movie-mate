from moviemate import models
from django.shortcuts import render_to_response
from django.db import connection, transaction



def movie_page(request, mid):
	if mid == None:
		movie = models.Movie.objects.filter(name=request.name, year=request.year).values()
	else:
		#movie = models.Movie.objects.get(mid=mid)
		#genre = models.Istype.objects.get(mid=mid)
		#cast = models.Isinvolved.objects.filter(mid=mid)
		#director = models.Isinvolved.objects.filter(mid=mid, role='Director')
		
		cursor = connection.cursor()
		
		#get movie info
		cursor.execute("""select m.name, m.year, m.avgRating, 
				m.numOfRatings, g.genre
				from Movie m, Genre g, isType i
				where m.mid='%s' and i.mid=m.mid and g.gid = i.gid""" % mid)
		row = cursor.fetchone()
		movie = {'mid':mid, 'name':row[0], 'year':row[1], 'avgrating':row[2], 'numofratings':row[3], 'genre':row[4]}
	
		#get director info
		cursor.execute("""select p.name, v.role from Person p, isInvolved v where
				v.mid = '%s' and v.role='Director' and p.pid = v.pid""" % mid)
		row = cursor.fetchone()
		director = {'name':row[0]}
		
		#get cast info
		cursor.execute("""select p.name, v.role, p.pid from Person p, isInvolved v where
				v.mid = '%s' and v.role <> 'Director' and p.pid = v.pid""" % mid)
		row = cursor.fetchall()
		cast = []
		for p in row:
			cast.append({'name':p[0], 'role':p[1], 'pid':p[2]})
			
		#get reviews
		cursor.execute("""select u.name, r.summary, r.timestamp from Users u, Review r where r.mid = '%s'
				and u.user_id = r.user_id""" % mid)
		row = cursor.fetchall()
		reviews = []
		print row
		for r in row:
			reviews.append({'username':r[0], 'summary':r[1], 'timestamp':r[2]})
	
	return render_to_response('movie.html', locals())
	
	
def person_page(request, pid):
	cursor = connection.cursor()
	cursor.execute("""select p.name, p.age, p.gender from Person p where p.pid = '%s'""" %pid)
	row = cursor.fetchone()
	
	person = {'name':row[0], 'age':row[1], 'gender':row[2]}
	
	cursor.execute("""select m.name, m.year, m.mid, v.role from Movie m, isInvolved v
			where v.pid = '%s' and m.mid = v.mid""" % pid)
	row = cursor.fetchall()
	movies = []
	for m in row:
		movies.append({'name':m[0], 'year':m[1], 'mid':m[2], 'role':m[3]})
	
	return render_to_response('person.html', locals())
