from django.db import models

# Create your models here.


class History(models.Model):
    original_text = models.TextField()
    result_text = models.TextField(blank=True,null=True)
    offset = models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    encryption = models.BooleanField(default=True)

    def to_dict(self):
        result = dict(original_text=self.original_text, result_text=self.result_text, id=self.pk,
                        offset=self.offset, encryption=self.encryption,
                        created_at=self.created_at.strftime('%a, %d %b %Y %H:%M:%S GMT'))
        return result
