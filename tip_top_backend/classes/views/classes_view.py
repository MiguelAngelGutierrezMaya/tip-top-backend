"""Class view"""

# Dependencies
import datetime
import json

# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializers
from tip_top_backend.classes.serializers import (
    ClassModelSerializer,
    ClassSignUpSerializer
)
from tip_top_backend.student_classes.serializers import (
    StudentClassModelSerializer,
    StudentClassSignUpSerializer
)
from tip_top_backend.notifications.serializers import (
    NotificationSignUpSerializer
)

# Model
from tip_top_backend.classes.models import Class
from tip_top_backend.students.models import Student
from tip_top_backend.student_classes.models import StudentClass
from tip_top_backend.levels.models import Level
from tip_top_backend.units.models import Unit
from tip_top_backend.lessons.models import Lesson

# Permissions
from rest_framework.permissions import (IsAuthenticated)

# Django Enviroment
import environ
env = environ.Env()


class ClassAPIView(APIView):
    """Class API view."""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Handle HTTP GET request."""
        pass

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        try:
            serializer = ClassSignUpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            class_obj = serializer.save()
            request.data['class_obj_id'] = class_obj.id
            lesson = Lesson.objects.filter(parent_id=request.data['lesson_id']).first()

            if lesson is None:
                lesson = Lesson.objects.get(pk=request.data['lesson_id'])
                unit = Unit.objects.filter(parent_id=lesson.unit.id).first()
                if unit is None:
                    level = Level.objects.filter(parent_id=lesson.unit.level.id).first()
                    if not level is None:
                        lesson = Lesson.objects.filter(unit__level_id=level.id).order_by('id').first()
                else:
                    lesson = Lesson.objects.filter(unit_id=unit.id).order_by('id').first()
            for student in request.data['students']:
                request.data['student_id'] = student['id']
                serializer = StudentClassSignUpSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                student_obj = Student.objects.get(pk=student['id'])
                student_obj.current_lesson_id = lesson.id
                student_obj.save()

                data_obj = {
                    "student": student_obj.user.first_name + ' ' + student_obj.user.last_name,
                    "lesson": class_obj.lesson.title,
                    "date": class_obj.init.strftime("%A, %d th %B - %Y"),
                    "time": class_obj.init.strftime("%H:%M %p"),
                    "date_init": class_obj.init.strftime("%Y-%m-%d %H:%M"),
                    "url": env('DJANGO_APP_URL'),
                    "type": "assignment"
                }

                request.data['type'] = 'EMAIL'
                request.data['status'] = 'PENDING'
                request.data['to'] = student_obj.user.email
                request.data['data'] = json.dumps(data_obj)
                # Save Class notification
                request.data['title'] = 'Clase asignada, Assigned class'
                request.data['template'] = 'email/email-asignacion'
                serializer = NotificationSignUpSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                # Save Class reminder notification
                request.data['title'] = 'Recordatorio de clase, Class reminder'
                request.data['template'] = 'email/email-recordatorio'
                data_obj['type'] = "reminder"
                request.data['data'] = json.dumps(data_obj)
                serializer = NotificationSignUpSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            data = ClassModelSerializer(class_obj).data
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({'msg': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        """Handle HTTP PATCH request."""
        class_obj = Class.objects.get(pk=request.data['id'])
        if not class_obj.state:
            return Response("The course is already canceled,El curso ya se encuentra cancelado", status=status.HTTP_400_BAD_REQUEST)
        current_date = (datetime.datetime.now() - datetime.timedelta(hours=5))
        if current_date > class_obj.init:
            return Response("You cannot cancel classes that have already been or are taking place,No se pueden cancelar clases que ya se han realizado o se están realizando", status=status.HTTP_400_BAD_REQUEST)

        student_classes = StudentClass.objects.filter(class_obj_id=class_obj.id)
        for student_class in student_classes:
            lesson = Lesson.objects.get(pk=student_class.student.current_lesson_id)
            student_class_verify = StudentClass.objects.filter(
                student_id=student_class.student.id, class_obj__lesson_id=lesson.parent_id, class_obj__state=True).first()
            if student_class_verify is None:
                student_class_verify = StudentClass.objects.filter(student_id=student_class.student.id,
                                                                   class_obj__lesson__id__lt=lesson.id, class_obj__state=True).first()
            if not student_class_verify is None:
                if not student_class_verify.class_obj_id == class_obj.id:
                    return Response(f"You cannot cancel this class as there is a class scheduled with a later lesson for the student {student_class.student.user.first_name},No puedes cancelar esta clase ya que hay una clase programada con una lección posterior para el estudiante {student_class.student.user.first_name}", status=status.HTTP_400_BAD_REQUEST)
        for student_class in student_classes:
            lesson = Lesson.objects.get(pk=student_class.student.current_lesson_id)
            student_obj = Student.objects.get(pk=student_class.student.id)
            if lesson.parent_id is None:
                lesson = Lesson.objects.filter(id__lt=lesson.id).first()
                if lesson is None:
                    lesson = Lesson.objects.all().order_by('id').first()
                student_obj.current_lesson_id = lesson.id
            else:
                student_obj.current_lesson_id = lesson.parent_id
            student_obj.save()
        class_obj.state = request.data['state']
        class_obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
