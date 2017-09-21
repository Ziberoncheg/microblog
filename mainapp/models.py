from django.db import models
from authsys.models import MyUser
# Create your models here.
class Post(models.Model):

    def __str__(self):
        return self.post_title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    post_authors = models.ForeignKey(MyUser)
    post_title = models.CharField(blank=False,max_length=264)
    post_description = models.TextField()
    post_photo = models.FileField(upload_to='images')
    post_create_date = models.DateTimeField(auto_now=True)

    def get_likes(self):
        count = Likes.objects.filter(like_to_post = self).count()
        return "%s" %count

class Post_comments(models.Model):

    def __str__(self):
        return self.comments_text

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    comments_author = models.ForeignKey(MyUser)
    comments_post = models.ForeignKey(Post)
    comments_text = models.TextField()

class Likes(models.Model):

    like_to_post = models.ForeignKey(Post)
    like_from_user = models.ForeignKey(MyUser)