from django.db import models


class BaseModel(models.Model): #base model for all my models. This will have the column create_date, last_update_date, Created_by, last_updated_by
    created_date = models.DateTimeField(
                auto_now_add=True,
                null=True
    )
    modified_date = models.DateTimeField(
                auto_now=True,
                null=True
    )

    class Meta:
        abstract = True
