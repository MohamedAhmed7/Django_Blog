from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'form':form,
    }
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        old_img = request.user.profile.image.url
        old_username = request.user.username
        old_mail  = request.user.email

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            new_img = request.user.profile.image.url
            new_username = request.user.username
            new_mail = request.user.email
            if (new_img != old_img or new_username != old_username or new_mail != old_mail):
                u_form.save()
                # check if the user updated profile image or not to delete the old one
                if(old_img != new_img):
                    try:
                        img_dir = os.getcwd() + old_img
                        os.remove(img_dir)
                    except:
                        print('error deleting old pic')
                    p_form.save()
                messages.success(request, 'Your Account has been updated!')
            else:
                messages.warning(request, 'Nothing to be Updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)