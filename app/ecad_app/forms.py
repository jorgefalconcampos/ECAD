from django import forms as f
from taggit.forms import TagWidget
from django.contrib.auth.models import User
from django.utils.text import format_lazy as fl
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . models import Post, Author, Comment, Category
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField




#Create a new post
class PostForm(f.ModelForm):
    class Meta:
        model = Post
        title_attrs = {'class':'form-control form-control-lg', 'id':'post_title', 'type': 'text', 'name':'title', 'placeholder': _('str_postForm_title_placeholder')}
        subtitle_attrs = {'class':'form-control form-control-lg', 'id':'post_subtitle', 'type': 'text', 'name':'subtitle', 'placeholder': _('str_postForm_subtitle_placeholder')}
        unsplash_url_attrs = {'class':'form-control form-control-lg mr-2', 'id':'post_unsplash_url', 'type': 'URL', 'name':'unsplash_url', 'placeholder': fl('{}/{}_url', 'https://unsplash.com', _('str_photo'))}
        category_attrs = {'class':'selectpicker', 'id':'post_category', 'name':'category', 'data-style':'bs-select-form-control', 'data-title': _('str_postForm_category_title'), 'data-width':'100%' }
        tags_attrs = {'class': 'form-control form-control-lg,', 'id': 'post_tags', 'type': 'text', 'name': 'tags', 'placeholder': _('str_postForm_tags_placeholder')}
        fields = ('title', 'subtitle', 'image', 'unsplash_URL', 'post_body', 'category', 'tags')
        labels = {
            'title': _('str_postForm_title_label'),
            'subtitle': _('str_postForm_subtitle_label'),
            'image': _('str_postForm_image_label'),
            'unsplash_URL': _('str_unsplashURL_label'),
            'category': _('str_postForm_category_label'),
            'tags': _('str_postForm_tags_label'),
            'post_body': _('str_postForm_postBody_label')
        }

        widgets = {
            'title': f.TextInput(attrs=title_attrs),
            'subtitle': f.TextInput(attrs=subtitle_attrs),
            'unsplash_URL': f.URLInput(attrs=unsplash_url_attrs),
            'category': f.Select(attrs=category_attrs),
            'tags': TagWidget(attrs=tags_attrs),
            'post_body': SummernoteWidget(),
        }

    # name = f.CharField(label='Nombre y apellido', max_length=128, widget=f.TextInput(attrs=name_attrs), required=True)




#Create a new comment
class CommentForm(f.ModelForm):
    class Meta:
        model = Comment
        author_attrs = {'class':'form-control form-control-lg', 'id':'comment_fullName', 'type':'text', 'name':'full-name', 'placeholder': _('str_fullName_placeholder')}
        author_email_attrs = {'class':'form-control form-control-lg', 'id': 'comment_email', 'type': 'email', 'name':'author-email', 'placeholder':_('str_yourEmail_placeholder')}
        comment_body_attrs = {'class': 'mt-2 mt-sm-0 mt-md-0 mt-lg-0 form-control form-control-lg txtarea-maxh-400', 'id':'comment_body', 'name':'comment-body', 'rows':'5', 'placeholder': _('str_commentForm_comment_placeholder')}
        fields = ('author', 'author_email', 'comment_body')
        labels = {
            'author': _('str_firstName'),
            'author_email': _('str_email'),
            'comment_body': _('str_commentForm_comment_label')
        }
        widgets = {
            'author': f.TextInput(attrs=author_attrs),
            'author_email': f.EmailInput(attrs=author_email_attrs),
            'comment_body': f.Textarea(attrs=comment_body_attrs)
        }



# Overriding the 'UserCreationForm' to allow the new following fields as inputs: email, first_name last_name
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


#Search inside the blog
class SearchForm(f.Form):
    q_attrs = {'type': 'text', 'class':'form-control border-0 mr-2'}
    q = f.CharField(label=_('str_searchForm_label'), max_length=128, widget=f.TextInput(attrs=q_attrs))
    def __init__(self, *args, **kwargs):
        super (SearchForm, self).__init__(auto_id=True, *args, **kwargs)
        all_posts = str(Post.objects.filter(status=1).count()) #counting all-time posts
        self.fields['q'].widget.attrs['placeholder'] = _('str_searchAmong') + all_posts +' posts'


#To edit the account form (in the account section)
class AccountEditUserForm(UserChangeForm):
    usernme_attrs = {'class':'form-control', 'id':'acc_username', 'type': 'text', 'name':'username', 'placeholder': _('str_yourUsername_placeholder')}
    email_attrs = {'class':'form-control', 'id':'acc_email', 'type': 'email', 'name':'email', 'placeholder': fl('{} ({})', _('str_yourEmail_placeholder'), _('str_private')) }
    
    username = f.CharField(label=_('str_user'), max_length=32, widget=f.TextInput(attrs=usernme_attrs))
    email = f.EmailField(label=fl('{} {}', _('str_email'), _('str_private')), max_length=64, widget=f.EmailInput(attrs=email_attrs))
        
    class Meta:
        model = User
        fields = ('username', 'email')


     

# The 'ProfileEditUserForm' and 'ProfileEditAuthorForm' classes are for the same form (profile setting in dashboard)
class ProfileEditUserForm(f.ModelForm):
    first_name_attrs = {'class':'form-control', 'id':'profile_firstName', 'type': 'text', 'placeholder': _('str_firstName_placeholder')}
    last_name_attrs = {'class':'form-control', 'id':'profile_lastName', 'type': 'text', 'placeholder': _('str_lastName_placeholder')}

    first_name = f.CharField(label=_('str_firstName'), max_length=32, widget=f.TextInput(attrs=first_name_attrs))
    last_name = f.CharField(label=_('str_lastName'), max_length=32, widget=f.TextInput(attrs=last_name_attrs))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


