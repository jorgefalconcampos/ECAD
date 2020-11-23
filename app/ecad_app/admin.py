from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from django_summernote.admin import SummernoteModelAdmin
from . models import Post, Category, Author, Comment, Misc, Subscriber




#Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    exclude = ('slug',)



#Blog post
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'subtitle', 'author', 'created_date', 'published_date', 'status')
    exclude = ('slug', 'vote_fav', 'vote_util', 'vote_tmbup', 'vote_tmbdn', 'send_to_newsletter',)
    summernote_fields = ('post_body')
    list_filter = ('author', 'status')
    search_fields = ['title', 'subtitle'] #author name has the double underscore bc is a foreign key
    actions = [ 'put_in_draft', 'approve_posts', 'reject_posts', 'archive_posts' ]

    def put_in_draft(self, request, queryset):
        queryset.update(status=0)

    def approve_posts(self, request, queryset):
        queryset.update(status=1)

    def reject_posts(self, request, queryset):
        queryset.update(status=2)

    def archive_posts(self, request, queryset):
        queryset.update(status=3)
    


#Comment inside a post
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'author_email', 'comment_body', 'is_approved', 'has_report', 'created_date', 'in_post')
    list_filter = ('created_date', 'is_approved')
    search_fields = ['author', 'author_email', 'comment_body']
    actions = [ 'approve_comments' ] 

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)



#User
UserAdmin.list_display = ('username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff')



#User/Author, person who can access to the dashboard and writes a post 
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'slug', 'activated_account')
    search_fields = ('name', 'title', 'email')
    prepopulated_fields = {'slug': ('name',)}
    actions = [ 'activate_account' ]

    def activate_account(self, request, queryset):
        queryset.update(activated_account=True)



class CrewAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email')
    search_fields = ('name', 'title', 'email')


class MiscAdmin(SummernoteModelAdmin):
    list_display = ('name', 'date')
    summernote_fields = ('content')
    search_fields = ('name', 'content')




class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'confirmed', 'conf_num')
    search_fields = ('email', 'confirmed')
    actions = ['confirm_subscriber']

    def confirm_subscriber(self, request, queryset):
        queryset.update(confirmed=True)







# Adding custom models to Admin page
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Misc, MiscAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
