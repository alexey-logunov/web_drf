from django.contrib import admin
from .models import Question, UserQuestionRelation


# @admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'added_at', 'rating', 'author')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text')
    list_editable = ('author',)
    list_filter = ('author', 'title')
    # fields = ('title', 'text', 'added_at', 'rating', 'author', 'likes')
    readonly_fields = ('added_at', 'author', 'likes')
    save_on_top = True


# @admin.register(UserQuestionRelation)
class UserQuestionRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'like', 'in_bookmarks', 'rate')
    list_display_links = ('id', 'user', 'question')
    search_fields = ('user', 'question')
    # list_editable = ('user',)
    list_filter = ('user', 'question')
    # fields = ('title', 'text', 'added_at', 'rating', 'author', 'likes')
    readonly_fields = ('user', 'question', 'like', 'in_bookmarks', 'rate')


admin.site.register(Question, QuestionAdmin)
admin.site.register(UserQuestionRelation, UserQuestionRelationAdmin)

admin.site.site_title = 'Управление вопросами'
admin.site.site_header = 'Управление вопросами'
