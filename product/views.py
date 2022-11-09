from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from .models import Member

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .serializers import MemberSerializer

#멤버 리스트를 위한 API
class MemberListAPI(APIView):
    def get(self, request):
        queryset = Member.objects.all()
        serializer = MemberSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        #many=True면 배열을 기대한다.
        serializer = MemberSerializer(data=request.data)

        #유효성 확인
        if(not serializer.is_valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=201)

    def put(self, request):
        #없는 메소드
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request):
        #없는 메소드
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#단일 멤버를 위한 API
class MemberAPI(APIView):
    def get(self, request, uid):
        queryset = Member.objects.get(uid=uid)
        serializer = MemberSerializer(queryset)
        return Response(serializer.data, status=200)

    def post(self, request, uid):
        #없는 메소드
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, uid): 
        #예외처리하기 key값이 없는거라던가
        Member.objects.filter(uid=uid).update(**request.data)

        return Response(status=200)

    def delete(self, request, uid):
        #실제로 데이터를 없애진 말자
        Member.objects.filter(uid=uid).update(inactive=True)
        return Response(status=200)