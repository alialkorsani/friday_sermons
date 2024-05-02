from django.contrib import admin

from app.models import NewImage, New, Lecture, LectureVideo, FridaySermon, FridaySermonVideo, Token, Image, Status, \
    StatusImage, Book, BookPDF, Live, HelpImage, Help, Stat
from django import forms

from app.views import Stats


class NewImageInline(admin.TabularInline):
    model = NewImage
    extra = 3
    min_num = 1

class NewsPropertyAdmin(admin.ModelAdmin):
    inlines = [NewImageInline, ]
    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {'desc': forms.Textarea}
        return super().get_form(request, obj, **kwargs)

class HelpImageInline(admin.TabularInline):
    model = HelpImage
    extra = 3
    min_num = 1

class HelpsPropertyAdmin(admin.ModelAdmin):
    inlines = [HelpImageInline, ]
    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {'desc': forms.Textarea}
        return super().get_form(request, obj, **kwargs)

class StatusImageInline(admin.TabularInline):
    model = StatusImage
    extra = 3
    min_num = 1

class StatusesPropertyAdmin(admin.ModelAdmin):
    inlines = [StatusImageInline, ]
    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {'desc': forms.Textarea}
        return super().get_form(request, obj, **kwargs)

class BookPDFInline(admin.TabularInline):
    model = BookPDF
    extra = 1
    max_num = 1
    min_num = 1

class BooksPropertyAdmin(admin.ModelAdmin):
    inlines = [BookPDFInline, ]
    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {'desc': forms.Textarea}
        return super().get_form(request, obj, **kwargs)

class LectureVideoInline(admin.TabularInline):
    model = LectureVideo
    extra = 1
    max_num = 1
    min_num = 1

class LectureVideoPropertyAdmin(admin.ModelAdmin):
    inlines = [LectureVideoInline, ]
    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {'desc': forms.Textarea}
        return super().get_form(request, obj, **kwargs)

class FridaySermonVideoInline(admin.TabularInline):
    model = FridaySermonVideo
    extra = 1
    max_num = 1
    min_num = 1

    
class FridaySermonVideoPropertyAdmin(admin.ModelAdmin):
    inlines = [FridaySermonVideoInline, ]
    def get_form(self, request, obj=None, **kwargs):
            kwargs['widgets'] = {'desc_1': forms.Textarea, 'desc_2': forms.Textarea, 'title': forms.Textarea, 'desc': forms.Textarea,'title_1': forms.Textarea,'title_2': forms.Textarea,}
            return super().get_form(request, obj, **kwargs)

class LiveAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {'desc': forms.Textarea}
        return super().get_form(request, obj, **kwargs)

class StatsPropertyAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {'desc': forms.Textarea}
        return super().get_form(request, obj, **kwargs)

# admin.site.register(Token, admin.ModelAdmin)
admin.site.register(New, NewsPropertyAdmin)
admin.site.register(Help, HelpsPropertyAdmin)
admin.site.register(Lecture, LectureVideoPropertyAdmin)
admin.site.register(FridaySermon, FridaySermonVideoPropertyAdmin)
admin.site.register(Image, admin.ModelAdmin)
admin.site.register(Status, StatusesPropertyAdmin)
admin.site.register(Book, BooksPropertyAdmin)
admin.site.register(Live, LiveAdmin)
admin.site.register(Stat, StatsPropertyAdmin)

