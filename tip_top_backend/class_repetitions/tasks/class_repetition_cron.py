# Python dependencies
import json
import datetime

# Models
from tip_top_backend.class_repetitions.models import ClassRepetition
from tip_top_backend.classes.models import Class
from tip_top_backend.lessons.models import Lesson
from tip_top_backend.units.models import Unit
from tip_top_backend.levels.models import Level
from tip_top_backend.students.models import Student
from tip_top_backend.student_classes.models import StudentClass
from tip_top_backend.notifications.serializers import NotificationSignUpSerializer

# Django Enviroment
import environ

env = environ.Env()


def single_class_repetition_service(class_id):
    class_obj = Class.objects.get(pk=class_id)
    return create_class_repetitions(class_obj)


def generate_class_repetitions_service():
    now = datetime.datetime.now()
    class_repetitions = ClassRepetition.objects.filter(last_repeat_date__lte=now)
    updated_class_repetitions = []
    for class_repetition in class_repetitions:
        last_class = Class.objects.filter(class_repetition_id=class_repetition.id).order_by('-init').first()
        if create_class_repetitions(last_class):
            updated_class_repetitions.append(ClassRepetition.objects.get(pk=class_repetition.id))
    return updated_class_repetitions


def create_class_repetitions(class_obj):
    class_id = class_obj.id
    if class_obj.state and class_obj.class_repetition is not None and class_obj.class_repetition.last_repeat_date < datetime.datetime.now():
        # Se establece la fecha inicial y final de la primera clase que ya fue creada, a partir de estas,
        # se crean las siguientes
        init_date = class_obj.init
        end_date = class_obj.end
        last_date = class_obj.class_repetition.last_repeat_date
        new_init_dates = []
        new_end_dates = []
        # Se generan las nuevas fechas de las clases repetidas, esto para luego poderlas ordenar
        for i, val in enumerate(class_obj.class_repetition.days):
            if val:
                # Se calcula el proximo dia mas cercano para crear la nueva clase
                if i == init_date.weekday():
                    new_init_date = init_date + datetime.timedelta(days=7)
                    new_end_date = end_date + datetime.timedelta(days=7)
                else:
                    new_init_date = init_date + datetime.timedelta((i - init_date.weekday()) % 7)
                    new_end_date = end_date + datetime.timedelta((i - end_date.weekday()) % 7)
                if init_date != new_init_date and new_init_date > init_date:
                    # Se valida que no exista ya una clase programada dentro de las nuevas fechas
                    existing_class = Class.objects.filter(init__gte=new_init_date, end__lte=new_end_date, state=True,
                                                          user_id=class_obj.user_id).first()
                    if existing_class is None:
                        new_init_dates.append(new_init_date)
                        new_end_dates.append(new_end_date)

        new_init_dates.sort()
        new_end_dates.sort()

        for i, new_init_date in enumerate(new_init_dates):
            # Se limpian campos para el nuevo registro
            current_lesson_id = class_obj.lesson_id
            class_obj.pk = None
            class_obj.created = None
            class_obj.modified = None
            class_obj.init = new_init_date
            class_obj.end = new_end_dates[i]

            students_class = StudentClass.objects.filter(class_obj_id=class_id)

            # Se busca la leccion para la clase siguiendo la secuencia
            student = students_class[0].student
            new_lesson = Lesson.objects.filter(parent_id=student.current_lesson_id).first()
            if new_lesson is None:
                new_lesson = Lesson.objects.get(pk=student.current_lesson_id)
                unit = Unit.objects.filter(parent_id=new_lesson.unit.id).first()
                if unit is None:
                    level = Level.objects.filter(parent_id=new_lesson.unit.level.id).first()
                    if not level is None:
                        new_lesson = Lesson.objects.filter(unit__level_id=level.id).order_by('id').first()
                else:
                    new_lesson = Lesson.objects.filter(unit_id=unit.id).order_by('id').first()
            if new_lesson is None:
                new_lesson = Lesson.objects.get(pk=student.current_lesson_id)

            # Si la nueva leccion es diferente a la que ya fue programada anteriormente
            if new_lesson.id != current_lesson_id:
                class_obj.lesson_id = student.current_lesson_id
                class_obj.save()

                # Se establece la fecha de la ultima clase programada
                if class_obj.end > last_date:
                    last_date = class_obj.end

                for student_class in students_class:
                    student_class.pk = None
                    student_class.created = None
                    student_class.modified = None
                    student_class.class_obj_id = class_obj.id
                    student_class.save()
                    student_class.student.current_lesson_id = new_lesson.id
                    student_class.student.save()

                    # Se generan las notificaciones pertinentes
                    generate_notifications(class_obj, student_class.student)

        class_repetition = ClassRepetition.objects.get(pk=class_obj.class_repetition_id)
        class_repetition.last_repeat_date = last_date
        class_repetition.save()
        return True
    else:
        return False


def generate_notifications(class_obj, student_obj):
    notification = {}
    data_obj = {
        "teacher": class_obj.user.first_name + ' ' + class_obj.user.last_name,
        "student": student_obj.user.first_name + ' ' + student_obj.user.last_name,
        "lesson": class_obj.lesson.title,
        "date": class_obj.init.strftime("%A, %d th %B - %Y"),
        "time": class_obj.init.strftime("%H:%M %p"),
        "date_init": class_obj.init.strftime("%Y-%m-%d %H:%M"),
        # "url": env('DJANGO_APP_URL'),
        "url": class_obj.url,
        "type": "assignment"
    }

    notification['type'] = 'EMAIL'
    notification['status'] = 'PENDING'
    notification['to'] = class_obj.user.email
    notification['data'] = json.dumps(data_obj)

    # Save Class notification for teacher
    notification['title'] = 'Clase asignada, Assigned class'
    notification['template'] = 'email/email-asignacion-profesor'
    serializer = NotificationSignUpSerializer(data=notification)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    # Save Class reminder notification for teacher
    notification['title'] = 'Recordatorio de clase, Class reminder'
    notification['template'] = 'email/email-recordatorio-profesor'
    data_obj['type'] = "reminder"
    notification['data'] = json.dumps(data_obj)
    serializer = NotificationSignUpSerializer(data=notification)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    if env('ENABLE_STUDENT_NOTIFICATIONS').lower() in ['true', '1']:
        data_obj['type'] = "assignment"
        notification['to'] = student_obj.user.email
        notification['data'] = json.dumps(data_obj)

        # Save Class notification for student
        notification['title'] = 'Clase asignada, Assigned class'
        notification['template'] = 'email/email-asignacion'
        serializer = NotificationSignUpSerializer(data=notification)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Save Class reminder notification for student
        notification['title'] = 'Recordatorio de clase, Class reminder'
        notification['template'] = 'email/email-recordatorio'
        data_obj['type'] = "reminder"
        notification['data'] = json.dumps(data_obj)
        serializer = NotificationSignUpSerializer(data=notification)
        serializer.is_valid(raise_exception=True)
        serializer.save()
