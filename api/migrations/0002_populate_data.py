from django.db import migrations


def populate_data(apps, schema_editor):
    User = apps.get_model('api', 'User')
    Post = apps.get_model('api', 'Post')
    Comment = apps.get_model('api', 'Comment')

    # Crear usuarios
    user1 = User.objects.create(
        username='user1', email='user1@example.com', password='password1')
    user2 = User.objects.create(
        username='user2', email='user2@example.com', password='password2')
    user3 = User.objects.create(
        username='user3', email='user3@example.com', password='password3')
    user4 = User.objects.create(
        username='user4', email='user4@example.com', password='password4')
    user5 = User.objects.create(
        username='user5', email='user5@example.com', password='password5')

    # Crear seguidores
    user2.followers.add(user1)
    user3.followers.add(user1)
    user4.followers.add(user1)
    user5.followers.add(user1)
    user1.followers.add(user2, user3, user4, user5)

    # Crear publicaciones
    post1 = Post.objects.create(
        author=user1, content='Contenido de la publicación 1')
    post2 = Post.objects.create(
        author=user2, content='Contenido de la publicación 2')
    post3 = Post.objects.create(
        author=user3, content='Contenido de la publicación 3')
    post4 = Post.objects.create(
        author=user4, content='Contenido de la publicación 4')
    post5 = Post.objects.create(
        author=user5, content='Contenido de la publicación 5')

    # Crear comentarios
    comment1 = Comment.objects.create(
        author=user1, post=post1, content='Comentario 1 en la publicación 1')
    comment2 = Comment.objects.create(
        author=user2, post=post1, content='Comentario 2 en la publicación 1')
    comment3 = Comment.objects.create(
        author=user3, post=post2, content='Comentario 1 en la publicación 2')
    comment4 = Comment.objects.create(
        author=user4, post=post2, content='Comentario 2 en la publicación 2')
    comment5 = Comment.objects.create(
        author=user5, post=post3, content='Comentario 1 en la publicación 3')


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]
