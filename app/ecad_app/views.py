import datetime, math, json, urllib, smtplib
from django.utils import timezone
from django.template.defaultfilters import date
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import gettext as _
from taggit.models import Tag
from django.db.models import Count, Q, F
from decouple import config
from django.views.decorators.http import require_GET
from . decorators import check_recaptcha
from . helpers import mail_newsletterv2, send_activation_linkv2, send_contact_message, send_newsletter_mail
from . models import Post, Category, Author, Comment, Misc, Subscriber  #Importing the models
from . forms import PostForm, CommentForm, CreateUserForm, AccountEditUserForm, ProfileEditUserForm, ProfileEditAuthorForm, ContactForm, SubscribeForm, NewCategory, SearchForm
#User, Admin & Superuser
from django.utils.text import slugify
from django.contrib import messages #To customize login & signup forms
from django.contrib.auth import authenticate, login as do_login, logout as do_logout
from django.contrib.auth.decorators import login_required, user_passes_test # upt is to restrict to super user only
from django.template.loader import render_to_string
from . tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode




# ==============================#
# ====== Config section ====== #
# =============================#


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /private/",
        "Disallow: /junk/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


# ============================#
# ====== Base section ====== #
# ============================#


def getdata(request):
    results = Post.objects.all()
    jsondata = serializers.serialize('json',results)
    return HttpResponse(jsondata)



def base(request):
    template = 'ecad_app/base.html'
    if request.method == 'GET':
        return redirect('index')
    return render(request, template, context)

def cm(request):
    # notify_new(request)
    # return render(request, 'ecad_app/user/contact-mail.html', {})
    # context = {'action': 'deleted'}
    # return render(request, 'ecad_app/mails/blog/confirm-mail.html')


    # return redirect('index')

    # return render(request, 'ecad_app/mails/user/email-sent.html')
    # return render(request, 'ecad_app/mails/user/wrong-link.html')
    return render(request, 'ecad_app/http_states/404.html')
    # return render(request, 'ecad_app/user/pswd/password-reset-done.html')
    # return render(request, 'ecad_app/user/pswd/password-reset-complete.html')


    # return render(request, 'ecad_app/mails/user/pswd/reset-pass.html')

    # return render(request, 'ecad_app/mails/user/wrong-link.html')



    # return render(request, 'ecad_app/mails/blog/verify.html')



#For searching a Post object
def search(request):
    template = 'ecad_app/search.html'

    if request.method == 'GET':
        search_term = request.GET.get('q')
        bad_query = False
        bad_query_len = False

        if not search_term:
            return render(request, template, {'empty_search':True})

        if len(search_term) <= 2:
            bad_query = True
        elif len(search_term) > 50:
            bad_query_len = True
        else:
            queryset = []
            queries = search_term.split(" ") #python install 2019 --> [python, install, 2019]
            for q in queries:
                posts = Post.objects.filter(
                    Q(title__icontains=q)|
                    Q(subtitle__icontains=q)|
                    Q(post_body__icontains=q)).distinct()

            for post in posts:
                queryset.append(post)

            context = {'results': queryset, 'number': len(queryset), 'query': search_term}
            return render(request, template, context)
    return render(request, template, {'bad_query':bad_query, 'bad_query_len':bad_query_len} )



#This method allows blog readers get in touch with ECAD
@check_recaptcha
def contact(request):
    response_data = {}
    if request.POST.get('action') == 'sendCtct_Form':
        ctct_form = ContactForm(data=request.POST)
        if ctct_form.is_valid() and request.recaptcha_is_valid:
            print('\n\n# --- PY: Form & Captcha passed --- #')
            msg_sender = request.POST.get('name')
            msg_email = request.POST.get('email')
            msg_subject = request.POST.get('subject')
            msg_msg = request.POST.get('msg')
            context = {'name': msg_sender, 'email': msg_email, 'subject': msg_subject, 'msg': msg_msg }
            if send_contact_message(context, msg_subject):
                response_data['success'] = True
            else:
                response_data['success'] = False
            return JsonResponse(response_data)
        else:
            return JsonResponse({'success': False, 'err_code': 'invalid_captcha'})
    else:
        return redirect('index')


