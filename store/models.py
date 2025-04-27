from djongo import models

class Product(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    category = models.CharField(max_length=50)
    tags = models.JSONField(default=list, blank=True)  # New field for storing tags as a JSON array

    def __str__(self):
        return self.name