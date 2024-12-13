from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Deliver
from .serializers import DeliverSerializer, ProfileSerializer
from .permissions import IsDeliver


class RegisterView(APIView):
    """
    提供外送員註冊 (POST) 的功能
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = DeliverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    提供取得外送員資訊 (GET) 和更新外送員資訊 (PUT) 的功能
    """
    queryset = Deliver.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsDeliver]

    def get_object(self):
        try:
            return self.queryset.get(user=self.request.user)
        except Deliver.DoesNotExist:
            return None