from django.db import models
from django.contrib.auth.models import User
from registration.models_base import BaseModel

class PositionManagerActive(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active = True)

class PositionManagerAll(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()

class Position(BaseModel):
    title = models.CharField(
            max_length=100,
            verbose_name="Title",
            null=False,
            blank=False,
            unique=True,
            db_index= True
    )
    number_of_slots = models.PositiveSmallIntegerField(
            verbose_name="Number of Slot",
            blank=False,
            null=False,
    )
    description = models.CharField(
            max_length=500,
            null=True,
            blank=True,
            verbose_name="Description"
    )
    is_active = models.BooleanField(
            default=True,
            verbose_name="Is Active?"
    )
    created_by = models.ForeignKey(
                User,
                on_delete=models.SET_NULL,
                null=True,
                verbose_name="Created by",
                related_name="position_created_by",
                related_query_name='position_created'
    )
    last_updated_by = models.ForeignKey(
                User,
                on_delete=models.SET_NULL,
                null=True,
                verbose_name="Last Updated by",
                related_name="position_updated_by",
                related_query_name='position_last_updated'
    )
    priority = models.PositiveSmallIntegerField(
                verbose_name="Priority",
                blank=False,
                null=False,
                default = 0,
    )

    #overriding objects so that it's the active will only show on the form ElectionForm
    #or any other form that call position
    objects = PositionManagerActive()

    all_objects = PositionManagerAll()

    class Meta:
        ordering = ['priority','title']

    def __str__(self):
        return self.title

    def natural_key(self):
        return self.__str__()

class PositionGradeLevel(models.Model):
    grade_level = models.CharField(
            max_length=20,
            verbose_name="Grade Level",
            null=False,
            blank=False,
    )
    position = models.ForeignKey(
            Position,
            on_delete=models.CASCADE,
            verbose_name="Position",
            related_name="grade_levels",
            related_query_name="grade_levels"
    )

    def __str__(self):
        return self.grade_level

    class Meta:
        ordering = ('grade_level',)
