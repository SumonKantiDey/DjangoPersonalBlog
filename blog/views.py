from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post,Comment
from django.utils import timezone
from .forms import PostForm,CommentForm
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.urls import reverse_lazy #Unlike the traditional reverse function, reverse_lazy won't execute until the value is needed.
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    template_name = 'coreblog/post_list.html'
    model = Post
    paginate_by = 2
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post    #get_absolute_url will redirect after create new post which is define in Post model
class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post 
class DraftListView(LoginRequiredMixin, ListView):
    #template_name = "post_draft_list.html"
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')  

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list') #http://cheng.logdown.com/posts/2015/05/25/django-reverse-vs-reverse-lazy


#####################################
# Function that requires a pk match #
#####################################
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk= pk)
    post.publish()
    return redirect('post_detail', pk = pk)

#@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk) #https://realpython.com/django-redirects/
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk= pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk) #post attribute  of comment model 

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
