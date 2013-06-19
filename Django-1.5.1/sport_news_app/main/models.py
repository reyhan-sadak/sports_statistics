from django.db import models

# Create your models here.

NEWS_PRIO = (
    ('NEWS_MAIN','Main news'),
    ('NEWS_SECONDARY_1','Secondary news 1'),
    ('NEWS_SECONDARY_2','Secondary news 2'),
    ('NEWS_SECONDARY_3','Secondary news 3'),
    ('NEWS_NORMAL', 'Normal news'),
)

class SportNewsMainCategory(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    order = models.PositiveIntegerField(unique = True)
    
    def __str__(self):
        return self.name

class SportNewsCategory(models.Model):
    name = models.CharField(max_length = 255)
    mainCategory = models.ForeignKey(SportNewsMainCategory)
    order = models.PositiveIntegerField()
    
    class Meta:
        unique_together = (('name', 'mainCategory'), ('mainCategory', 'order'))
    
    def __str__(self):
        return self.name
        

class SportNews(models.Model):
    # News Title
    title = models.CharField(max_length = 255)
    # News text
    text = models.TextField()
    # Priority
    priority = models.CharField(max_length = 255, choices = NEWS_PRIO)
    # Category
    category = models.ForeignKey(SportNewsCategory)
    # Created at
    created_at = models.DateTimeField(auto_now_add = True)
    # Updated at
    updated_at = models.DateTimeField(auto_now = True)
    # News photo
    photo = models.FileField(upload_to='news', blank=True)
    def __str__(self):
        return self.title