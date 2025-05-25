from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import User, Course, Lesson, Enrollment, Evaluation, Score
from .forms import (
    UserRegistrationForm, UserProfileForm, CourseForm, LessonForm,
    EvaluationForm, ScoreForm, EnrollmentForm
)

def home(request):
    """Página principal con cursos destacados"""
    courses = Course.objects.all().order_by('-created_at')[:6]
    return render(request, 'index.html', {'courses': courses})

def login_view(request):
    """Vista de inicio de sesión"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'auth/login.html')

def register(request):
    """Registro de nuevos usuarios"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

@login_required
def dashboard(request):
    """Panel de control para profesores y alumnos"""
    user = request.user
    if user.is_teacher():
        # Vista para profesores
        courses = Course.objects.filter(teacher=user)
        return render(request, 'dashboard/teacher.html', {'courses': courses})
    else:
        # Vista para alumnos
        enrollments = Enrollment.objects.filter(student=user)
        return render(request, 'dashboard/student.html', {'enrollments': enrollments})

@login_required
def profile(request):
    """Perfil de usuario"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

def course_list(request):
    """Lista de todos los cursos disponibles"""
    query = request.GET.get('q', '')
    if query:
        courses = Course.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        courses = Course.objects.all()
    return render(request, 'course/list.html', {'courses': courses, 'query': query})

def course_detail(request, course_id):
    """Detalle de un curso específico"""
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    evaluations = course.evaluations.all()
    
    # Verificar si el usuario está inscrito
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            course=course, student=request.user
        ).exists()
    
    return render(request, 'course/detail.html', {
        'course': course,
        'lessons': lessons,
        'evaluations': evaluations,
        'is_enrolled': is_enrolled
    })

@login_required
def course_create(request):
    """Crear un nuevo curso (solo profesores)"""
    if not request.user.is_teacher():
        messages.error(request, 'Solo los profesores pueden crear cursos')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, 'Curso creado correctamente')
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm()
    
    return render(request, 'course/create.html', {'form': form})

@login_required
def course_edit(request, course_id):
    """Editar un curso existente (solo profesor del curso)"""
    course = get_object_or_404(Course, id=course_id)
    
    # Verificar permisos
    if course.teacher != request.user:
        messages.error(request, 'No tienes permiso para editar este curso')
        return redirect('course_detail', course_id=course.id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso actualizado correctamente')
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'course/create.html', {'form': form, 'course': course})

@login_required
def course_delete(request, course_id):
    """Eliminar un curso (solo profesor del curso)"""
    course = get_object_or_404(Course, id=course_id)
    
    # Verificar permisos
    if course.teacher != request.user:
        messages.error(request, 'No tienes permiso para eliminar este curso')
        return redirect('course_detail', course_id=course.id)
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Curso eliminado correctamente')
        return redirect('dashboard')
    
    return render(request, 'course/delete.html', {'course': course})

@login_required
def lesson_create(request, course_id):
    """Crear una nueva lección para un curso (solo profesor del curso)"""
    course = get_object_or_404(Course, id=course_id)
    
    # Verificar permisos
    if course.teacher != request.user:
        messages.error(request, 'No tienes permiso para añadir lecciones a este curso')
        return redirect('course_detail', course_id=course.id)
    
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, 'Lección creada correctamente')
            return redirect('course_detail', course_id=course.id)
    else:
        form = LessonForm()
    
    return render(request, 'lesson/create.html', {'form': form, 'course': course})

@login_required
def lesson_detail(request, lesson_id):
    """Ver detalle de una lección (solo usuarios inscritos o profesor)"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course
    
    # Verificar permisos
    if course.teacher != request.user:
        # Si no es el profesor, verificar inscripción
        if not Enrollment.objects.filter(course=course, student=request.user).exists():
            messages.error(request, 'Debes estar inscrito en este curso para ver las lecciones')
            return redirect('course_detail', course_id=course.id)
    
    return render(request, 'lesson/detail.html', {'lesson': lesson, 'course': course})