# The 'ProfileEditUserForm' and 'ProfileEditAuthorForm' classes are for the same form (profile setting in dashboard)
class ProfileEditAuthorForm(f.ModelForm):
    title_attrs = {'class':'form-control', 'id':'profile_title', 'type':'text', 'placeholder': _('str_profileForm_title_placeholder')}
    bio_attrs = {'class':'form-control txtarea-maxh-200', 'id':'profile_bio', 'rows':'2', 'placeholder': _('str_profileForm_bio_placeholder')}
    email_attrs = {'class':'form-control', 'id':'profile_email', 'name':'email_url', 'type':'email', 'placeholder': fl('{} ({})', _('str_yourEmail_placeholder'), _('str_public'))}
    image_attrs = { 'class':'filestyle', 'id':'profile_image', 'type':'file', 'data-buttonBefore':'true', 'data-size':'sm', 'data-text': _('str_uploadPhoto'), "data-icon":"<i class='fas fa-file-image pr-2'></i>", 'data-btnClass':'btn-dark px-3', 'data-placeholder':_('str_profileForm_image_placeholder') }
    fb_attrs = {'class':'form-control', 'id':'profile_facebook', 'name':'facebook_url', 'type':'url', 'placeholder':'https://www.facebook.com/myprofile' }
    tw_attrs = {'class':'form-control', 'id':'profile_twitter', 'name':'twitter_url', 'type':'url', 'placeholder':'https://www.twitter.com/myprofile' }
    li_attrs = {'class':'form-control', 'id':'profile_linkedin', 'name':'linkedin_url', 'type':'url', 'placeholder':'https://www.linkedin.com/myprofile' }

    title = f.CharField(label=_('str_profileForm_title_label'), max_length=32, widget=f.TextInput(attrs=title_attrs), required=False)
    bio = f.CharField(label=_('str_profileForm_bio_label'), max_length=128, widget=f.Textarea(attrs=bio_attrs), required=False)
    email = f.EmailField(label=fl('{} {}', _('str_email'), _('str_public')), max_length=32, widget=f.EmailInput(attrs=email_attrs), required=False)
    image = f.ImageField(widget=f.FileInput(attrs=image_attrs), required=False, help_text=_('str_profileForm_image_helpText'))
    facebook_URL = f.URLField(max_length=256, widget=f.TextInput(attrs=fb_attrs), required=False)
    twitter_URL = f.CharField(max_length=256, widget=f.TextInput(attrs=tw_attrs), required=False)
    linkedin_URL = f.CharField(max_length=256, widget=f.TextInput(attrs=li_attrs), required=False)

    class Meta:
        model = Author
        fields = ('title', 'bio', 'email', 'image', 'facebook_URL', 'twitter_URL', 'linkedin_URL')


class NewCategory(f.ModelForm):
    class Meta:
        model = Category
        name_attrs = {'class':'form-control form-control-lg', 'id':'catego_name', 'type':'text', 'name':'name', 'placeholder': 'Escribe el nombre de la categoría'} 
        desc_attrs = {'class': 'form-control form-control-lg', 'id':'catego_desc', 'type':'text', 'name':'description', 'placeholder': 'Escribe una breve descripción de la categoría'}     

        fields = ('name', 'description', 'image')
        labels = {
            'name': 'Nombre de la categoría',
            'description': 'Descripción de la categoría',
            'image': 'Imagen'
        }

        widgets = {
            'name': f.TextInput(attrs=name_attrs),
            'description': f.TextInput(attrs=desc_attrs),
        }


#Send contact mail
class ContactForm(f.Form):
    name_attrs = {'class':'form-control form-control-lg',  'id':'contact_fullName', 'type':'text', 'name': 'fullname', 'placeholder':_('str_fullName_placeholder')}
    email_attrs = {'class':'form-control form-control-lg', 'id':'contact_email', 'type':'email', 'name':'email', 'placeholder':_('str_yourEmail_placeholder')}
    subject_attrs = {'class':'form-control form-control-lg', 'id':'contact_subject', 'type':'text', 'name':'subject', 'placeholder':_('str_contactForm_subject_placeholder')}
    msg_attrs = {'class':'form-control form-control-lg txtarea-maxh-s', 'id':'contact_message', 'name':'message', 'rows':'2', 'placeholder':_('str_contactForm_message_placeholder')}

    name = f.CharField(label=_('str_contactForm_fullName'), max_length=128, widget=f.TextInput(attrs=name_attrs), required=True)
    email = f.EmailField(label=_('str_email'), max_length=128, widget=f.EmailInput(attrs=email_attrs), required=True)
    subject = f.CharField(label=_('str_subject'), max_length=128, widget=f.TextInput(attrs=subject_attrs), required=True)
    msg = f.CharField(label=_('str_message'), max_length=1024, widget=f.Textarea(attrs=msg_attrs), required=True)


#Subscribe to newsletter
class SubscribeForm(f.Form):
    s_email_attrs = {'class':'form-control bg-none border-dark text-white', 'id':'sub_email', 'type':'email', 'name':'sub_email', 'placeholder': _('str_yourEmail_placeholder')}
    s_email = f.EmailField(label=_('str_subNewsletter_title'), max_length=128, widget=f.EmailInput(attrs=s_email_attrs), required=True)



   