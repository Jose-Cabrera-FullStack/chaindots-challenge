from django.http import Http404

from rest_framework import generics, status
from rest_framework.response import Response

from api.models import User, Post, Comment
from api.serializers import UserSerializer, PostSerializer, CommentSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        try:
            user_id = self.kwargs.get('pk', None)
            return User.objects.prefetch_related(
                'followers',
                'following',
                'post_set'
            ).get(id=user_id)
        except User.DoesNotExist:
            raise Http404()


class UserFollow(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        follow_id = self.kwargs.get('follow_id')

        try:
            user = User.objects.get(id=user_id)
            follower = User.objects.get(id=follow_id)
        except User.DoesNotExist:
            raise Http404()

        user.following.add(follower)
        return Response({
            "status": 200,
            "message": f"Follower: {follower.username} follows to User: {user.username}"},
            status=status.HTTP_200_OK
        )


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):

        queryset = super().get_queryset()

        author_id = self.request.query_params.get('author_id')
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')

        if author_id:
            queryset = queryset.filter(author_id=author_id)
        if from_date:
            queryset = queryset.filter(created_at__gte=from_date)
        if to_date:
            queryset = queryset.filter(created_at__lte=to_date)

        return queryset.select_related("author").order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.kwargs.get('pk')
        return queryset.select_related('author', 'post').filter(post_id=post_id)


class CommentDetail(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        comment_id = self.kwargs.get('pk')
        return queryset.select_related('author', 'post').filter(id=comment_id)
