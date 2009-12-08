from moviemate import models
from moviemate import forms as myForms
from django.shortcuts import render_to_response
from django.db import connection, transaction
from math import ceil
from django.template.context import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect

def get_movie_info(mid):
	try:
		cursor.execute("""select m.name, m.year, m.avgRating, 
				m.numOfRatings, g.genre
				from Movie m, Genre g, isType i
				where m.mid='%s' and i.mid=m.mid and g.gid = i.gid""" % mid)
		row = cursor.fetchone()
		movie = {'mid':mid, 'name':row[0], 'year':row[1], 'avgrating':row[2], 'numofratings':row[3], 'genre':row[4]}
	except:
		pass


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
		#stupid hack for missing genre info
		try:
			cursor.execute("""select m.name, m.year, m.avgRating, 
					m.numOfRatings, m.MPAA, g.genre
					from Movie m, Genre g, isType i
					where m.mid='%s' and i.mid=m.mid and g.gid = i.gid""" % mid)
			row = cursor.fetchone()
			movie = {'mid':mid, 'name':row[0], 'year':row[1], 'avgrating':row[2], 'numofratings':row[3], 'MPAA':row[4], 'genre':row[5]}

		except:
			cursor.execute("""select m.name, m.year, m.avgRating, m.numOfRatings, m.MPAA
					from Movie m
					where m.mid='%s'""" % mid)
			row = cursor.fetchone()
			movie = {'mid':mid, 'name':row[0], 'year':row[1], 'avgrating':row[2], 'numofratings':row[3], 'MPAA':row[4]}

	
	
	
		#get director info
		cursor.execute("""select p.name, v.role from Person p, isInvolved v where
				v.mid = '%s' and v.role='Director' and p.pid = v.pid""" % mid)
		row = cursor.fetchone()
		try:
			director = {'name':row[0]}
		except:
			director = {}
		
		#get cast info
		cursor.execute("""select p.name, v.role, p.pid from Person p, isInvolved v where
				v.mid = '%s' and v.role <> 'Director' and p.pid = v.pid""" % mid)
		row = cursor.fetchall()
		cast = []
		try:
			for p in row:
				cast.append({'name':p[0], 'role':p[1], 'pid':p[2]})
		except:
			pass
			
		#get reviews
		cursor.execute("""select u.name, r.summary, r.timestamp from Users u, Review r where r.mid = '%s'
				and u.user_id = r.user_id""" % mid)
		row = cursor.fetchall()
		reviews = []
		
		try:
			for r in row:
				reviews.append({'username':r[0], 'summary':r[1], 'timestamp':r[2]})
		except:
			pass
	cursor.close()
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
	
	cursor.close()
	return render_to_response('person.html', locals())
	
def basic_search(request, type, query, count=10):
	if type == 'movie':
		cursor = connection.cursor()
		cursor.execute("""select m.mid, m.name, m.year, m.avgRating
				from Movie m
				where m.name like '%%"""+query+"""%%' 
				order by m.numOfRatings desc limit 25""")
		
		numResults = cursor.rowcount
		row = cursor.fetchall()
		
	elif type == 'person':
		cursor = connection.cursor()
		cursor.execute("""select p.pid, p.name from Person p
				where p.name = '%s'""" % query)
		numResults = cursor.rowcount
		row = cursor.fetchmany(count)
	elif type == 'friend':
		cursor = connection.cursor()
		cursor.execute("""select u.user_id, u.name, u.login
				from Users u
				where (u.name like '%%"""+query+"""%%')
				or (u.login like '%%"""+query+"""%%')
				""")
		numResults = cursor.rowcount
		row = cursor.fetchmany(count)
	
	results = []
	for r in row:
		results.append({'type':type, 'id':r[0], 'name':r[1], 'data':r[2:]})
	
	cursor.close()
	numPages = int(ceil(numResults / 10.0))
	return render_to_response('testresults.html', locals())

