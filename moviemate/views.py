from moviemate.models import auth_user_ext, Users
from moviemate import queries
from moviemate import forms as myForms
from django.shortcuts import render_to_response
from django.db import connection, transaction
from math import ceil
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login, logout
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
	
def friend_page(request, user_id):
	cursor = connection.cursor()
	cursor.execute("""select f.name, f.city, f.state, f.school, 
			f.age from Users f
			where f.user_id = %s """ % user_id)
	r = cursor.fetchone()
	friend = {'name':r[0], 'city':r[1], 'state':r[2], 'school':r[3], 'age':r[4]}
	
	cursor.execute("""select f.name, f.user_id from Users f, isFriend i
		where (i.uid1 = %s and f.user_id = i.uid2) or (i.uid2 = %s and f.user_id = uid1)""" % (user_id, user_id))
	row = cursor.fetchall()
	friends = []
	for r in row:
		friends.append({'name':r[0], 'id':r[1]})
	
	return render_to_response('friend.html', locals())
	
def basic_search(request, type, query, count=25):
	if type == 'movie':
		cursor = connection.cursor()
		cursor.execute("""select m.mid, m.name, m.year, m.MPAA, m.avgRating
				from Movie m
				where m.name like '%%"""+query+"""%%' 
				order by m.numOfRatings desc limit 25""")
		
		numResults = cursor.rowcount
		row = cursor.fetchall()
		
		movies = []
		for r in row:
			movies.append({'mid':r[0], 'name':r[1], 'year':r[2], 'MPAA':r[3], 'avgRating':r[4]})
		return render_to_response('movieResults.html', locals())
		
	elif type == 'person':
		cursor = connection.cursor()
		cursor.execute("""select distinct p.name, p.pid from Person p
				where p.name = '%s'""" % query)
		numResults = cursor.rowcount
		row = cursor.fetchmany(count)
		
		persons = []
		for p in row:
			persons.append({'pid':p[1], 'name':p[0]})
		return render_to_response('personResults.html', locals())
		
	elif type == 'friend':
		cursor = connection.cursor()
		cursor.execute("""select u.user_id, u.name, u.login
				from Users u
				where (u.name like '%%"""+query+"""%%')
				or (u.login like '%%"""+query+"""%%')
				""")
		numResults = cursor.rowcount
		row = cursor.fetchmany(count)
		friends = []
		for r in row:
			friends.append({'user_id':r[0], 'name':r[1], 'login':r[2]})
		return render_to_response("friendResults.html", locals())
	
	cursor.close()
	numPages = int(ceil(numResults / 10.0))
	return render_to_response('testresults.html', locals())

def advance_search(request):

	db_user = Users.objects.get(user_id=request.user.get_profile().db_user)

	if request.POST:
		post = request.POST		
		if request.user.is_authenticated():
			#MPAA G, PG, PG-13, NC-17, R, NR, ADULT
			if db_user.age < 10:
				mpaa = 1
			elif db_user.age < 13:
				mpaa = 2
			elif db_user.age < 17:
				mpaa = 3
			elif db_user.age < 18:
				mpaa = 4
			elif db_user.age < 19:
				mpaa = 5
			else:
				mpaa = 7
		else:
		    mpaa = 1
		    
		cursor = connection.cursor()
		
		if post['searchOp'] == '1':   #Movie Title Search
			
			row = queries.find_movie_by_title(post['title'], mpaa)
			movies = []
			for r in row:
				movies.append({'mid':r[0], 'name':r[1], 'year':r[2], 'avgRating':r[3], 'numOfRatings':r[4], 'MPAA':r[5]})
			numResults = len(movies)
			return render_to_response('movieResults.html', locals())
			
		elif post['searchOp'] == '2':  #User Search
			
			row = queries.find_user(post['findUser'])
			friends = []
			for r in row:
				friends.append({'user_id':r[0], 'login':r[1], 'name':r[2]})
			numResults = len(friends)
			return render_to_response('friendResults.html', locals())
		
		####
		elif post['searchOp'] == '3':  #Actor/Actress or Directors Search
			row = queries.find_person(post['findPerson'])
			persons = []
			for r in row:
				persons.append({'pid':r[0], 'name':r[1]})
			numResults = len(persons)
			return render_to_response('personResults.html', locals())
			
		####
		elif post['searchOp'] == '4':  #list of actors, actresses, or directors
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
		
		####				   
		elif post['searchOp'] == '5':  #list of actors, actresses ALL INVOLVED IN MOVIE
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
		
		####	
		elif post['searchOp'] == '6':  #one director, return actors and actresses
			cursor.execute("""SELECT p.pid, p.name, p.age, p.gender, iv.role
					FROM Person p, Movie m, isInvolved iv
					WHERE p.pid = iv.pid and m.mid = iv.mid and (iv.role = 'Actor' or iv.role = 'Actress') and m.MPAA < %s and m.mid IN
						(SELECT m2.mid 
						FROM Person p2, Movie m2, isInvolved iv2 
						WHERE m2.mid = iv2.mid and p2.pid = iv2.pid and p2.name = '%s' and iv2.role = 'Director'""" % mpaa, query)
		
		####
		elif post['searchOp'] == '7':  #Movies released in this year.
			year1 = post['year1'];
			year2 = post['year2'];
			if year2 == '':
				year2 = None
			elif year2 < year1:
			    temp = year2
			    year2 = year1
			    year1 = temp
			
			row = queries.find_movie_by_year(year1, year2, mpaa)
			movies = []
			for r in row:
				movies.append({'mid':r[0], 'name':r[1], 'year':r[2], 'avgRating':r[3], 'numOfRatings':r[4], 'MPAA':r[5]})
			numResults = len(movies)
			return render_to_response('movieResults.html', locals())
		
		####
		elif post['searchOp'] == '8':  #Movies who's rating is in a range
			rating1 = post['rating1'];
			rating2 = post['rating2'];
			if rating2 == '':
				rating1 = float(rating1)
				rating2 = None
			else:
				rating1 = float(rating1)
				rating2 = float(rating2)
				if rating2 < rating1:
					temp = rating2
			    	rating2 = rating1
			    	rating1 = temp
			
			row = queries.find_movie_by_rating(rating1, rating2, mpaa)
			movies = []
			for r in row:
				movies.append({'mid':r[0], 'name':r[1], 'year':r[2], 'avgRating':r[3], 'numOfRatings':r[4], 'MPAA':r[5]})
			numResults = len(movies)
			return render_to_response('movieResults.html', locals())
		
		####	
		elif post['searchOp'] == '9':  #Top n rated movies.
			row = queries.top_k_search(post['value_k'], mpaa)
			movies = []
			for r in row:
				movies.append({'mid':r[0], 'name':r[1], 'year':r[2], 'avgRating':r[3], 'numOfRatings':r[4], 'MPAA':r[5]})
			numResults = len(movies)
			return render_to_response('movieResults.html', locals())
	else:
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
		
def myLogin(request):
	if request.method == 'POST':
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/home/')
			else: #inactive account
				error = "This account has been disabled."
				return render_to_response('welcome.html', locals())
		else: #invalid login
			error = "Invalid username or password."
			return render_to_response('welcome.html', locals())
	else:
		return render_to_response('login.html')
	
		
def myLogout(request):
	logout(request)
	return HttpResponseRedirect('/')
	
	
def welcome(request):
	if request.user.is_authenticated():
		return render_to_response('home.html', locals())
	else:
		return render_to_response('welcome.html', locals())
	
def home(request):
	db_user = models.Users.objects.get(user_id=request.user.get_profile().db_user)
	return render_to_response('home.html', locals())