from django.contrib import admin
from main.models import SportNewsMainCategory, SportNewsCategory, SportNews

class SportNewsMainCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    
    ordering = ['order',]
    
    fieldsets = [
        ('Name', {'fields' : ['name',]}),
        ('Order', {'fields' : ['order',]}),
    ]
    
    list_display = ('name', 'order',)

class SportNewsCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'mainCategory']
    
    list_filter = ['mainCategory',]
    
    ordering = ['mainCategory__order', 'order',]
    
    fieldsets = [
        ('Name', {'fields' : ['name',]}),
        ('Main category', {'fields' : ['mainCategory',]}),
        ('Order', {'fields' : ['order',]}),
    ]
    
    list_display = ('name', 'mainCategory', 'order',)

class SportNewsAdmin(admin.ModelAdmin):
    search_fields = ['title', 'text', 'category',]
    
    list_filter = ['priority', 'category__mainCategory', 'category', 'created_at', 'updated_at',]
    
    ordering = ['priority', 'created_at', ]
    
    readonly_fields = ('created_at', 'updated_at',)
    
    list_display = ('title', 'category', 'priority', 'created_at', 'updated_at',)
    
    

admin.site.register(SportNewsMainCategory, SportNewsMainCategoryAdmin)
admin.site.register(SportNewsCategory, SportNewsCategoryAdmin)
admin.site.register(SportNews, SportNewsAdmin)