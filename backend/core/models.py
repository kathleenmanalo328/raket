from django.db import models
from .ids import generate_id

class PrefixedIDModel(models.Model):
    id_prefix=""
    id = models.CharField(primary_key=True, max_length=40, editable=False)

    class Meta:
        abstract=True #tempalte, not real table

    def save(self, *args, **kwargs):
        if not self.id:
            self.id=generate_id(self.id_prefix)
        super().save(*args, **kwargs)
