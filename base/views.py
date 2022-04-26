from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.list import ListView
from .models import Task
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin # restrict access
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

#set debug False in settings.py to catch these exceptions
def handler404(request, exception):
    return render(request, 'base/404.html', status=404)

def handler500(request):
    return render(request, 'base/500.html', status=500)


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True  #prevent logged in user from login page
    
    def get_success_url(self):      #redirect logged in user to tasks
        return reverse_lazy('tasks')
    
    
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True  #not working, using get method(overiden)
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):   #save user from register form
        user = form.save()
        if user is not None: #if user is created log them in
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks' #customize object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user) # get tasks of loged in user
        context['count'] = context['tasks'].filter(complete=False).count() #get count of incomplete tasks
        
        search_input = self.request.GET.get('search-area') or ''    # find search data
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
            
        context['search_input'] = search_input
        
        return context
    
    
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'  #customize object
    template_name = 'base/task.html' #override task_detail.html
    
    
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete', 'header_image']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form): #prevent user from creating task for other users(removed 'user' in fields too)
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)
    
    
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete', 'header_image']
    success_url = reverse_lazy('tasks')
    
    
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')