from . import views
from django.urls import path
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views



# -------------------#
#    App URL'S   #
# -------------------#


urlpatterns = [
    #base:
    path("robots.txt", views.robots_txt),
    path('', views.base, name='base'),
    path('inicio', views.index, name='index'),
    path('buscar', views.search, name='search'),
    path('contact', views.contact, name='contact'),
    path('getdata', views.getdata, name='getdata'),
    #subscriber
    path('subscribe', views.subscribe, name='subscribe'),
    path('confirm', views.confirm_subscribe, name='confirm'),
    path('unsubscribe', views.unsubscribe, name='unsubscribe'),
    #blog
    path('acerca', views.about, name='about'),  
    path('post/<slug:category_text>/<slug:slug_text>/', views.post_detail, name='post_detail'),
    path('tags', views.tags, name='tags'),
    path('tags/<slug:slug>', views.tags_detail, name='tags_detail'),
    path('categorias', views.categories, name='categories'),
    path('categorias/<slug:slug>', views.categories_detail, name='categories_detail'),
    path('autores', views.authors, name='authors'),
    path('autores/<slug:profautor>', views.author_detail, name='author_detail'),
    #misc:
    path('reglas', views.rules, name='rules'),
    path('tutorial', views.tutorial, name='tutorial'),

    # user/author:
    path('usuario/login', views.login, name='login'),
    path('usuario/registar', views.sign_up, name='signup'),
    path('usuario/moderar', views.moderate_posts, name='moderate'),
    path('usuario/moderar-comentarios', views.moderate_comments, name='moderate_comments'),
    path('usuario/categoria/nueva', views.new_category, name='new_category'),
    path('usuario/perfil', views.profile, name='profile'),    
    path('usuario/ajustes', views.settings, name='settings'),
    path('usuario/dashboard', views.dashboard, name='dashboard'),
    path('usuario/posts', views.post_list, name='post_list'),
    path('usuario/post/nuevo', views.post_new, name='post_new'),
    path('usuario/post/borrar/<int:pk>', views.post_delete, name='post_delete'),
    path('usuario/post/perform-action/<str:post_action>/<int:pk>', views.post_actions, name='post_actions'),
    path('usuario/comment/perform-action/<str:comment_action>/<int:pk>', views.comment_actions, name='comment_actions'),
    path('usuario/post/editar/<slug:slug_text>', views.post_edit, name='post_edit'),
    path('activar/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('usuario/cuenta-activada/<str:user>', views.signup_account_activated, name='account_activated'),
    path('usuario/enviar-newsletter/<int:pk>', views.send_newsletter_mail, name='send_newsletter_mail'),
    path('borrar/<slug:slug_text>', views.post_delete, name='post_delete'),
    path('archivar/<slug:slug_text>', views.post_archive, name='post_archive'),
    path('usuario/logout', views.logout, name='logout'),

    #others:
    path('usuario/password-reset/', auth_views.PasswordResetView.as_view(
        template_name='ecad_app/user/pswd/password-reset.html', subject_template_name='ecad_app/mails/user/pswd/reset-pass-mail-subj.txt',
        html_email_template_name='ecad_app/mails/user/pswd/reset-pass-mail.html'),name='password_reset'),    
    path('usuario/password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='ecad_app/user/pswd/password-reset-done.html'), name='password_reset_done'),
    path('usuario/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='ecad_app/user/pswd/password-reset-confirm.html'),name='password_reset_confirm'),
    path('usuario/password-reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name='ecad_app/user/pswd/password-reset-complete.html'),name='password_reset_complete'),
    path('usuario/password-change/', auth_views.PasswordChangeView.as_view(template_name='ecad_app/user/pswd/password-change.html',),name='password_change'),
    path('usuario/password-change/complete', auth_views.PasswordChangeDoneView.as_view(template_name='ecad_app/user/pswd/password-change-done.html'),name='password_change_done'),


]

handler404 = 'ecad_app.views.error_404_view'