#This method adds a new subscriber and send a confirmation mail
def subscribe(request):
    response_data = {}
    if request.POST.get('action') == 'subscribe_Form':
        subscribe_form = SubscribeForm(data=request.POST)
        if subscribe_form.is_valid():
            subscriber_email = request.POST.get('s_email')
            if not Subscriber.objects.filter(email=subscriber_email):
                if mail_newsletterv2(subscriber_email, request):
                    response_data['success'] = True
                else:
                    response_data['success'] = False
                return JsonResponse(response_data)
            else:
                print(f'\n\n# --- PY: The email <<{subscriber_email}>> is already subscribed to newsletter --- #\n')
                return JsonResponse({'success': False, 'already_exists': True})
        else:
            return JsonResponse({'success': False})
    else:
        subscribe_form = SubscribeForm()


 


#Method that allows a subscriber confirm its email and receive updates
def confirm_subscribe(request):
    template = 'ecad_app/mails/blog/verify.html'
    conf_numb = request.GET['id']
    sub = Subscriber.objects.get(conf_num=conf_numb)
    context = {'email': sub.email}

   
    if sub.conf_num == conf_numb:
        if sub.confirmed:
            context['action'] = 'already_confirmed'
        else:
            sub.confirmed = True
            sub.save()
            print(f'\n\n# --- PY: The email <<{sub}>> is now confirmed! --- #\n')
            context['action'] = 'confirmed'
        return render(request, template, context)
    else:
        context['action'] = 'denied'
        return render(request, template, context)




#This method removes a subscriber from the database
def unsubscribe(request):
    template = 'ecad_app/mails/blog/verify.html'
    conf_numb = request.GET['id']
    context = {}
    if Subscriber.objects.filter(conf_num=conf_numb).exists():
        sub = Subscriber.objects.get(conf_num=conf_numb)
        if sub.conf_num == conf_numb:
            print(f'\n\n# --- PY: The email <<{sub.email}>> have been deleted from the database --- #\n')
            sub.delete()
            context['action'] = 'deleted'
            return render(request, template, context)
        else:
            return redirect('index')
    else:
        context['action'] = 'already_deleted'
        return render(request, template, context)




# ===========================#
# ====== Blog section ====== #
# ===========================#

#The homepage
def index(request):
    template_name = 'ecad_app/index.html'
    all_posts = Post.objects.filter(published_date__lte=timezone.now(), status=1).order_by('-published_date') #creating the 'all posts' variable, inside it we'll pass the result of the Query Set

    # all_osts = str(all_posts.count()) #counting all-time posts
    # print(f"TODOS LOS POSTS: {all_osts}")

    common_tags = Post.tags.most_common()[:3] #Getting the latest n trending tags
    trending = []
    for tag in common_tags:
        posts = Post.objects.filter(tags=tag, status=1) #Getting a QuerySet with all the posts that contains the common n tags
        for post in posts: #Accessing to each post inside the QuerySet
            if post not in trending:
                trending.append(post) #Putting that post inside the trending array list

    all_categories = Category.objects.all()


    try:
        avg = math.ceil(all_posts.count()/all_categories.count()) #Getting the average between all posts divided by number of categories
        popular_categories = Category.objects.annotate(post_count=Count('catego')).filter(post_count__gte=avg)
        #Once average is calculated, we filter categories that have more or equal posts (gte) than the average
        # print(f" categorias: {popular_categories}")
        diccionario = {}
        for category in popular_categories:
            how_many = all_posts.filter(category=category).count() #Getting how many posts with that popular category exists
            if len(diccionario) < 8:
                diccionario[category]=how_many
    except Exception as e:
        diccionario = {}

    # print(diccionario)
    paginator = Paginator(all_posts, 9) #n posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context = { 'all_posts': all_posts, 'trending': trending[:3], 'page': page, 'post_list': post_list, 'popular_categories': diccionario }
    return render(request, template_name, context)





