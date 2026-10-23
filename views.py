from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import SignUpForm, PostForm, CommentForm, ProfileForm
from .models import Post, Like, Comment, Profile

def feed(request):
 posts=Post.objects.select_related("author").prefetch_related("likes","comments__author")
 liked=set(Like.objects.filter(user=request.user).values_list("post_id",flat=True)) if request.user.is_authenticated else set()
 return render(request,"network/feed.html",{"posts":posts,"post_form":PostForm(),"comment_form":CommentForm(),"liked_ids":liked})
def signup(request):
 if request.user.is_authenticated: return redirect("feed")
 form=SignUpForm(request.POST or None)
 if request.method=="POST" and form.is_valid():
  user=form.save(); Profile.objects.get_or_create(user=user); login(request,user); messages.success(request,"Welcome to SocialHub!"); return redirect("feed")
 return render(request,"network/signup.html",{"form":form})
@login_required
@require_POST
def create_post(request):
 form=PostForm(request.POST)
 if form.is_valid():
  post=form.save(commit=False); post.author=request.user; post.save(); messages.success(request,"Post published.")
 else: messages.error(request,"Please enter a post (maximum 2,000 characters).")
 return redirect("feed")
@login_required
@require_POST
def delete_post(request, post_id):
 post=get_object_or_404(Post,pk=post_id)
 if post.author_id==request.user.id: post.delete(); messages.success(request,"Post deleted.")
 else: messages.error(request,"You can only delete your own posts.")
 return redirect(request.META.get("HTTP_REFERER") or "feed")
@login_required
@require_POST
def toggle_like(request, post_id):
 post=get_object_or_404(Post,pk=post_id); like,created=Like.objects.get_or_create(user=request.user,post=post)
 if not created: like.delete()
 return redirect(request.META.get("HTTP_REFERER") or "feed")
@login_required
@require_POST
def add_comment(request, post_id):
 post=get_object_or_404(Post,pk=post_id); form=CommentForm(request.POST)
 if form.is_valid():
  comment=form.save(commit=False); comment.author=request.user; comment.post=post; comment.save()
 else: messages.error(request,"Comment must contain 1–500 characters.")
 return redirect(request.META.get("HTTP_REFERER") or "feed")
@login_required
def edit_profile(request):
 profile,_=Profile.objects.get_or_create(user=request.user); form=ProfileForm(request.POST or None,instance=profile)
 if request.method=="POST" and form.is_valid(): form.save(); messages.success(request,"Profile updated."); return redirect("profile",username=request.user.username)
 return render(request,"network/edit_profile.html",{"form":form})
def profile(request, username):
 person=get_object_or_404(User,username=username); posts=person.posts.select_related("author").prefetch_related("likes","comments__author")
 liked=set(Like.objects.filter(user=request.user,post__author=person).values_list("post_id",flat=True)) if request.user.is_authenticated else set()
 return render(request,"network/profile.html",{"person":person,"posts":posts,"liked_ids":liked,"comment_form":CommentForm()})
