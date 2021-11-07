from django.contrib import admin
from .models import Question

# @admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'added_at', 'rating', 'author')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text')
    list_editable = ('author',)
    list_filter = ('author', 'title')
    # fields = ('title', 'text', 'added_at', 'rating', 'author', 'likes')
    readonly_fields = ('added_at', 'likes')
    save_on_top = True


admin.site.register(Question, QuestionAdmin)

admin.site.site_title = 'Управление вопросами'
admin.site.site_header = 'Управление вопросами'