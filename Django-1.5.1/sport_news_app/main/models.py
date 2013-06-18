from django.db import models

# Create your models here.

NEWS_PRIO = (
    ('NEWS_MAIN1','Main news 1st'),
    ('NEWS_MAIN2','Main news 2nd'),
    ('NEWS_MAIN3','Main news 3th'),
    ('NEWS_MAIN4','Main news 4th'),
    ('NEWS_MAIN5','Main news 5th'),
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