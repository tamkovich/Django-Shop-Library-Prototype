from django.db import models

from django.utils.text import slugify
from django.db.models.signals import pre_save

class Categories(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, null=True, blank=True)
    def __str__(self):
        return self.title


def create_slug(instance, new_slug=None):
	slug = slugify(instance.title, allow_unicode=True)
	if new_slug is not None:
		slug = new_slug
	qs = Categories.objects.filter(slug=slug).order_by('-id')
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Categories)