
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


class PostReadSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        return CommentWriteSerializer(obj.comment_set.all().order_by('-created_at'), many=True).data[:3]

    class Meta:
        model = Post
        fields = '__all__'


class PostWriteSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    comments = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author

    def get_comments(self, obj):
        return CommentWriteSerializer(obj.comment_set.all().order_by('-created_at'), many=True).data[:3]

    class Meta:
        model = Post
        fields = '__all__'


class CommentReadSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    post = PostWriteSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class CommentWriteSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'
