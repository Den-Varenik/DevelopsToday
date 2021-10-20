from django.conf import settings
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Post author",
        on_delete=models.CASCADE,
    )
    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField()
    link = models.URLField(_("Link"))
    upvote = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.title)


@receiver(signals.pre_save, sender=Post)
def populate_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.title)[:50]


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Comment author",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField(_("Comment"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
