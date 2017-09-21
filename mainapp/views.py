from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect
from mainapp.models import Post, Likes, Post_comments
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt


def main_page(request):
    if not request.user.is_authenticated():
        return redirect("/auth")

    args = {}
    args["user"] = auth.get_user(request)

    if 'search' in request.GET and request.GET['search']:
        page = request.GET.get('page', 1)

        search = request.GET['search']
        word = Post.objects.filter(Q(post_title__icontains=search) | Q(post_description__icontains=search)).order_by('-id')
        paginator = Paginator(word,2)
        try:
            args["data"] = paginator.page(page)
            args["query"] = search
        except PageNotAnInteger:
            args["data"] = paginator.page(1)
            args["query"] = search
        except EmptyPage:
            args["data"] = paginator.page(paginator.num_pages)
            args["query"] = search

        return render_to_response('allpost.html', args)
    if 'country' in request.GET and request.GET['country']:
        page = request.GET.get('page', 1)

        country = request.GET['country']
        word = Post.objects.filter(post_authors__country=country).order_by('-id')
        paginator = Paginator(word,2)
        try:
            args["data"] = paginator.page(page)
            args["country"] = country
        except PageNotAnInteger:
            args["data"] = paginator.page(1)
            args["country"] = country
        except EmptyPage:
            args["data"] = paginator.page(paginator.num_pages)
            args["country"] = country

        return render_to_response('allpost.html', args)
    if 'city' in request.GET and request.GET['city']:
        page = request.GET.get('page', 1)

        city = request.GET['city']
        word = Post.objects.filter(post_authors__city=city).order_by('-id')
        paginator = Paginator(word, 2)
        try:
            args["data"] = paginator.page(page)
            args["city"] = city
        except PageNotAnInteger:
            args["data"] = paginator.page(1)
            args["city"] = city
        except EmptyPage:
            args["data"] = paginator.page(paginator.num_pages)
            args["city"] = city
        return render_to_response('allpost.html', args)
    else:
        all_post = Post.objects.all().order_by("-id")
        page = request.GET.get('page', 1)

        paginator = Paginator(all_post, 2)
        try:
            args["data"] = paginator.page(page)
        except PageNotAnInteger:
            args["data"] = paginator.page(1)
        except EmptyPage:
            args["data"] = paginator.page(paginator.num_pages)

        return render(request, 'allpost.html', args)


def single_post(request, id):
    if not request.user.is_authenticated():
        return redirect("/auth")
    args={}
    post = Post.objects.get(id=id)
    args['data'] = post
    all_comments = Post_comments.objects.filter(comments_post=post).order_by("-id")
    page = request.GET.get('page', 1)
    paginator = Paginator(all_comments, 5)
    try:
        args['comments'] = paginator.page(page)
    except PageNotAnInteger:
        args['comments'] = paginator.page(1)
    except EmptyPage:
        args['comments'] = paginator.page(paginator.num_pages)
    return render(request, 'singlepost.html', args)


def sendcomment(request, id):
    if not request.user.is_authenticated():
        return redirect("/auth")
    post = Post.objects.get(id=id)
    comment = Post_comments.objects.create(comments_author=auth.get_user(request), comments_post = post,
                                           comments_text =request.POST['text'])
    comment.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def likedislike(request, post_id):
    if not request.user.is_authenticated():
        return redirect("/auth")
    post = Post.objects.get(id=post_id)
    try:
        Likes.objects.get(like_to_post = post, like_from_user = auth.get_user(request) ).delete()
    except:
        addlike = Likes.objects.create(like_to_post = post, like_from_user = auth.get_user(request))
        addlike.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))