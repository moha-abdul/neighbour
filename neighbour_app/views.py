from django.http import HttpResponse,Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import SignupForm,ProfileForm,PostForm
from django.contrib.auth.models import User
from .models import Profile, Posts
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
    posts = Posts.objects.all()
    return render(request, 'neighbour/index.html',{"posts": posts})

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

@login_required
def new_post(request):
    current_user = request.user
    post_form = PostForm()
    if request.method == 'POST':
        post_form =PostForm(request.POST,instance=request.user.profile)
        if post_form.is_valid:
            post_form.save()
        else:
            post_form = PostForm()
            return render(request, 'neighbour/new-post.html', {"post_form": post_form})
    return render(request, 'neighbour/new-post.html', {"post_form":post_form})
