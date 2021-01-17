from django.db import models
from users.models import User


class Review(models.Model):
    statuses = [
        ('moderation', 'на модерации'),
        ('published', 'опубликован'),
        ('declined', 'отклонен'),
    ]

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='автор')
    text = models.TextField(max_length=500, verbose_name='текст')
    created_at = models.DateTimeField(null=True, verbose_name='дата создания')
    published_at = models.DateTimeField(null=True, verbose_name='дата публикации')
    status = models.CharField(max_length=20, choices=statuses, verbose_name='статус')

    def __str__(self):
        return str(self.text)