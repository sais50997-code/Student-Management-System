from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Course
from .serializers import CourseSerializer


class CourseListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)

    def post(self, request):
        if request.user.role == 'STUDENT':
            return Response(
        {"error": "Students cannot create courses"},
        status=status.HTTP_403_FORBIDDEN
    )
        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CourseDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        serializer = CourseSerializer(course)

        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.role == 'STUDENT':
            return Response(
        {"error": "Students cannot update courses"},
        status=status.HTTP_403_FORBIDDEN
    )
        course = get_object_or_404(Course, id=pk)

        serializer = CourseSerializer(
            course,
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
        {"error": "Students cannot delete courses"},
        status=status.HTTP_403_FORBIDDEN
    )
        course = get_object_or_404(Course, id=pk)

        course.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )