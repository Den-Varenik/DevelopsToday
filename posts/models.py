from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Comment author",
        on_delete=models.CASCADE,
    )
    title = models.CharField(_("Title"), max_length=100)
    link = models.URLField(_("Link"))
    upvote = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.title)
