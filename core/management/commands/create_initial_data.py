from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Course, Lesson, Evaluation, Enrollment, Score
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea datos iniciales para la aplicación'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creando datos iniciales...')
        
        # Crear usuarios profesores
        if not User.objects.filter(username='profesor1').exists():
            profesor1 = User.objects.create_user(
                username='profesor1',
                email='profesor1@academia.com',
                password='academia2025',
                first_name='Juan',
                last_name='García',
                role='teacher'
            )
            self.stdout.write(self.style.SUCCESS(f'Profesor creado: {profesor1.username}'))
        else:
            profesor1 = User.objects.get(username='profesor1')
            
        if not User.objects.filter(username='profesor2').exists():
            profesor2 = User.objects.create_user(
                username='profesor2',
                email='profesor2@academia.com',
                password='academia2025',
                first_name='María',
                last_name='López',
                role='teacher'
            )
            self.stdout.write(self.style.SUCCESS(f'Profesor creado: {profesor2.username}'))
        else:
            profesor2 = User.objects.get(username='profesor2')
        
        # Crear usuarios alumnos
        alumnos = []
        for i in range(1, 6):
            if not User.objects.filter(username=f'alumno{i}').exists():
                alumno = User.objects.create_user(
                    username=f'alumno{i}',
                    email=f'alumno{i}@academia.com',
                    password='academia2025',
                    first_name=f'Alumno {i}',
                    last_name=f'Apellido {i}',
                    role='student'
                )
                alumnos.append(alumno)
                self.stdout.write(self.style.SUCCESS(f'Alumno creado: {alumno.username}'))
            else:
                alumnos.append(User.objects.get(username=f'alumno{i}'))
        
        # Crear cursos
        cursos_data = [
            {
                'title': 'Introducción a la Programación',
                'description': 'Curso básico para aprender los fundamentos de la programación. Aprenderás lógica de programación, estructuras de datos y algoritmos básicos.',
                'duration': '8 semanas',
                'teacher': profesor1
            },
            {
                'title': 'Desarrollo Web con HTML y CSS',
                'description': 'Aprende a crear sitios web desde cero utilizando HTML5 y CSS3. Curso práctico con múltiples proyectos.',
                'duration': '6 semanas',
                'teacher': profesor1
            },
            {
                'title': 'Marketing Digital',
                'description': 'Estrategias de marketing en redes sociales, SEO, SEM y análisis de datos para mejorar la presencia online de tu negocio.',
                'duration': '10 semanas',
                'teacher': profesor2
            },
            {
                'title': 'Diseño Gráfico para Principiantes',
                'description': 'Fundamentos de diseño gráfico, uso de herramientas profesionales y creación de proyectos visuales atractivos.',
                'duration': '12 semanas',
                'teacher': profesor2
            }
        ]
        
        cursos = []
        for curso_data in cursos_data:
            curso, created = Course.objects.get_or_create(
                title=curso_data['title'],
                defaults={
                    'description': curso_data['description'],
                    'duration': curso_data['duration'],
                    'teacher': curso_data['teacher']
                }
            )
            cursos.append(curso)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Curso creado: {curso.title}'))
            else:
                self.stdout.write(f'Curso ya existente: {curso.title}')
        
        # Crear lecciones
        lecciones_data = [
            # Curso 1: Introducción a la Programación
            {
                'course': cursos[0],
                'title': 'Fundamentos de la programación',
                'content': 'En esta lección aprenderás los conceptos básicos de la programación, como variables, tipos de datos y operadores.',
                'order': 1
            },
            {
                'course': cursos[0],
                'title': 'Estructuras de control',
                'content': 'Aprenderás a utilizar condicionales (if-else) y bucles (for, while) para controlar el flujo de ejecución de tus programas.',
                'order': 2
            },
            {
                'course': cursos[0],
                'title': 'Funciones y procedimientos',
                'content': 'En esta lección veremos cómo crear y utilizar funciones para organizar y reutilizar código.',
                'video_url': 'https://www.youtube.com/watch?v=example1',
                'order': 3
            },
            
            # Curso 2: Desarrollo Web con HTML y CSS
            {
                'course': cursos[1],
                'title': 'Introducción a HTML5',
                'content': 'Aprenderás la estructura básica de un documento HTML y las etiquetas más importantes.',
                'order': 1
            },
            {
                'course': cursos[1],
                'title': 'Estilos con CSS3',
                'content': 'En esta lección veremos cómo dar estilo a nuestras páginas web utilizando CSS3.',
                'video_url': 'https://www.youtube.com/watch?v=example2',
                'order': 2
            },
            
            # Curso 3: Marketing Digital
            {
                'course': cursos[2],
                'title': 'Fundamentos del Marketing Digital',
                'content': 'Introducción a los conceptos básicos del marketing digital y su importancia en la actualidad.',
                'order': 1
            },
            {
                'course': cursos[2],
                'title': 'Estrategias en Redes Sociales',
                'content': 'Aprenderás a crear y gestionar campañas efectivas en las principales redes sociales.',
                'video_url': 'https://www.youtube.com/watch?v=example3',
                'order': 2
            },
            
            # Curso 4: Diseño Gráfico para Principiantes
            {
                'course': cursos[3],
                'title': 'Principios básicos del diseño',
                'content': 'Conocerás los fundamentos del diseño gráfico: color, tipografía, composición y balance.',
                'order': 1
            },
            {
                'course': cursos[3],
                'title': 'Introducción a herramientas de diseño',
                'content': 'Aprenderás a utilizar las principales herramientas de diseño gráfico del mercado.',
                'video_url': 'https://www.youtube.com/watch?v=example4',
                'order': 2
            }
        ]
        
        for leccion_data in lecciones_data:
            leccion, created = Lesson.objects.get_or_create(
                course=leccion_data['course'],
                title=leccion_data['title'],
                defaults={
                    'content': leccion_data['content'],
                    'video_url': leccion_data.get('video_url'),
                    'order': leccion_data['order']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Lección creada: {leccion.title}'))
            else:
                self.stdout.write(f'Lección ya existente: {leccion.title}')
        
        # Crear evaluaciones
        now = timezone.now()
        evaluaciones_data = [
            # Curso 1: Introducción a la Programación
            {
                'course': cursos[0],
                'title': 'Examen parcial',
                'description': 'Evaluación de los conceptos básicos de programación vistos hasta ahora.',
                'due_date': now + timedelta(days=15),
                'max_score': 10.0
            },
            {
                'course': cursos[0],
                'title': 'Proyecto final',
                'description': 'Desarrollo de una aplicación sencilla aplicando todos los conceptos aprendidos en el curso.',
                'due_date': now + timedelta(days=30),
                'max_score': 20.0
            },
            
            # Curso 2: Desarrollo Web con HTML y CSS
            {
                'course': cursos[1],
                'title': 'Práctica HTML',
                'description': 'Creación de una página web estática utilizando HTML5.',
                'due_date': now + timedelta(days=10),
                'max_score': 10.0
            },
            
            # Curso 3: Marketing Digital
            {
                'course': cursos[2],
                'title': 'Plan de marketing',
                'description': 'Desarrollo de un plan de marketing digital para un negocio ficticio.',
                'due_date': now + timedelta(days=20),
                'max_score': 15.0
            },
            
            # Curso 4: Diseño Gráfico para Principiantes
            {
                'course': cursos[3],
                'title': 'Diseño de logotipo',
                'description': 'Creación de un logotipo para una marca ficticia aplicando los principios de diseño aprendidos.',
                'due_date': now + timedelta(days=25),
                'max_score': 10.0
            }
        ]
        
        evaluaciones = []
        for eval_data in evaluaciones_data:
            evaluacion, created = Evaluation.objects.get_or_create(
                course=eval_data['course'],
                title=eval_data['title'],
                defaults={
                    'description': eval_data['description'],
                    'due_date': eval_data['due_date'],
                    'max_score': eval_data['max_score']
                }
            )
            evaluaciones.append(evaluacion)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Evaluación creada: {evaluacion.title}'))
            else:
                self.stdout.write(f'Evaluación ya existente: {evaluacion.title}')
        
        # Crear inscripciones
        inscripciones_data = [
            {'student': alumnos[0], 'course': cursos[0], 'status': 'enrolled', 'progress': 60},
            {'student': alumnos[0], 'course': cursos[1], 'status': 'enrolled', 'progress': 30},
            {'student': alumnos[1], 'course': cursos[0], 'status': 'enrolled', 'progress': 75},
            {'student': alumnos[1], 'course': cursos[2], 'status': 'enrolled', 'progress': 40},
            {'student': alumnos[2], 'course': cursos[1], 'status': 'enrolled', 'progress': 50},
            {'student': alumnos[2], 'course': cursos[3], 'status': 'enrolled', 'progress': 20},
            {'student': alumnos[3], 'course': cursos[2], 'status': 'enrolled', 'progress': 65},
            {'student': alumnos[4], 'course': cursos[3], 'status': 'enrolled', 'progress': 45}
        ]
        
        for insc_data in inscripciones_data:
            inscripcion, created = Enrollment.objects.get_or_create(
                student=insc_data['student'],
                course=insc_data['course'],
                defaults={
                    'status': insc_data['status'],
                    'progress': insc_data['progress']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Inscripción creada: {inscripcion.student.username} - {inscripcion.course.title}'))
            else:
                self.stdout.write(f'Inscripción ya existente: {inscripcion.student.username} - {inscripcion.course.title}')
        
        # Crear calificaciones
        calificaciones_data = [
            {'student': alumnos[0], 'evaluation': evaluaciones[0], 'score': 8.5},
            {'student': alumnos[1], 'evaluation': evaluaciones[0], 'score': 9.0},
            {'student': alumnos[0], 'evaluation': evaluaciones[2], 'score': 7.5},
            {'student': alumnos[2], 'evaluation': evaluaciones[2], 'score': 8.0},
            {'student': alumnos[1], 'evaluation': evaluaciones[3], 'score': 8.5},
            {'student': alumnos[3], 'evaluation': evaluaciones[3], 'score': 7.0},
            {'student': alumnos[2], 'evaluation': evaluaciones[4], 'score': 9.5},
            {'student': alumnos[4], 'evaluation': evaluaciones[4], 'score': 8.0}
        ]
        
        for cal_data in calificaciones_data:
            calificacion, created = Score.objects.get_or_create(
                student=cal_data['student'],
                evaluation=cal_data['evaluation'],
                defaults={
                    'score': cal_data['score']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Calificación creada: {calificacion.student.username} - {calificacion.evaluation.title}: {calificacion.score}'))
            else:
                self.stdout.write(f'Calificación ya existente: {calificacion.student.username} - {calificacion.evaluation.title}')
        
        self.stdout.write(self.style.SUCCESS('Datos iniciales creados correctamente'))