#This method shows the detail of the selected post of the blog
@check_recaptcha
def post_detail(request, category_text, slug_text):
    template = 'ecad_app/post_detail.html'
    post = get_object_or_404(Post, slug=slug_text)

    # if post isn't approved yet, only the author and superuser can see it in detail, otherwise redirect to index
    if post.status != 1:
        if not ((request.user == post.author.name) or (request.user.is_superuser)):
            return redirect('index')

    more_from_author = Post.objects.filter(author=post.author, status=1).exclude(slug=post.slug).order_by('-published_date')[:3]
    related = post.tags.similar_objects()[:3] #Getting the last 3 posts that contains the same tags that the current post
    all_comments = post.comments.filter(is_approved=True) # Filtering only approved comments
    new_comment = None
    response_data = {}
    response_data_r = {'success': True}

    if request.POST.get('action') == 'reaction_Form':
        try:
            if request.POST.get('reaction') == 'fav':
                post.vote_fav = F('vote_fav')+1
            elif request.POST.get('reaction') == 'util':
                post.vote_util = F('vote_util')+1
            elif request.POST.get('reaction') == 'thumbs_up':
                post.vote_tmbup = F('vote_tmbup')+1
            elif request.POST.get('reaction') == 'thumbs_down':
                post.vote_tmbdn = F('vote_tmbdn')+1
        except:
            response_data_r['success'] = False
        finally:
            post.save()
            return JsonResponse(response_data_r)

    elif request.POST.get('action') == 'newCmt_Form':
        cmt_form = CommentForm(data=request.POST)
        if cmt_form.is_valid() and request.recaptcha_is_valid:
            print('\n\n# --- PY: Form & Captcha passed --- #')
            name = request.POST.get('author')
            email = request.POST.get('author_email')
            cmt = request.POST.get('comment_body')
            response_data['success'] = True
            response_data['cmt_name'] = name
            response_data['cmt_name'] = email
            response_data['cmt_name'] = cmt
            new_comment = cmt_form.save(commit=False) #Create a new comment but don't save it to the DB yet
            new_comment.in_post = post #Assign the current post to the comment
            new_comment.save()
            print(f"\n# --- Form & Captcha were valid. More info: --- #\n{response_data}")
            return JsonResponse(response_data)
        else:
            return JsonResponse({'success': False, 'err_code': 'invalid_captcha'})
    else:
        cmt_form = CommentForm()

    context = {
        'post': post,
        'related_posts': related,
        'more_from_author': more_from_author,
        'comments': all_comments,
        'new_comment': new_comment,
        'cmt_form': cmt_form
    }

    return render(request, template, context )




#All authors page
def authors(request):
    template = 'ecad_app/authors.html'
    details = []

    all_authors = Author.objects.filter(activated_account=True).order_by('name__first_name', 'name__last_name')
    print(all_authors)
    for author in all_authors:
        dicc = {}
        num = Post.objects.filter(author=author, status=1).count()
        dicc['author'] = author
        dicc['posts'] = num
        details.append(dicc)
    paginator = Paginator(details, 9) #n authors in each page
    page = request.GET.get('page')
    try:
        authors_list = paginator.page(page)
    except PageNotAnInteger:
        authors_list = paginator.page(1)
    except EmptyPage:
        authors_list = paginator.page(paginator.num_pages)
    context = {'page': page, 'authors_list': authors_list}
    return render(request, template, context)





#Author detail
def author_detail(request, pinchiautor):
    template = 'ecad_app/author_detail.html'
    author = get_object_or_404(Author, slug=pinchiautor)
    posts_by_author = Post.objects.filter(author__slug=pinchiautor, status=1).order_by('-published_date')  #Getting al posts by the current author
    paginator = Paginator(posts_by_author, 6)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context = { 'author': author, 'page': page, 'post_list': post_list }
    return render(request, template, context)



#All Tags page
def tags(request):
    template = 'ecad_app/tags.html'
    all_tags = Tag.objects.all()
    #TO DO: If tag belongs to a non-approved post, hide that tag
    context = { 'all_tags': all_tags }
    return render(request, template, context)



