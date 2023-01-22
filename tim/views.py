from django.shortcuts import render, get_object_or_404

from django.views.generic.base import TemplateView, RedirectView
from tim.models import Post
from django.db.models import F


class Ex2View(TemplateView):

    template_name = "ex2.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.get(id=1)
        context['data'] = "Context Data for Ex2"
        return context

class PostPreLoadTaskView(RedirectView):

    pattern_name = 'tim:singlepost'
    
    def get_redirect_url(self, *args, **kwargs):

        post = Post.objects.filter(pk=kwargs['pk'])
        post.update(count=F('count') + 1)

        return super().get_redirect_url(*args, **kwargs)


class SinglePostView(TemplateView):
    template_name = "ex4.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return context