from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework import generics # generics class-based view 사용할 계획
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from .serializers import MemberSerializer, MemberRegisterSerializer, MemberLoginSerializer
from .models import Member

# Create your views here.

# 누구나 접근 가능
@permission_classes([AllowAny]) 
class Registration(generics.GenericAPIView):
    serializer_class = MemberRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)

        member = serializer.save(request) # request 필요 -> 오류 발생

        return Response(
            {
            # get_serializer_context: serializer에 포함되어야 할 어떠한 정보의 context를 딕셔너리 형태로 리턴
            # 디폴트 정보 context는 request, view, format
                "member": MemberSerializer(
                    member, context=self.get_serializer_context()
                ).data
            },
                status=status.HTTP_201_CREATED,
        )

@permission_classes([AllowAny])
class Login(generics.GenericAPIView):
    serializer_class = MemberLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
        member = serializer.validated_data
        if member['username'] == "None":
            return Response({"message": "fail"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            {
                "member": MemberLoginSerializer(
                    member, context=self.get_serializer_context()
                ).data
            }
        )

#멤버 리스트를 위한 API
class MemberListAPI(generics.GenericAPIView):
    def get(self, request):
        """
        API형식
        GET /members?
                     query=<table id>&           기준 정렬은 없는 것이 기본
                     asc=<int:0, 1::default=0>&  내림차순이 기본
                     offset=<int::default=0>&    0번 부터 불러오는 것이 기본
                     limit=<int::default = 10>   최대 10까지 불러오는 것이 기본
        """

        #정렬관련 쿼리 
        #?query=username&asc=0&offset=0&limit=3
        #정렬할 대상
        query = request.GET.get('query', None)                              
        #오름차순 내림차순
        asc =  "" if int(request.GET.get('asc', 0)) else "-"     

        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 10))

        queryset = Member.objects.all()
        queryset = queryset.filter(is_active=True)

        if query is not None:
            queryset = queryset.order_by(f"{asc}{query}")[offset:offset+limit]

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
class MemberAPI(generics.GenericAPIView):
    def get(self, request, username):
        queryset = Member.objects.get(username=username)
        serializer = MemberSerializer(queryset)
        return Response(serializer.data, status=200)

    def post(self, request, username):
        #없는 메소드
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, username): 
        #예외처리하기 key값이 없는거라던가
        Member.objects.filter(username=username).update(**request.data)

        return Response(status=200)

    def delete(self, request, username):
        #실제로 데이터를 없애진 말자
        Member.objects.filter(username=username).update(inactive=True)
        return Response(status=200)