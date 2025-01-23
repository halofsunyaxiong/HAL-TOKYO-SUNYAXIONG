from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

now = datetime.now()
time = now.strftime("%Y/%m/%d")

# 時間の形


# ユーザクラスはDjango自分のモドルを利用します
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/users', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    following = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# 記事
class Post(models.Model):
    postname = models.CharField(max_length=600)
    category = models.CharField(max_length=600)
    image = models.ImageField(upload_to='images/posts', blank=True, null=True)
    content = models.CharField(max_length=100000)
    time = models.CharField(default=time, max_length=100, blank=True)
    likes = models.IntegerField(null=True, blank=True, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.postname)


# コメント
class Comment(models.Model):
    content = models.CharField(max_length=200)
    time = models.CharField(default=time, max_length=100, blank=True)  # 時間
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # 多对一
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 多对一

    def __str__(self):
        return f"{self.id}.{self.content[:20]}..."  # コメント20文字


class Contact(models.Model):
    name = models.CharField(max_length=600)
    email = models.EmailField(max_length=600)
    subject = models.CharField(max_length=1000)
    message = models.CharField(max_length=10000, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # 多对一

    def __str__(self):
        return self.name
