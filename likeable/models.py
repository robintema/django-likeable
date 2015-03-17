#
# django-likeable
#
# See LICENSE for licensing details.
#

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _



class Like(models.Model):
    """
    A single "like" for a likeable object.
    Aims to be scaling-friendly by avoiding class inheritance.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='likes',
        help_text=_("The user who liked the particular object."),
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The date/time when this user liked this object."),
    )
    content_type = models.ForeignKey(
        ContentType,
        help_text=_("The content type of the liked object."),
    )
    object_id = models.PositiveIntegerField(
        help_text=_("The primary key of the liked object."),
    )
    liked = generic.GenericForeignKey(
        'content_type',
        'object_id',
    )

    class Meta:
        # make sure we can't have a user liking an object more than once
        unique_together = (('user', 'content_type', 'object_id'),)


    def __unicode__(self):
        return _("Like of %(obj)s by %(user)s at %(timestamp)s") % {
            'obj': self.liked,
            'user': self.user,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }


    


class Likeable(models.Model):
    """
    Abstract class on which a "likeable" object can be based.

    Essentially adds a "likes" relation to the models derived from this
    class which allows one simple access to likes.
    """

    likes = generic.GenericRelation(
        Like,
    )

    class Meta:
        abstract = True


    def like(self, user):
        """
        Generates a like for this object by the given user.
        """

        return Like.objects.create(user=user, liked=self)


    def unlike(self, user):
        """
        Delete the like for this object by the given user.
        """
        content_type = ContentType.objects.get_for_model(self)
        object_id = self.pk
        try:
            like = Like.objects.get(user=user, content_type=content_type, object_id=object_id)
        except Like.DoesNotExist:
            raise

        return like.delete()

    def liked(self, user):
        """
        Check if the user liked this object.
        """
        content_type = ContentType.objects.get_for_model(self)
        object_id = self.pk
        try:
            like = Like.objects.get(user=user, content_type=content_type, object_id=object_id)
            return True
        except Like.DoesNotExist:
            return False
