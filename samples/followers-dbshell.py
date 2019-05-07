from blog.models import *
john = Author.objects.create_user('john', 'lennon@thebeatles.com', 'password')
paul = Author.objects.create_user('paul', 'mccartney@thebeatles.com', 'password')

john.following.add(Follower(following=paul), bulk=False)

# У john нет подписчиков
john.followers.all()
# У paul подписчик john
paul.followers.all()
# Сам же paul ни на кого не подписывался
paul.following.all()
# А john подписался на paul
john.following.all()