def advance_search(request):
	user, radio_btn, query, gt, lt = "", "", "", "", ""
	if request.POST:
		if user.age < 13:
			mpaa = 2
		if user.age < 14:
			mpaa = 3
		elif user.age < 18:
			mpaa = 4
		elif user == None:
			mpaa = 4
		else:
		    mpaa = 7
		cursor = connection.cursor()
		if radio_btn == 1:   #Movie Title Search
			cursor.execute("""SELECT m.name, m.year, m.avgRating, m.numOfRatings, m.MPAA, g.genre FROM Movie m, Genre g, isType i
					where m.name LIKE '%%s%' and i.mid=m.mid and g.gid = i.gid and m.MPAA < %s""" % query, mpaa)
			row = cursor.fetchall()
			movies = []
			for r in row:
				movies.append({'name':r[0], 'year':r[1], 'avgRating':r[2], 'numOfRatings':r[3], 'MPAA':r[4], 'genre':r[5]})
			
		elif radio_btn == 2:  #User Search
			cursor.execute("""select u.user_id, u.username, u.name, u.age, u.state, u.city
					from Users u where u.username LIKE '%%s%' or u.name LIKE '%%s%'""" % query)
			
			row = cursor.fetchall()
			user = []
			for r in row:
				user.append({'username':r[0], 'name':r[1],'age':r[1], 'state':r[1], 'city':r[2]})
			
		elif radio_btn == 3:  #Actor/Actress or Directors Search
			cursor.execute("""select p.pid, p.name, p.age, p.gender
					from Person p where p.name LIKE '%%s%'""" % query)
			row = cursor.fetchall()
			person = []
			for r in row:
				person.append({'name':r[0], 'age':r[1], 'gender':r[2]})
			
		elif radio_btn == 5:  #list of actors, actresses, or directors
			quaryset = query.split(',')
			
			person = ''
			for q in quaryset:
				person += """p2.name = '%s' or """ % q
			person = person.rstrip(' or ')
			
	   
			cursor.execute("""SELECT DISTINCT m.mid, m.name, m.year, m.avgRating, m.numOfRatings, m.MPAA, g.genre
					FROM Movie m, Genre g, isType i, isInvolved iv, Person p 
					WHERE m.mid = iv.mid AND p.pid = iv.pid AND i.mid = m.mid AND g.gid = i.gid and m.MPAA < %s AND p.pid IN 
					(SELECT p2.pid FROM Person p2 WHERE %s""" % mpaa, person )
			row = cursor.fetchall()
			movies = []
			for r in row:
				movies.append({'name':r[0], 'year':r[1], 'avgRating':r[2], 'numOfRatings':r[3], 'MPAA':r[4], 'genre':r[5]})
						   
		elif radio_btn == 6:  #list of actors, actresses ALL INVOLVED IN MOVIE
			quaryset = query.split(',')
			
			person = ''
			for q in quaryset:
				person += """p2.name = '%s' or """ % q
			person = person.rstrip(' or ')
	
			cursor.execute("""SELECT m.name, m.year, m.avgRating, m.numOfRatings, m.MPAA, g.genre
					FROM Movie m, Genre g, isType i, isInvolved iv, Person p 
					WHERE m.mid = iv.mid AND p.pid = iv.pid AND i.mid = m.mid AND g.gid = i.gid and m.MPAA < %s AND p.pid IN 
					(SELECT p2.pid FROM Person p2 WHERE %s""" % mpaa, person )
			
			row = cursor.fetchall()
			movies = []
			for r in row:
				movies.append({'name':r[0], 'year':r[1], 'avgRating':r[2], 'numOfRatings':r[3], 'MPAA':r[4], 'genre':r[5]})
			
		elif radio_btn == 7:  #one director, return actors and actresses
			cursor.execute("""SELECT p.pid, p.name, p.age, p.gender, iv.role
					FROM Person p, Movie m, isInvolved iv
					WHERE p.pid = iv.pid and m.mid = iv.mid and (iv.role = 'Actor' or iv.role = 'Actress') and m.MPAA < %s and m.mid IN
						(SELECT m2.mid 
						FROM Person p2, Movie m2, isInvolved iv2 
						WHERE m2.mid = iv2.mid and p2.pid = iv2.pid and p2.name = '%s' and iv2.role = 'Director'""" % mpaa, query)
			
		elif radio_btn == 8:  #Movies released in this year.
			cursor.execute("""SELECT m.name, m.year, m.avgRating, m.numOfRatings, m.MPAA, g.genre
					FROM Movie m, Genre g, isType i
					WHERE m.year = '%s' and i.mid=m.mid and g.gid = i.gid and m.MPAA < %s""" % query, mpaa)
			row = cursor.fetchall()
			movies = []
			for r in row:
				movies.append({'name':r[0], 'year':r[1], 'avgRating':r[2], 'numOfRatings':r[3], 'MPAA':r[4], 'genre':r[5]})
			
		elif radio_btn == 9:  #Movies who's rating is in a range
			cursor.execute("""SELECT m.name, m.year, m.avgRating, m.numOfRatings, m.MPAA, g.genre
					FROM Movie m, Genre g, isType i
					WHERE i.mid = m.mid and g.gid = i.gid and m.avgRating >= %s and m.avgRating <= %s and m.MPAA < %s""" % gt, lt, mpaa)
			
		elif radio_btn == 10:  #Top n rated movies.
			cursor.execute("""SELECT m.name, m.year, m.avgRating, m.numOfRatings, m.MPAA, g.genre
					FROM Movie m, Genre g, isType i
					WHERE m.MPAA < %s
					LIMIT '%s'""" % mpaa, query)
			row = cursor.fetchall()
			movies = []
			for r in row:
				movies.append({'name':r[0], 'year':r[1], 'avgRating':r[2], 'numOfRatings':r[3], 'MPAA':r[4], 'genre':r[5]})
			return render_to_response('testresults.html', locals())
	else: #GET
	   return render_to_response('search.html', locals())
		   
def edit_profile(request, user_id):
	if request.is_ajax():
		if request.method == 'POST':
			form = ProfileForm(request.POST)
			if(form.isValid):
				form.save()
		else:
			return render_to_response('editprofile.html', {'form': form,})
		
def review(request):
	if request.method == 'POST':
		form = myForms.ReviewForm(request.POST)
		if(form.isValid):
			form.save()
	else:
		form = myForms.ReviewForm()
		return render_to_response('review.html', locals())
	

	
def ajax_top_five(request):
	if request.is_ajax():
		cursor = connection.cursor()
		cursor.execute("""select m.name, m.year, m.mid
				from TopFiftyMovies m
				limit 5""")
		row = cursor.fetchall()
		movies = []
		for r in row:
			movies.append({'name':r[0], 'year':r[1], 'mid':r[2]})
		template = "top5.html"
		data = {'results':movies}
			
		return render_to_response(template, data )
		
def login(request):
	if request.POST:
		user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
		if user != None and user.is_active:
			auth.login(request, user)
			return HttpResponseRedirect('/')
		else: #invalid login or inactive account
			return HttpResponseRedirect('/search/movie/invalid')
	else: #request.GET
		return render_to_response('login.html', locals())