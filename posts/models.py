from django.db import models
from django.urls import reverse
from users_api.models import Account


class Post(models.Model):
    body = models.TextField(blank=True)
    # pic = models.ImageField(upload_to='path/to/img')
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Account, related_name='posts', on_delete=models.CASCADE)
    # tags = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['created']

    # def __str__(self):
    #     return str(self.owner)

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': self.pk})
 
class Comments(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    owner = models.ForeignKey(Account, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return str(self.owner)

class Like(models.Model):
    owner = models.ForeignKey(Account, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('owner', 'post'),)

