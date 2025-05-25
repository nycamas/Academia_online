from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Profesor'),
        ('student', 'Alumno'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    def is_teacher(self):
        return self.role == 'teacher'
    
    def is_student(self):
        return self.role == 'student'

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.CharField(max_length=50)  # Ej: "8 semanas", "3 meses"
    created_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    link = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('enrolled', 'Inscrito'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='enrolled')
    progress = models.IntegerField(default=0)  # Porcentaje de avance
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('course', 'student')
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Evaluation(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='evaluations')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return self.title

class Score(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='scores')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('evaluation', 'student')
    
    def __str__(self):
        return f"{self.student.username} - {self.evaluation.title}: {self.score}"