# A particular tag page
def tags_detail(request, slug):
    template = 'ecad_app/tags_detail.html'
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status=1).order_by('-published_date')
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context = { 'tag': tag, 'post_list': post_list }
    return render(request, template, context)



# ALL categories page
def categories(request):
    template = 'ecad_app/categories.html'
    all_categories = Category.objects.all()
    diccionario = {}
    for category in all_categories:
        how_many = Post.objects.filter(category=category, status=1).count() #Getting how many posts with that popular category exists
        diccionario[category]=how_many
    context = { 'categories': diccionario }
    return render(request, template, context)



# A particular category page
def categories_detail(request, slug):
    template = 'ecad_app/categories_detail.html'
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status=1).order_by('-published_date')
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    context = { 'category': category, 'post_list': post_list}
    return render(request, template, context)



#About page
def about(request):
    context = {}
    return render (request, 'ecad_app/about.html', context)



#Custom error 404 http states
def page_not_found_404(request, exception):
    return render (request, 'ecad_app/http_states/404.html', {})




# ===================================#
#  ===== Miscellaneous section ===== #
# ===================================#


def rules(request):
    template =  'ecad_app/misc/rules.html'
    rules = Misc.objects.filter(Q(name__contains="reglas")|Q(head_desc__contains="reglas")).first()
    context = { 'misc': rules }
    return render(request, template, context)


@login_required(login_url='login')
def tutorial(request):
    template =  'ecad_app/misc/tutorial.html'
    rules = Misc.objects.filter(Q(name__contains="tutorial")|Q(head_desc__contains="tutorial")).first()
    context = { 'misc': rules }
    return render(request, template, context)





# ==================================#
# ====== User/Author section ====== #
# ==================================#



def login(request):
    template = 'ecad_app/user/login.html'
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.POST.get('action') == 'login_Form':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if (username and password):
                user = authenticate(request, username=username, password=password)
                if user is not None and user.is_active:
                    do_login(request, user)
                    return JsonResponse({'status': True})
                else:
                    return JsonResponse({'status': False, 'err_code': 'login_failed'})
            else:
                return JsonResponse({'status': False, 'err_code': 'invalid_form'})
    context = {}
    return render(request, template, context)



@login_required(login_url='login')
def dashboard(request):
    template = 'ecad_app/user/dashboard.html'
    author = Author.objects.filter(name=request.user).first()
    posts_by_author = Post.objects.filter(author=author).order_by('-created_date')[:5]
    context = { 'author': author, 'posts_by_author': posts_by_author}
    return render (request, template , context)



@login_required(login_url='login')
def profile(request):
    author = Author.objects.filter(name=request.user).first()
    total_post_list = Post.objects.filter(author=author)
    posts = {'approved':0, 'draft':0, 'archived':0, 'rejected':0}
    reactions = {'fav':0, 'util':0, 'tmbup':0, 'tmbdn':0}

    for post in total_post_list:
        if post.status == 0:
            posts['draft'] += 1
        elif post.status == 1:
            posts['approved'] += 1
            reactions['fav'] += post.vote_fav
            reactions['util'] += post.vote_util
            reactions['tmbup'] += post.vote_tmbup
            reactions['tmbdn'] += post.vote_tmbdn
        elif post.status == 2:
            posts['rejected'] += 1
        elif post.status == 3:
            posts['archived'] += 1

    total_reactions = sum([int(i) for i in reactions.values()])
    total_posts = sum([int(i) for i in posts.values()])

    context = {'author': author, 'posts': posts, 'total_posts': total_post_list.count(), 'reactions': reactions, 'total_reactions': total_reactions}
    return render (request, 'ecad_app/user/profile.html', context)



