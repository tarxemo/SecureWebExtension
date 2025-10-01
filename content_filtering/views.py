from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from .models import *  # Assuming you have a model for allowed URLs
import json
from django.shortcuts import render
from django.db.models import Count
from .models import RestrictedURL, RequestedUrls
from django.utils.timezone import now
from datetime import timedelta


@login_required
def index(request):
    # Get URL statistics
    total_clicks = RequestedUrls.objects.count()
    recent_data = RequestedUrls.objects.filter(visited_at__gte=now() - timedelta(days=30))
    daily_requests = recent_data.values('visited_at__date').annotate(count=Count('id')).order_by('visited_at__date')
    
    # Get recent URLs
    recent_urls = RequestedUrls.objects.order_by('-visited_at')[:5]

    # Example account overview (static data or from another model)
    account_plan = "Pro Plan"
    next_billing = "12th Sep 2024"

    context = {
        'total_clicks': total_clicks,
        'recent_urls': recent_urls,
        'account_plan': account_plan,
        'next_billing': next_billing,
        'daily_requests':daily_requests
    }

    return render(request, 'index.html', context)
 
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RestrictedURL, RequestedUrls
from urllib.parse import urlparse

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RestrictedURL, RequestedUrls
from urllib.parse import urlparse

@csrf_exempt
def check_url(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url')
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'result': 'error', 'message': 'Invalid request format'}, status=400)

        # Parse the provided URL to get the domain
        parsed_url = urlparse(url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # Check if the domain or any subdirectory is in the RestrictedURL model
        restricted_urls = RestrictedURL.objects.filter(url__icontains=domain)
        
        if restricted_urls.exists():
            # Block the URL and create an entry in RequestedUrls
            for restricted_url in restricted_urls:
                RequestedUrls.objects.create(url=restricted_url, rejected=True)
            return JsonResponse({'result': 'blocked'})
        
        # Check for restricted keywords in the URL
        restricted_keywords = RestrictedKeyword.objects.all()
        for keyword in restricted_keywords:
            if keyword.keyword.lower() in url.lower():
                RequestedUrls.objects.create(keyword=keyword, rejected=True)
                return JsonResponse({'result': 'blocked'})
        
        # Allow the URL and create an entry in RequestedUrls
        RequestedUrls.objects.create(unblocked_url=url)
        return JsonResponse({'result': 'allowed'})
    else:
        return JsonResponse({'result': 'error', 'message': 'Only POST requests allowed'}, status=405)



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user but don't save yet to set password
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')  # Redirect to a login page or another page
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {user.username}!')
                return redirect('index')  # Redirect to a profile page or another page after login
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def manage_urls(request):
    restricted_urls = RestrictedURL.objects.all()
    requested_urls = RequestedUrls.objects.all().order_by('-rejected', 'visited_at')[:15]
    context = {
        'restricted_urls': restricted_urls,
        'requested_urls': requested_urls,
    }
    return render(request, 'manage_urls.html', context)


@login_required
def analytics(request):
    # Get the total number of URLs
    total_urls = RestrictedURL.objects.count()

    # Get the total number of requests and clicks
    total_requests = RequestedUrls.objects.count()
    total_clicks = RequestedUrls.objects.exclude(unblocked_url__isnull=True).count()

    # Get the number of URLs rejected
    total_rejected = RequestedUrls.objects.filter(rejected=True).count()

    # Get recent data for visualization (e.g., last 30 days)
    recent_data = RequestedUrls.objects.filter(visited_at__gte=now() - timedelta(days=30))
    daily_requests = recent_data.values('visited_at__date').annotate(count=Count('id')).order_by('visited_at__date')

    context = {
        'total_urls': total_urls,
        'total_requests': total_requests,
        'total_clicks': total_clicks,
        'total_rejected': total_rejected,
        'daily_requests': daily_requests,
    }
    return render(request, 'analytics.html', context)

@login_required
def add_restricted_url(request):
    if request.method == 'POST':
        form = RestrictedURLForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_urls')  # Redirect to the URL management page after saving
    else:
        form = RestrictedURLForm()
    
    return render(request, 'add_restricted_url.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import RestrictedURL
from .forms import RestrictedURLForm  # Make sure to create this form if not existing

def edit_restricted_url(request, pk):
    restricted_url = get_object_or_404(RestrictedURL, pk=pk)

    if request.method == 'POST':
        form = RestrictedURLForm(request.POST, instance=restricted_url)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to a relevant page or URL
    else:
        form = RestrictedURLForm(instance=restricted_url)

    return render(request, 'edit_restricted_url.html', {'form': form})

def delete_restricted_url(request, pk):
    restricted_url = get_object_or_404(RestrictedURL, pk=pk)

    if request.method == 'POST':
        restricted_url.delete()
        return redirect('index')  # Redirect to a relevant page or URL

    return render(request, 'confirm_delete.html', {'restricted_url': restricted_url})

def delete_all_requested_urls(request):
    if request.method == 'POST':
        # Delete all entries in the RequestedUrls table
        RequestedUrls.objects.all().delete()
        return redirect('manage_urls')  # Redirect to a success page or any other URL
    return HttpResponse("Invalid request method", status=405)


def add_restricted_keyword(request):
    if request.method == 'POST':
        form = RestrictedKeywordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_restricted_keyword')
    else:
        form = RestrictedKeywordForm()
    return render(request, 'add_restricted_keyword.html', {'form': form})

def list_restricted_keywords(request):
    keywords = RestrictedKeyword.objects.all()
    return render(request, 'list_restricted_keywords.html', {'keywords': keywords})