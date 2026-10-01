from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Enrollment
from .serializers import EnrollmentSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class EnrollmentListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = Enrollment.objects.all()

        serializer = EnrollmentSerializer(
            enrollments,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        if request.user.role == 'STUDENT':
            return Response(
        {"error": "Students cannot create enrollments"},
        status=status.HTTP_403_FORBIDDEN
    )
        serializer = EnrollmentSerializer(
            data=request.data
        )

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
from django.shortcuts import get_object_or_404
class EnrollmentDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role == 'STUDENT':
            enrollments = Enrollment.objects.filter(
            student__user=request.user
        )
        else:
             enrollments = Enrollment.objects.all()

        serializer = EnrollmentSerializer(
            enrollments,
            many=True
    )

        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.role == 'STUDENT':
            return Response(
        {"error": "Students cannot update enrollments"},
        status=status.HTTP_403_FORBIDDEN
    )
        enrollment = get_object_or_404(
            Enrollment,
            id=pk
        )

        serializer = EnrollmentSerializer(
            enrollment,
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
        {"error": "Students cannot delete enrollments"},
        status=status.HTTP_403_FORBIDDEN
    )
        enrollment = get_object_or_404(
            Enrollment,
            id=pk
        )

        enrollment.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )