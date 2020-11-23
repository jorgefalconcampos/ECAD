import os 
from django.db import models as m
#Importando "pre_save" para auto-generar el slug del post y "post_save" para auto-generar/actualizar el modelo Autor                    
from django.db.models.signals import pre_save, post_save 
from django.dispatch import receiver
from taggit.managers import TaggableManager
from django.utils import timezone
from ecad_project.utils import unique_slug_generator #Importando el the auto slug generator
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify



# Modelo Author, representa un "autor" o profesor quién escribe posts y tiene accesos al dashboard
class Author(m.Model):
    name = m.OneToOneField(User, on_delete=m.CASCADE, related_name='autor')
    slug = m.SlugField(unique=True, null=True, blank=True)
    title = m.CharField(max_length=100, blank=True)
    email = m.EmailField(unique=True, null=True)
    image = m.ImageField(upload_to='author/img/', default='author/default-img.png')
    bio = m.TextField(max_length=500)
    facebook_URL = m.URLField(null=True, blank=True)
    twitter_URL = m.URLField(null=True, blank=True)
    linkedin_URL = m.URLField(null=True, blank=True)
    activated_account = m.BooleanField(default=False)

    def __str__(self):
        return self.name.username

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Author.objects.create(name=instance)
        if not User.is_superuser:
            instance.Author.save()

    # @receiver(pre_save, sender=User)
    # def save_instance(sender, instance, **kwargs):
    #     instance.Author.save()

    def image_filename(self):
        return os.path.basename(self.image.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.first_name+' '+self.name.last_name)
        super (Author, self).save(*args, **kwargs)

    def activate_account(self, *args, **kwargs):
        self.activated_account = True
        super (Author, self).save(*args, **kwargs)



# Modelo Category, representa una "categoría", tema, o materia en términos generales
class Category(m.Model):
    name = m.CharField(max_length=100)
    description = m.CharField(max_length=300)
    slug = m.SlugField(unique=True)
    image = m.ImageField(upload_to='categories/', default='no-category.png')

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super (Category, self).save(*args, **kwargs)
   



# Status en los que se puede encontrar el post
post_status = (
    (0, 'Draft'),
    (1, 'Approved'),
    (2, 'Rejected'),
    (3, 'Archived')
)


# Modelo Post, representa una "nota", apunte o anotación
class Post(m.Model):
    author = m.ForeignKey(Author, on_delete=m.CASCADE, related_name='author')
    title = m.CharField(max_length=150)
    subtitle = m.CharField(max_length=200, blank=True) #Subtitulo es opcional
    slug = m.SlugField(unique=True)
    category = m.ForeignKey(Category, on_delete=m.CASCADE, related_name='catego', default='1')
    image = m.ImageField(upload_to='img/', default='no-img.png')
    unsplash_URL = m.URLField(null=True, blank=True)
    post_body = m.TextField() #Post body
    tags = TaggableManager() #Tags
    created_date = m.DateTimeField(default=timezone.now)
    published_date = m.DateTimeField(blank=True, null=True)
    status = m.IntegerField(choices=post_status, default=0)
    # Reacciones y votos para el post: fav, util, like o dislike
    vote_fav = m.IntegerField(default=0) 
    vote_util = m.IntegerField(default=0)     
    vote_tmbup = m.IntegerField(default=0) 
    vote_tmbdn = m.IntegerField(default=0)
    send_to_newsletter = m.BooleanField(null=True, default=False) 

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def approve_post(self):
        self.published_date = timezone.now()
        self.status = 1
        self.save()
    
    def reject_post(self):
        self.status = 2
        self.save()

    def archive_post(self):
        self.status = 3
        self.save()

    def unarchive_post(self):
        self.status = 0
        self.save()

    def all_cmts(self):
        return Comment.objects.filter(in_post=self).count() or False

    def approved_cmts(self):
        return Comment.objects.filter(in_post=self, is_approved=True).count()

    def non_approved_cmts(self):
        return Comment.objects.filter(in_post=self, is_approved=False).count()
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super (Post, self).save(*args, **kwargs)




# Modelo Comment, representa un "comentario" dentro de un post
class Comment(m.Model):
    in_post = m.ForeignKey(Post, on_delete=m.CASCADE, related_name="comments")
    author = m.CharField(max_length=125)
    author_email = m.EmailField()
    comment_body = m.TextField()
    created_date = m.DateTimeField(auto_now_add=True)
    is_approved = m.BooleanField(default=False)
    has_report = m.BooleanField(default=False)

    # approve method, to approve or disapprove comments
    def approve(self):
        self.is_approved = True
        self.save()

    def report(self):
        self.has_report = True
        self.save()

    def approved_comments(self):
        return self.Comment.objects.filter(is_approved=True)


# Modelo Misc, representa un objeto "misceláneo", puede ser un anuncio general, página de reglas, cookies (si aplica) etc
class Misc(m.Model):
    name = m.CharField(max_length=100)
    date = m.DateTimeField(default=timezone.now)
    head_desc = m.CharField(max_length=200) #Description for HTML
    bgImage = m.URLField(max_length=500)
    content = m.TextField() #Post body
    
    def __str__(self):
        return self.name




# Modelo Subscriber, representa un "suscriptor" que está suscrito al Newsletter
class Subscriber(m.Model):
    email = m.EmailField(unique=True)
    conf_num = m.CharField(max_length=15)
    confirmed = m.BooleanField(default=False)

    def __str__(self):
        return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"





    
# Auto-generador de slug para una instancia del modelo Post cuando es guardado de una petición HTTP (form)
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Post)