from moviemate import models
from moviemate import queries
from moviemate import forms as myForms
from django.shortcuts import render_to_response
from django.db import connection, transaction
from math import ceil
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


def admin_query(request):
	if request.user.is_superuser:
		if request.POST:
			query = request.POST['adminSQL']
			result = queries.sql_query(query)
			count = len(result)
			return render_to_response('adminSQL.html', locals())
				
		else:
			return render_to_response('adminSQL.html', locals())
	else:
		return HttpResponseRedirect('/')

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


def movie_page(request, mid=None):
	db_user = models.Users.objects.get(user_id=request.user.get_profile().db_user)
	if mid == None:
		movie = models.Movie.objects.filter(name=request.name, year=request.year).values()
	else:	
		if request.method == 'POST':
			try:
				review = request.POST['review']
			except:
				review = ''
			if review <> '' and len(review) > 2:
				queries.add_review(db_user.user_id, mid, review)
	
		cursor = connection.cursor()
		#movie = models.Movie.objects.get(mid=mid)
		#genre = models.Istype.objects.get(mid=mid)
		#cast = models.Isinvolved.objects.filter(mid=mid)
		#director = models.Isinvolved.objects.filter(mid=mid, role='Director')
					
		#get movie info
		#stupid hack for missing genre info
		cursor.execute("""select m.name, m.year, m.avgRating, m.numOfRatings, m.MPAA, g.genre
						  from Movie m, Genre g, isType i
						  where m.mid='%s' and i.mid=m.mid and g.gid = i.gid""" % mid)
		row = cursor.fetchone()
		try:
			movie = {'mid':mid, 'name':row[0], 'year':row[1], 'avgrating':row[2], 'numofratings':row[3], 'MPAA':row[4], 'genre':row[5]}
		except:
			movie = {'mid':mid, 'name':row[0], 'year':row[1], 'avgrating':row[2], 'numofratings':row[3], 'MPAA':row[4]}

		#get rating info
		cursor.execute("""SELECT rating FROM Rates WHERE user_id = '%s'""" % db_user.user_id)
		row = cursor.fetchone()

		rating = {'rate1':False, 'rate2':False, 'rate3':False, 'rate4':False, 'rate5':False, 
				  'rate6':False, 'rate7':False, 'rate8':False, 'rate9':False, 'rate10':False}
		try:
			if row[0] == 1: rating['rate1'] = True
			elif row[0] == 2: rating['rate2'] = True
			elif row[0] == 3: rating['rate3'] = True
			elif row[0] == 4: rating['rate4'] = True
			elif row[0] == 5: rating['rate5'] = True
			elif row[0] == 6: rating['rate6'] = True
			elif row[0] == 7: rating['rate7'] = True
			elif row[0] == 8: rating['rate8'] = True
			elif row[0] == 9: rating['rate9'] = True
			elif row[0] == 10: rating['rate10'] = True
		except:
			rating = False
			
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
		row = queries.get_reviews(mid)
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

	db_user = models.Users.objects.get(user_id=request.user.get_profile().db_user)

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
		
		#
		#Movie Title Search
		#
		if post['searchOp'] == '1':   
			
			row = queries.find_movie_by_title(post['title'], mpaa)
			movies = []
			for r in row:
				movies.append({'mid':r[0], 'name':r[1], 'year':r[2], 'avgRating':r[3], 'numOfRatings':r[4], 'MPAA':r[5]})
			numResults = len(movies)
			return render_to_response('movieResults.html', locals())
		
		#
		#User Search
		#	
		elif post['searchOp'] == '2':  
			
			row = queries.find_user(post['findUser'])
			friends = []
			for r in row:
				friends.append({'user_id':r[0], 'login':r[1], 'name':r[2]})
			numResults = len(friends)
			return render_to_response('friendResults.html', locals())
		
		#
		#Actor/Actress or Directors Search
		#
		elif post['searchOp'] == '3':  
			row = queries.find_person(post['findPerson'])
			persons = []
			for r in row:
				persons.append({'pid':r[0], 'name':r[1]})
			numResults = len(persons)
			return render_to_response('personResults.html', locals())
			
		#
		# Movies with at least one of the listed actors, actresses, or directors
		#
		elif post['searchOp'] == '4':
			people = [ post['person1'], post['person2'], post['person3'], post['person4'], post['person5'] ]
					
			personList = []
			for p in people:
				if p <> '':
					personList.append(p)
			
			if personList == []:
			     return render_to_response('search.html')
			    
			row = queries.find_all_movies_by_person_list(personList, mpaa)
			movies = []
			for r in row:
				movies.append({'mid':r[0], 'name':r[1], 'year':r[2], 'avgRating':r[3], 'numOfRatings':r[4], 'MPAA':r[5]})
			numResults = len(movies)
			return render_to_response('movieResults.html', locals())
		
		####
		# Movies with ALL of the listed actors, actresses, or directors
		#			   
		elif post['searchOp'] == '5':
			people = [ post['person1'], post['person2'], post['person3'], post['person4'], post['person5'] ]
					
			personList = []
			for p in people:
				if p <> '':
					personList.append(p)
					
			if personList == []:
			     return render_to_response('search.html')
			    
			row = queries.find_movie_by_all_persons(personList, mpaa)
			movies = []
			for r in row:
				movies.append({'mid':r[0], 'name':r[1], 'year':r[2], 'avgRating':r[3], 'numOfRatings':r[4], 'MPAA':r[5]})
			numResults = len(movies)
			return render_to_response('movieResults.html', locals())
		
		#
		# Actors and Actresses that worked with a given Director
		#	
		elif post['searchOp'] == '6':  
			row = queries.find_cast_for_director(post['director'])
			persons = []
			for r in row:
				persons.append({'pid':r[0], 'name':r[1]})
			numResults = len(persons)
			return render_to_response('personResults.html', locals())
			
		#
		# Movies released in year range.
		#
		elif post['searchOp'] == '7':
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
		#
		# Movies within rating range
		#
		elif post['searchOp'] == '8':
			rating1 = post['rating1'];
			rating2 = post['rating2'];
			if rating2 == '':
				rating1 = float(rating1)
				rating2 = None
			else:
				rating1 = float(rating1)
				rating2 = float(rating2)
				if rating2 < rating1:
					n_temp = rating2
					rating2 = rating1
					rating1 = n_temp

			row = queries.find_movie_by_rating(rating1, rating2, mpaa)
			movies = []
			for r in row:
				movies.append({'mid':r[0], 'name':r[1], 'year':r[2], 'avgRating':r[3], 'numOfRatings':r[4], 'MPAA':r[5]})
			numResults = len(movies)
			return render_to_response('movieResults.html', locals())
		#
		#Top n rated movies.
		#
		elif post['searchOp'] == '9':
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