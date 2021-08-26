from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Follow
from .serializers import FollowSerializer, ShowFollowsSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):

    @action(detail=True,
            methods=["GET", "DELETE"],
            url_path='subscribe',
            url_name='subscribe',
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        serializer = FollowSerializer(
            data={'user': request.user.id, 'author': id}
        )
        if request.method == "GET":
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            serializer = ShowFollowsSerializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        follow = get_object_or_404(Follow, user=request.user, author__id=id)
        follow.delete()
        return Response(f'{request.user} отписался от {follow.author}',
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=["GET"],
            url_path='subscriptions',
            url_name='subscriptions',
            permission_classes=[permissions.IsAuthenticated])
    def show_follows(self, request):
        user_obj = User.objects.filter(following__user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 3
        result_page = paginator.paginate_queryset(user_obj, request)
        serializer = ShowFollowsSerializer(
            result_page, many=True, context={'current_user': request.user})
        return paginator.get_paginated_response(serializer.data)
