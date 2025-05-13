from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
import os
# users/views.py
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Add FILES
        if form.is_valid():
            user = form.save(commit=False)
            # Handle profile picture explicitly
            if 'profile_pic' in request.FILES:
                user.profile_pic.save(
                    f"user_{user.username}_{request.FILES['profile_pic'].name}",
                    request.FILES['profile_pic']
                )
            user.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
# users/views.py
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserChangeForm
from django.contrib.auth import update_session_auth_hash
# users/views.py
@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if form.is_valid():
            user = form.save(commit=False)
            
            # Explicitly handle file upload
            if 'profile_pic' in request.FILES:
                if user.profile_pic:
                    user.profile_pic.delete()
                user.profile_pic = request.FILES['profile_pic']
            
            # Force save all fields
            user.save(update_fields=[
                'username', 'email', 'first_name', 'last_name',
                'profile_pic', 'contact_number'
            ])
            
            # Update session data
            update_session_auth_hash(request, user)
            return redirect('post_list')
        else:
            print("Form errors:", form.errors)  # Debug form validation
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'users/profile_edit.html', {'form': form})