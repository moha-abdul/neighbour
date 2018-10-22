from django.http import HttpResponse,Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import SignupForm,ProfileForm,PostForm, BusinessForm, CommentForm
from django.contrib.auth.models import User
from .models import Profile, Posts, Business, Neighbourhood, Comment
from django.core.mail import EmailMessage

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile=Profile(user=user)
            profile.save()             
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you. Now you can login your account.' '<a href="/accounts/login">Click here</a>')
    else:
        return HttpResponse('Activation link is invalid!')

def home(request):
    neighbourhoods = Neighbourhood.objects.all()
    posts = Posts.objects.all()
    # businesses = Business.objects.all()
    return render(request, 'neighbour/index.html',{"posts": posts, "businesses": businesses, "neighbourhoods": neighbourhoods})

@login_required(login_url="/accounts/login/")
def profile(request):
    current_user = request.user
    profile=Profile.objects.filter(user=request.user)
    # neighbourhood = Neighbourhood.objects.filter(user=request.user)
    return render (request,'neighbour/profile.html',{'profile':profile})

@login_required
def edit_profile(request):
    profile = Profile.objects.filter(user=request.user)
    current_user = request.user
    prof_form = ProfileForm()
    if request.method == 'POST':
        prof_form =ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if prof_form.is_valid:
            prof_form.save()
        else:
            prof_form = ProfileForm()
            return render(request, 'neighbour/edit-profile.html', {"prof_form": prof_form,"profile":profile})
    return render(request, 'neighbour/edit-profile.html', {"prof_form":prof_form,"profile":profile})

# @login_required
# def new_post(request):
#     current_user = request.user
#     # current_neighbourhood = Posts.neighbourhood
#     # post_form = PostForm()
#     if request.method == 'POST':
#         post_form =PostForm(request.POST,request.FILES)
#         if post_form.is_valid:
#             new_post = post_form.save(commit=False)
#             # new_post.neighbourhood = current_neighbourhood
#             new_post.save()
#             print('x')
#         return redirect('/')

#     else:
#         post_form = PostForm()
#         return render(request, 'neighbour/new-post.html', {"post_form": post_form})

@login_required
def single_post(request,post_id):
    post = Posts.objects.get(id=post_id)
    comments = Comment.objects.all()
    co_form = CommentForm()
    return render(request,'neighbour/single-post.html',{"post": post, "co_form":co_form, "comments":comments})

@login_required
def single_biz(request,post_id):
    business = Business.objects.get(id=post_id)
    return render(request,'neighbour/single-biz.html',{"business": business})

@login_required
def new_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            posted = post_form.save(commit=False)
            posted.user = request.user
            posted.neighbourhood = request.user.profile.neighbourhood
            posted.save()
            return redirect('neighbour/neighbour.html',request.user.profile.neighbourhood.id)
    else:
        post_form = PostForm()
    return render(request,'neighbour/new-post.html', locals())

# @login_required
# def new_biz(request):
#     current_user = request.user
#     if request.method == 'POST':
#         biz_form =BusinessForm(request.POST,instance=request.user.profile)
#         if biz_form.is_valid:
#             new_biz = biz_form.save(commit=False)
#             new_biz.user = current_user
#             new_biz.save()
#         return redirect('/')

#     else:
#         biz_form =BusinessForm()
#         return render(request, 'neighbour/new-biz.html',{"biz_form": biz_form})

@login_required
def new_biz(request):
    if request.method == 'POST':
        biz_form = BusinessForm(request.POST, request.FILES)
        if biz_form.is_valid():
            bizna = biz_form.save(commit=False)
            bizna.user = request.user.profile
            bizna.neighbourhood = request.user.profile.neighbourhood
            bizna.save()
            return redirect('neighbour/neighbour.html')
    else:
        biz_form = BusinessForm()
    return render(request, 'neighbour/new-biz.html', locals())

@login_required
def search_biz(request):

    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        searched_biz = Business.objects.filter(name=search_term)
        message = f"{search_term}"

        return render(request, 'neighbour/search.html',{"message":message,"businesses": searched_biz})

    else:
        message = "You haven't searched for any user"
        return render(request, 'neighbour/search.html',{"message":message,"businesses": searched_biz})

@login_required
def neighbour(request,neighbourhood_id):
    users = Profile.objects.filter(id=neighbourhood_id)
    return render(request,'neighbour/neighbour.html',locals())

@login_required
def posts(request):
    posts = Posts.objects.filter(neighbourhood=request.user.profile.neighbourhood)
    # comment = Commment.comment.filter(id=post_id)
    return render(request,'neighbour/posts.html',{"posts":posts})

@login_required
def businesses(request):
    businesses = Business.objects.filter(neighbourhood=request.user.profile.neighbourhood)
    return render(request,'neighbour/businesses.html',locals())

@login_required
def comment(request,id):
    upload_comment = Posts.objects.get(id=id)
    if request.method == 'POST':
        co_form = CommentForm(request.POST)
        if co_form.is_valid():
            comment = co_form.save(commit=False)
            comment.user = request.user
            comment.posts = upload_comment
            # print(upload_comment)
            # print('print works')
            comment.save()
        return redirect('posts')