
from rest_framework import serializers
from api.models import User, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    total_posts = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    def get_total_posts(self, obj):
        return obj.post_set.count()

    def get_total_comments(self, obj):
        return obj.comment_set.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'followers',
            'following',
            'total_posts',
            'total_comments',
            'followers_count',
            'following_count'
        ]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def get_author(self, obj):
        return obj.author

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    post = PostSerializer()

    def get_author(self, obj):
        return obj.author

    def get_post(self, obj):
        return obj.post

    class Meta:
        model = Comment
        fields = '__all__'
