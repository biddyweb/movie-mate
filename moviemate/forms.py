from moviemate.models import Users
from django import forms

STATES=( 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
         'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 
         'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 
         'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 
         'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 
         'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 
         'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 
         'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 
         'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming')

def handle_uploaded_file(f):
    destination = open('some/file/name.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

#class ProfileForm(forms.Form):
#    user = Users.objects.get(pk=489512)
#    name = forms.CharField(label="Full Name", initial=user['name'])
#    age = forms.IntegerField(required=False, label="Age", initial=user['age'])
#    country = forms.CharField(required=False, label="Country", initial=user['country'])
#    state = forms.CharField(required=False, choices=STATES, label="State", initial=user['state'])
#    city = forms.CharField(required=False, label="City", initial=user['city'])
#    gender = forms.CharField(choices=('M','F'), label="Gender", initial=user['gender'])
#    school = forms.CharField(choices=self.get_schools(), label="School", initial=user['school'])
#    picture = forms.ImageField()
#    file = forms.FilePathField()
#
#    def get_schools(self):
#        return cursor.execute("""SELECT DISTINCT school FROM Users""")
    
class ReviewForm(forms.Form):
    review = forms.CharField(required=True, widget=forms.Textarea)
    
class RatingForm(forms.Form):
    rating = forms.IntegerField(required=True, min_value=0, max_value=10)
