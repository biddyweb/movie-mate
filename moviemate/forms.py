from django import newforms as forms

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

class ProfileForm(forms.Form):
    name = forms.CharField(label="Full Name")
    age = forms.IntegerField(required=False, label="Age")
    country = forms.CharField(required=False, label="Country", initial="United States")
    state = forms.CharField(required=False, choices=STATES, label="State")
    city = forms.CharField(required=False, label="City")
    gender = forms.CharField(choices=('M','F'), label="Gender")
    school = forms.CharField(choices=self.get_schools, label="School")
    picture = forms.ImageField()
    file = forms.FilePathField()

    def get_schools(self):
        return cursor.execute("""SELECT DISTINCT school FROM Users""")
    
class ReviewForm(forms.Form):
    review = forms.CharField(required=True, widget=forms.Textarea)
    
class RatingForm(forms.Form):
    rating = forms.IntegerField(required=True, min_value=0, max_value=10)
