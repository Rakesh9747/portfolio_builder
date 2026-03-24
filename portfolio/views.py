from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Education, Project, Skill

# Home
def home(request):
    return render(request, 'home.html')


# Register
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user)

        return redirect('/login/')

    return render(request, 'register.html')


# Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# Logout
def user_logout(request):
    logout(request)
    return redirect('home.html')

from django.contrib.auth.decorators import login_required

@login_required
def create_portfolio(request):
    return render(request, 'create.html')

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        template = request.POST.get('template')
        if template:
            profile.template = template
            profile.save()
            return redirect('/build/')

    return render(request, 'dashboard.html', {'profile': profile})
def portfolio_view(request, username):
    
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)

    education = Education.objects.filter(user=user)
    projects = Project.objects.filter(user=user)
    skills = Skill.objects.filter(user=user)

    # 🔥 Preview feature
    
    preview_template = request.GET.get('preview')
    profile.bio = request.POST.get('bio', profile.bio)
    if preview_template:
        template_name = f"{preview_template}.html"
    else:
        template_name = f"{profile.template}.html"

    return render(request, template_name, {
        'profile': profile,
        'education': education,
        'projects': projects,
        'skills': skills
    })

@login_required
def select_template(request):
    if request.method == 'POST':
        template = request.POST['template']
        profile = Profile.objects.get(user=request.user)
        profile.template = template
        profile.save()

        return redirect('/build/')

    return render(request, 'select_template.html')

@login_required
def build_portfolio(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Update Profile
        profile.bio = request.POST.get('bio', profile.bio)
        profile.github = request.POST.get('github', profile.github)
        profile.linkedin = request.POST.get('linkedin', profile.linkedin)
        profile.email = request.POST.get('email', profile.email)

        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES['profile_image']

        profile.save()

        # Add Skill if provided
        skill_name = request.POST.get('skill')
        if skill_name:
            Skill.objects.create(user=request.user, name=skill_name)

        # Add Project if provided
        project_title = request.POST.get('project_title')
        project_desc = request.POST.get('project_desc')
        project_link = request.POST.get('project_link')
        if project_title and project_desc:
            Project.objects.create(
                user=request.user, 
                title=project_title, 
                description=project_desc,
                link=project_link or ''
            )
            
        # Add Education if provided
        degree = request.POST.get('degree')
        college = request.POST.get('college')
        year = request.POST.get('year')
        if degree and college:
            Education.objects.create(
                user=request.user,
                degree=degree,
                college=college,
                year=year or ''
            )

        # Handle deletions if any id is passed
        delete_skill = request.POST.get('delete_skill')
        if delete_skill:
            Skill.objects.filter(id=delete_skill, user=request.user).delete()
            
        delete_project = request.POST.get('delete_project')
        if delete_project:
            Project.objects.filter(id=delete_project, user=request.user).delete()
            
        delete_education = request.POST.get('delete_education')
        if delete_education:
            Education.objects.filter(id=delete_education, user=request.user).delete()

        # Check if user clicked publish/view instead of just save
        if 'publish' in request.POST:
            return redirect(f'/portfolio/{request.user.username}/')
        
        # Otherwise redirect back to build page to continue editing
        return redirect('/build/')

    context = {
        'profile': profile,
        'skills': Skill.objects.filter(user=request.user),
        'projects': Project.objects.filter(user=request.user),
        'education': Education.objects.filter(user=request.user)
    }
    return render(request, 'build.html', context)