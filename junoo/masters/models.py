from django.db import models
class junoocategory(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    def __str__(self):
        return self.title

    @property
    def get_junnosubcats(self):
        return junoosubcategory.objects.filter(junoocategory=self.id)

class junoosubcategory(models.Model):
    junoocategory = models.ForeignKey(junoocategory, default=None, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    def __str__(self):
        return self.title