@login_required
def lesson_edit(request, lesson_id):
    """Editar una lección (solo profesor del curso)"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course
    
    # Verificar permisos
    if course.teacher != request.user:
        messages.error(request, 'No tienes permiso para editar esta lección')
        return redirect('lesson_detail', lesson_id=lesson.id)
    
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lección actualizada correctamente')
            return redirect('lesson_detail', lesson_id=lesson.id)
    else:
        form = LessonForm(instance=lesson)
    
    return render(request, 'lesson/create.html', {'form': form, 'course': course, 'lesson': lesson})

@login_required
def lesson_delete(request, lesson_id):
    """Eliminar una lección (solo profesor del curso)"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course
    
    # Verificar permisos
    if course.teacher != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta lección')
        return redirect('lesson_detail', lesson_id=lesson.id)
    
    if request.method == 'POST':
        course_id = course.id
        lesson.delete()
        messages.success(request, 'Lección eliminada correctamente')
        return redirect('course_detail', course_id=course_id)
    
    return render(request, 'lesson/delete.html', {'lesson': lesson, 'course': course})

@login_required
def evaluation_create(request, course_id):
    """Crear una nueva evaluación para un curso (solo profesor del curso)"""
    course = get_object_or_404(Course, id=course_id)
    
    # Verificar permisos
    if course.teacher != request.user:
        messages.error(request, 'No tienes permiso para añadir evaluaciones a este curso')
        return redirect('course_detail', course_id=course.id)
    
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.course = course
            evaluation.save()
            messages.success(request, 'Evaluación creada correctamente')
            return redirect('course_detail', course_id=course.id)
    else:
        form = EvaluationForm()
    
    return render(request, 'evaluation/create.html', {'form': form, 'course': course})

@login_required
def evaluation_detail(request, evaluation_id):
    """Ver detalle de una evaluación"""
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    course = evaluation.course
    
    # Verificar permisos
    if course.teacher != request.user:
        # Si no es el profesor, verificar inscripción
        if not Enrollment.objects.filter(course=course, student=request.user).exists():
            messages.error(request, 'Debes estar inscrito en este curso para ver las evaluaciones')
            return redirect('course_detail', course_id=course.id)
    
    # Si es profesor, mostrar todas las calificaciones
    if request.user.is_teacher():
        scores = Score.objects.filter(evaluation=evaluation)
        students = Enrollment.objects.filter(course=course).values_list('student', flat=True)
        students_without_score = User.objects.filter(id__in=students).exclude(
            id__in=scores.values_list('student', flat=True)
        )
    else:
        # Si es alumno, mostrar solo su calificación
        scores = Score.objects.filter(evaluation=evaluation, student=request.user)
        students_without_score = []
    
    return render(request, 'evaluation/detail.html', {
        'evaluation': evaluation,
        'course': course,
        'scores': scores,
        'students_without_score': students_without_score
    })

@login_required
def evaluation_edit(request, evaluation_id):
    """Editar una evaluación (solo profesor del curso)"""
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    course = evaluation.course
    
    # Verificar permisos
    if course.teacher != request.user:
        messages.error(request, 'No tienes permiso para editar esta evaluación')
        return redirect('evaluation_detail', evaluation_id=evaluation.id)
    
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evaluación actualizada correctamente')
            return redirect('evaluation_detail', evaluation_id=evaluation.id)
    else:
        form = EvaluationForm(instance=evaluation)
    
    return render(request, 'evaluation/create.html', {'form': form, 'course': course, 'evaluation': evaluation})

@login_required
def evaluation_delete(request, evaluation_id):
    """Eliminar una evaluación (solo profesor del curso)"""
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    course = evaluation.course
    
    # Verificar permisos
    if course.teacher != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta evaluación')
        return redirect('evaluation_detail', evaluation_id=evaluation.id)
    
    if request.method == 'POST':
        course_id = course.id
        evaluation.delete()
        messages.success(request, 'Evaluación eliminada correctamente')
        return redirect('course_detail', course_id=course_id)
    
    return render(request, 'evaluation/delete.html', {'evaluation': evaluation, 'course': course})

