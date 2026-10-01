from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Result
from .serializers import ResultSerializer
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class ResultListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = Result.objects.all()

        serializer = ResultSerializer(
            results,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        if request.user.role == 'STUDENT':
            return Response(
        {"error": "Students cannot create results"},
        status=status.HTTP_403_FORBIDDEN
    )
        serializer = ResultSerializer(
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
class ResultDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role == 'STUDENT':
         results = Result.objects.filter(
            student__user=request.user
        )
        else:
            results = Result.objects.all()

        serializer = ResultSerializer(
            results,
            many=True
    )

        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.role == 'STUDENT':
            return Response(
        {"error": "Students cannot update results"},
        status=status.HTTP_403_FORBIDDEN
    )
        result = get_object_or_404(
            Result,
            id=pk
        )

        serializer = ResultSerializer(
            result,
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
        {"error": "Students cannot delete results"},
        status=status.HTTP_403_FORBIDDEN
    )
        result = get_object_or_404(
            Result,
            id=pk
        )

        result.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )