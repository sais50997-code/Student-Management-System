from django.db import models
from students.models import Student
from courses.models import Course


class Result(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    internal_marks = models.PositiveIntegerField()
    external_marks = models.PositiveIntegerField()

    total_marks = models.PositiveIntegerField(
        editable=False
    )

    grade = models.CharField(
        max_length=2,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course_result'
            )
        ]

    def save(self, *args, **kwargs):
        self.total_marks = self.internal_marks + self.external_marks

        if self.total_marks >= 90:
            self.grade = 'A+'
        elif self.total_marks >= 80:
            self.grade = 'A'
        elif self.total_marks >= 70:
            self.grade = 'B'
        elif self.total_marks >= 60:
            self.grade = 'C'
        elif self.total_marks >= 50:
            self.grade = 'D'
        else:
            self.grade = 'F'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.course.course_name}"
