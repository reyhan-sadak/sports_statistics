from django.db import models
from django.contrib.auth.models import User

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
        return self.name + ' from ' + self.mainCategory.name
        

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

class SportNewsComment(models.Model):
    # Created at
    created_at = models.DateTimeField(auto_now_add = True)
    # Updated at
    updated_at = models.DateTimeField(auto_now = True)
    # User
    user = models.ForeignKey(User)
    # Tite
    title = models.CharField(max_length = 255)
    # Comment text
    text = models.TextField()
    # Root comment
    root_comment = models.ForeignKey("SportNewsComment", null=True, blank=True)
    # The news for which the comment is
    news = models.ForeignKey(SportNews)
    # Comment number
    comment_number = models.PositiveIntegerField()
    
    class Meta:
        unique_together = (('news', 'comment_number'),)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        comment_number = getNextCommentNumber(self.news)
        if self.comment_number is None:
            self.comment_number = comment_number
        super(SportNewsComment, self).save(*args, **kwargs)

def getNextCommentNumber(news):
    current_comment_number = SportNewsComment.objects.filter(news=news).order_by('-comment_number').values_list('comment_number', flat=True)
    if current_comment_number:
        return current_comment_number[0] + 1
    else:
        return 1