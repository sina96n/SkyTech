from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import RESTRICT

from user.models import Operator, Attendant

User = get_user_model()

class Meeting(models.Model):

    title    = models.CharField(max_length=255)
    operator = models.ForeignKey(Operator, null=True, blank=True, related_name="operator", on_delete=RESTRICT)
    # date     = models.DateField()

    # category_choices = (
    #     ("mathematics", "Mathematics"),
    #     ("geometry"   , "Geometry"),
    #     ("physics"    , "Physics"),
    #     ("chemistry"  , "Chemistry"),
    #     ("literature" , "Literature"),
    #     ("hiatory"    , "Hiatory"),
    # )

    #category = models.CharField(max_length=150)

    description = models.TextField()
    thumbnail   = models.ImageField(
        #default='thumbnail/default/default-gray.png',
        upload_to='thumbnail/',
        blank=True,
        null=True
    )

    status = (
        (True, "On"),
        (False, "Off"),
    )

    is_open = models.BooleanField(choices=status, default=False, verbose_name="Status")

    path = models.CharField(max_length=50, blank=True)

    attendants = models.ManyToManyField(Attendant, default=None, blank=True)

    def attendants_num(self):
        return self.attendants.all().count()

    def snippet(self) -> str:
        return self.description[:150] + "  ...."

    def __str__(self) -> str:
        return self.title 