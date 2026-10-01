from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Student
from .serializers import StudentSerializer


class StudentListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):

        if request.user.role == 'STUDENT':

            students = Student.objects.filter(
            user=request.user
        )

        else:

            students = Student.objects.all()

        serializer = StudentSerializer(
                students,
        many=True
    )

        return Response(serializer.data)
    def post(self, request):
        if request.user.role == 'STUDENT':
            return Response(
        {"error": "Students cannot create student records"},
        status=status.HTTP_403_FORBIDDEN
    )
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        print("HII")
        print(serializer.errors)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class StudentDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        student = get_object_or_404(Student, id=pk)

        if request.user.role == 'STUDENT' and student.user != request.user:
            return Response(
            {"error": "You can only view your own profile"},
            status=status.HTTP_403_FORBIDDEN
        )

        serializer = StudentSerializer(student)

        return Response(serializer.data)
    def put(self, request, pk):
        if request.user.role == 'STUDENT':
            return Response(
        {"error": "Students cannot update student records"},
        status=status.HTTP_403_FORBIDDEN
    )
        student = get_object_or_404(Student, id=pk)

        serializer = StudentSerializer(
            student,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        if request.user.role == 'STUDENT':
            return Response(
        {"error": "Students cannot delete student records"},
        status=status.HTTP_403_FORBIDDEN
    )
        student = get_object_or_404(Student, id=pk)

        student.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
   