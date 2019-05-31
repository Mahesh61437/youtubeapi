from django.db import models

# Create your models here.
class SearchDetail(models.Model):
    # video title
    title = models.CharField(max_length=255, null=False)
    # video description
    description = models.CharField(max_length=300)
    # video thumnail urls
    thumbnail = models.URLField()
    #video publishined date time
    datetime = models.DateTimeField()
    #query
    query = models.CharField(max_length=255,null = True)


    def __str__(self):
        return "{}".format(self.title)