@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def new_category(request):
    template = 'ecad_app/user/new_category.html'
    response_data = {'success': False}
    if request.method == 'POST':
        form = NewCategory(data=request.POST, files=request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            if not Category.objects.filter(slug=slugify(name)).exists():
                newCateg = form.save(commit=False)
                newCateg.save()
                form.save_m2m()
                response_data['success'] = True
                return JsonResponse(response_data)
            else:
                response_data['err_code'] = 'already_exists'
                return JsonResponse(response_data)
        else:
            response_data['err_code'] = form.errors
            return JsonResponse(response_data)
    else:
        form = NewCategory()
    context = {'newCategoryForm':form}
    return render(request, template, context)



@login_required(login_url='login')
def settings(request):
    template = 'ecad_app/user/settings.html'
    author = Author.objects.get(name=request.user)

    response_data = {}

    if request.POST.get('action') == 'profile_Form':
        profile_user_form = ProfileEditUserForm(data=request.POST, instance=request.user)
        profile_author_form = ProfileEditAuthorForm(data=request.POST, instance=author, files=request.FILES)
        if  profile_user_form.is_valid() and profile_author_form.is_valid():
            prof_user = profile_user_form.save(commit=False)
            prof_user.save()
            prof_author = profile_author_form.save(commit=False)
            prof_author.save()
            response_data['success'] = True
            return JsonResponse(response_data)
        else:
            return JsonResponse({'success': False})
    else:
        profile_user_form = ProfileEditUserForm(instance=request.user)

    if request.POST.get('action') == 'account_Form':
        a_mail = request.user.email
        acc_form = AccountEditUserForm(request.POST, instance=request.user)
        if acc_form.is_valid():
            if User.objects.filter(email=request.POST.get('email')).exclude(email=a_mail).exists() == True:               
                return JsonResponse({'success': False, 'errors': 'email_already_taken'})              
            else:
                acc_form.save()
                response_data['success'] = True
                return JsonResponse(response_data)        
        else:
            return JsonResponse({'success': False, 'errors': acc_form.errors})
    else:
        acc_form = AccountEditUserForm(instance=request.user)

    account_frm_initial = { 'username': request.user, 'email': request.user.email }
    profile_frm_user_initial = { 'first_name': request.user.first_name, 'last_name': request.user.last_name }
    profile_frm_author_initial = { 'title': author.title, 'bio': author.bio, 'email': author.email, 'image':author.image, 'facebook_URL': author.facebook_URL, 'twitter_URL': author.twitter_URL, 'linkedin_URL': author.linkedin_URL }

    context = {
        'author': author,
        'AccountForm': AccountEditUserForm(initial=account_frm_initial),
        # --------------------- #
        'ProfileUserForm': ProfileEditUserForm(initial=profile_frm_user_initial),
        'ProfileAuthorUserForm': ProfileEditAuthorForm(initial=profile_frm_author_initial),
    }

    print(author.slug)


    if not request.user.is_superuser:
        avg_user_perms = ['Crear posts en mi nombre', 'Editar posts en mi nombre', 'Archivar posts escritos en mi nombre', 'Eliminar posts escritos en mi nombre', 'Solicitar cambio de contraseña', 'Solicitar restablecimiento de contraseña', 'Crear tags (al crear un post, si el tag no existe)', 'Modificar datos personales públicos', 'Modificar datos personales privados', 'Cambiar imagen de perfil público', 'Login y logout']
        context['permissions'] = avg_user_perms
    else:
        perms = request.user.get_group_permissions()
        context['permissions'] = perms


    return render (request, template, context)




@login_required(login_url='login')
def edit_account_info(request):
    if request.method == 'POST':
        form = EditUserForm(instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EditUserForm(isinstance=request.user)
        context = { 'form':form }
        return render(reques, 'ecad_app/user/settings.html', context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def sign_up(request):
    template = 'ecad_app/user/sign_up.html'
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False #To prevent login to non-confirmed users
            user.save()

            sent_successfully = False
            template = 'ecad_app/mails/user/email-sent.html'

            # context passed to the HttpResponse
            context = {'email': user.email, 'first_name': user.first_name, 'sent_successfully': sent_successfully }
            
            if send_activation_linkv2(user, request):
                context['sent_successfully'] = True 
                rendered = render_to_string(template, context)
                return HttpResponse(rendered)
            else:
                rendered = render_to_string(template, context)
                user.delete()
                return HttpResponse(rendered)
        else:
            messages.error(request, _('ErrorCreatingUser') )
    context = {'form': form}
    return render (request, template, context)


# Allow superuser accepts, rejects, approves posts
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def moderate_posts(request):
    template = 'ecad_app/user/moderate_posts.html'
    all_post_list = Post.objects.filter(status=0).order_by('-created_date')
    paginator = Paginator(all_post_list, 15)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context = {'post_list': post_list, 'all_post_list': all_post_list.count()}
    return render(request, template, context)


# Allow superuser or post's user/author accepts or rejects comments inside a post
@login_required(login_url='login')
def moderate_comments(request):
    template = 'ecad_app/user/moderate_comments.html'
    all_comments = None
    if request.user.is_superuser:
        all_comments = Comment.objects.filter(is_approved=False, in_post__status=1).order_by('-created_date')
    elif request.user.is_authenticated:
        all_comments = Comment.objects.filter(is_approved=False, in_post__status=1, in_post__author__name=request.user).order_by('-created_date')

    all_posts = {}
    details = []

    for comment in all_comments:
        comment_detail = {}
        comment_detail['pk'] = comment.pk
        comment_detail['author'] = comment.author
        comment_detail['author_email'] = comment.author_email
        comment_detail['body'] = comment.comment_body
        comment_detail['created'] = comment.created_date

        if not comment.in_post in all_posts:
            if ((request.user.is_superuser) or (request.user == comment.in_post.author.name)):
                all_posts[comment.in_post] = []

        for k, v in all_posts.items():
            if k == comment.in_post:
                    all_posts[k].append(comment_detail)

    # print(f"\n\n\nDiccionario final: \n\n{all_posts}")

    context = {'all_comments': all_comments, 'all_posts': all_posts}
    return render(request, template, context)


# This method deletes, archives or rejects a blog post - Only superuser can reject
@login_required(login_url='login')
def post_actions(request, post_action, pk):
    response_data = {'success': False}
    post = Post.objects.filter(pk=pk).first()
    if request.user.is_authenticated:
        try:
            if request.user == post.author.name:
                if post_action == 'delete':
                    post.delete()
                    response_data['success'] = True
                elif post_action == 'archive':
                    post.archive_post()
                    response_data['success'] = True
                elif post_action == 'unarchive':
                    post.unarchive_post()
                    response_data['success'] = True
            elif request.user.is_superuser:
                if post_action == 'reject':
                    post.reject_post()
                    response_data['success'] = True
                elif post_action == 'approve':
                    post.approve_post()
                    response_data['success'] = True
                elif post_action == 'approve_n_send':
                    post.approve_post()
                    if send_new_newsletter_mail(request, post):
                        response_data['success'] = True
                    else:
                        response_data['err'] = 'error sending email'
            else:
                response_data['invalid_request'] = f"{request.user} cannot perform this action - is not the author"
        except Exception as e:
            response_data['err'] = str(e)
        finally:
            return JsonResponse(response_data)
    else:
        return redirect('index')


# Given a post pk, this method sents the post to all newsletter susbscribers
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def send_new_newsletter_mail(request, post):
    if send_newsletter_mail(post, request): # 'send_newsletter_mail' lives in helpers.py... be careful
        return True
    else: 
        return False
    


# This method approves or deletes a comment inside a blog post
@login_required(login_url='login')
def comment_actions(request, comment_action, pk):

    response_data = {'success': False}
    comment = Comment.objects.filter(pk=pk).first()
    if request.user.is_authenticated:
        try:
            if ((request.user == comment.in_post.author.name) or (request.user.is_superuser)):
                print('si es el mismo xd')
                if comment_action == 'approve':
                    comment.approve()
                    response_data['success'] = True
                elif comment_action == 'delete':
                    comment.delete()
                    response_data['success'] = True
            else:
                response_data['invalid_request'] = f"{request.user} cannot perform this action"
        except Exception as e:
            response_data['err'] = str(e)
        finally:
            return JsonResponse(response_data)
    else:
        return redirect('index')



def signup_account_activated(request, user):
    template = 'ecad_app/mails/user/account-activated.html'
    context = {'new_user': user}
    return render(request, template, context)



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.refresh_from_db()
        user.is_active = True
        # authorrrr = Author.objects.filter(name=user.pk).first()
        # authorrrr.activated_account = True
        # user.autor.activated_account = True
        # toslug = user.first_name + ' ' + user.last_name
        # user.autor.slug = slugify(toslug)
        # authorrrr.slug = slugify(toslug)
        # authorrrr.save()
        user.save()
        user.autor.activate_account()


        return redirect('account_activated', user=user)
    else:
        template = 'ecad_app/mails/user/wrong-link.html'
        rendered = render_to_string(template, {'user': user } )
        return HttpResponse(rendered)


#This method show all the posts written by user/author
@login_required(login_url='login')
def post_list(request):
    template = 'ecad_app/user/post_list.html'
    author = Author.objects.filter(name=request.user).first()
    all_post_list = Post.objects.filter(author=author).order_by('-published_date')
    paginator = Paginator(all_post_list, 10)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    context = { 'author': author, 'post_list': post_list}
    return render(request, template, context)



#This method allows user/author add a new post
@login_required(login_url='login')
def post_new(request):
    template = 'ecad_app/user/post_edit.html'
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            newpost = form.save(commit=False)
            get_author = Author.objects.get(name=request.user)
            newpost.author = get_author
            newpost.published_date = timezone.now()
            newpost.save()
            form.save_m2m()
            # messages.success(request, _('PostCreated_Ok'))
            return redirect('post_detail', category_text=slugify(newpost.category), slug_text=newpost.slug)
        else:
            messages.error(request, _('EmptyFields'))
    else:
        form = PostForm()
    context = { 'postForm': form }
    if not Category.objects.count():
        context['nocategs'] = True
    return render(request, template, context)



#This method opens a text editor for edit an existing post
@login_required(login_url='login')
def post_edit(request, slug_text):
    template = 'ecad_app/user/post_edit.html'
    post = get_object_or_404(Post, slug=slug_text)
    status = post.status
    slug = post.slug
    title = post.title
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            get_author = Author.objects.get(name=request.user)
            post.author = get_author
            post.published_date = timezone.now()
            post.status = 0
            post.save()
            form.save_m2m()
            return redirect('post_detail', category_text=post.category, slug_text=post.slug)
    else:
        form = PostForm(instance=post)
    context = {'postForm': form, 'is_edit': True, 'post':post }
    return render (request, template, context)




@login_required(login_url='login')
def post_delete(request, pk):
    response_data = {'success': False}
    try:
        post = Post.objects.filter(pk=pk).first()
        if request.user == post.author.name:
            post.delete()
            response_data['success'] = True
        else:
            response_data['invalid_request'] = f"{request.user} cannot perform this action - is not the author"
    except Exception as e:
        response_data['err'] = str(e)
    finally:
        return JsonResponse(response_data)



@login_required(login_url='login')
def post_archive(request, pk):
    response_data = {'success': False}
    try:
        post = Post.objects.filter(pk=pk).first()
        if request.user == post.author.name:
            post.status = 3
            post.save()
            response_data['success'] = True
        else:
            response_data['invalid_request'] = f"{request.user} cannot perform this action - is not the author"
    except Exception as e:
        response_data['err'] = str(e)
    finally:
        return JsonResponse(response_data)



@login_required(login_url='login')
def post_archive(request, slug_text):
    post = get_object_or_404(Post, slug=slug_text)
    post.status = 3
    post.save()
    return redirect('dashboard')

def logout(request):
    do_logout(request)
    return redirect('index')


# ======================================#
# ======= Custom errors section ======= #
# ======================================#


#Custom error 400 (bad request)
def error_400_view(request, exception):
    return render (request, 'ecad_app/http_states/400.html', {})


#Custom error 403 (permission denied)
def error_403_view(request, exception):
    return render (request, 'ecad_app/http_states/403.html', {})


#Custom error 404 (not found)
def error_404_view(request, exception):
    return render (request, 'ecad_app/http_states/404.html', {})


#Custom error 500 (internal server error)
def error_500_view(request):
    return render (request, 'ecad_app/http_states/500.html', {})


