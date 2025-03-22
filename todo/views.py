from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Task, Profile
from .forms import TaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def task_list(request):
    """
    List all tasks sorted by due date.
    This view is accessible to everyone.
    """
    tasks = Task.objects.all().order_by('due_date')
    return render(request, 'todo/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    """
    Create a new task. Only accessible to logged-in users.
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user # Set the author field
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form, 'action': 'Create'})


@login_required
def task_update(request, pk):
    """
    Update an existing task identified by its primary key.
    Only the author is allowed to update the task
    """
    task = get_object_or_404(Task, pk=pk)
    if task.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this task.")
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form, 'action': 'Update'})


@login_required
def task_delete(request, pk):
    """
    Delete a task after confirmation.
    Only the author is allowed to delete the task.
    """
    task = get_object_or_404(Task, pk=pk)
    if task.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this task.")
    
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'todo/task_confirm_delete.html', {'task': task})



def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create empty profile for new user
            Profile.objects.create(user=user)
            messages.success(request, f'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})



@login_required
def profile(request):
    # Get or create profile if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'registration/profile.html', context)