@login_required
def score_create(request, evaluation_id, student_id):
    """Asignar calificación a un alumno (solo profesor del curso)"""
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    student = get_object_or_404(User, id=student_id)
    course = evaluation.course
    
    # Verificar permisos
    if course.teacher != request.user:
        messages.error(request, 'No tienes permiso para asignar calificaciones')
        return redirect('evaluation_detail', evaluation_id=evaluation.id)
    
    # Verificar que el alumno esté inscrito en el curso
    if not Enrollment.objects.filter(course=course, student=student).exists():
        messages.error(request, 'El alumno no está inscrito en este curso')
        return redirect('evaluation_detail', evaluation_id=evaluation.id)
    
    # Verificar si ya existe una calificación
    score = Score.objects.filter(evaluation=evaluation, student=student).first()
    
    if request.method == 'POST':
        if score:
            form = ScoreForm(request.POST, instance=score)
        else:
            form = ScoreForm(request.POST)
        
        if form.is_valid():
            if not score:
                score = form.save(commit=False)
                score.evaluation = evaluation
                score.student = student
            else:
                score = form.save(commit=False)
            
            score.save()
            messages.success(request, 'Calificación asignada correctamente')
            return redirect('evaluation_detail', evaluation_id=evaluation.id)
    else:
        if score:
            form = ScoreForm(instance=score)
        else:
            form = ScoreForm()
    
    return render(request, 'score/create.html', {
        'form': form,
        'evaluation': evaluation,
        'student': student,
        'course': course
    })

@login_required
def score_edit(request, score_id):
    """Editar una calificación (solo profesor del curso)"""
    score = get_object_or_404(Score, id=score_id)
    evaluation = score.evaluation
    course = evaluation.course
    
    # Verificar permisos
    if course.teacher != request.user:
        messages.error(request, 'No tienes permiso para editar esta calificación')
        return redirect('evaluation_detail', evaluation_id=evaluation.id)
    
    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=score)
        if form.is_valid():
            form.save()
            messages.success(request, 'Calificación actualizada correctamente')
            return redirect('evaluation_detail', evaluation_id=evaluation.id)
    else:
        form = ScoreForm(instance=score)
    
    return render(request, 'score/create.html', {
        'form': form,
        'evaluation': evaluation,
        'student': score.student,
        'course': course,
        'score': score
    })

@login_required
def enroll(request, course_id):
    """Inscribirse en un curso (solo alumnos)"""
    course = get_object_or_404(Course, id=course_id)
    
    # Verificar que el usuario sea alumno
    if not request.user.is_student():
        messages.error(request, 'Solo los alumnos pueden inscribirse en cursos')
        return redirect('course_detail', course_id=course.id)
    
    # Verificar si ya está inscrito
    if Enrollment.objects.filter(course=course, student=request.user).exists():
        messages.info(request, 'Ya estás inscrito en este curso')
        return redirect('course_detail', course_id=course.id)
    
    # Crear inscripción
    enrollment = Enrollment(course=course, student=request.user)
    enrollment.save()
    
    messages.success(request, f'Te has inscrito correctamente en el curso "{course.title}"')
    return redirect('course_detail', course_id=course.id)

@login_required
def enrollment_cancel(request, enrollment_id):
    """Cancelar inscripción en un curso"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    # Verificar permisos
    if enrollment.student != request.user:
        messages.error(request, 'No tienes permiso para cancelar esta inscripción')
        return redirect('dashboard')
    
    if request.method == 'POST':
        course_id = enrollment.course.id
        enrollment.status = 'cancelled'
        enrollment.save()
        messages.success(request, 'Inscripción cancelada correctamente')
        return redirect('dashboard')
    
    return render(request, 'enrollment/cancel.html', {'enrollment': enrollment})
