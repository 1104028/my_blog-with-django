from urllib.parse import quote_plus

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, request
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Comment
from blog.models import Post
from blog.forms import CommentForm
def index(request):
    return render(request, 'home_page.html', )


def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.all()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 15)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "List",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "post_list.html", context)


@login_required
def post_detail(request, pk):
    queryset_list = Post.objects.filter(id=pk)

    return render(request, 'post_detail.html', {'object_list': queryset_list})

@method_decorator(login_required, name='dispatch')
class PostCreate(CreateView):
    model = Post
    fields = ['author', 'title', 'body', 'image', 'draft', 'created_date', 'published_date', 'status']

class PostUpdate(UpdateView):
    model = Post
    fields = ['author', 'title', 'body', 'image', 'draft', 'created_date', 'published_date', 'status']

class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:postlist')


def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if(request.method =="POST"):
        userform = CommentForm(request.POST)
        if userform.is_valid():
            comment = userform.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        userform = CommentForm

    return render(request,'post_detail.html',{'userform': userform })


@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)