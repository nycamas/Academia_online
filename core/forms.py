from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Course, Lesson, Evaluation, Score, Enrollment

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'duration', 'link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_url', 'order']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['title', 'description', 'due_date', 'max_score']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course']
