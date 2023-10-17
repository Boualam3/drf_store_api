from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# because we change default auth settings of django models to our custom settings (on core app) we import AUTH_USER_MODEL from settings file and specify to first arg of ForeignKey otherwise we dont walk on right way we should use the custom auth on every model or relationship


# as best practice we should always create custom user model at the beginning of project even is there is no requirement to change authentication so if you don't do as mentioned above you should drop the db and recreate that
class LikedItem(models.Model):
    # what user likes what object
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
