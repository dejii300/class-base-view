from django.shortcuts import render

from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from Book.forms import AddForm
from Book.models import Books
from django.db.models import F
from django.utils import timezone

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect

class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full_path(),
                                    self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('/books')            
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)                    


class BookDeleteView(DeleteView):

    model = Books
    template_name = 'delete.html'
    context_object_name = 'book'
    success_url = '/books/'

    



class BookUpdateView(UserAccessMixin, UpdateView):
    raise_exception = False
    permission_required = 'Book.change_books'
    permission_denied_message = ""
    login_url = '/books/'
    redirect_field_name = 'next'

    model = Books
    template_name = 'add.html'
    form_class = AddForm
    success_url = '/books/'

"""
class AddBookView(FormView):
    template_name = 'add.html'
    form_class = AddForm
    success_url = '/books/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
"""       
class AddBookView(CreateView):
    model = Books
    template_name = 'add.html'
    form_class = AddForm
    success_url = '/books/'

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        initial['title'] = 'Enter Title'
        initial['genre'] = 'Enter Genre'
        return initial


"""
class IndexView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Books.objects.all()
        return context
"""

class IndexView(ListView):
    model = Books
    template_name = "home.html"
    context_object_name = 'books'
    paginate_by = 2

    #def get_queryset(self):
        #return Books.objects.all()[:3]


class GenreView(ListView):
    model = Books
    template_name = 'home.html'
    context_object_name = 'books'
    paginate_by = 1

    def get_queryset(self, *args, **kwargs):
        return Books.objects.filter(genre__icontains=self.kwargs.get('genre'))



class BookDetailView(DetailView):

    model = Books
    template_name = 'book-detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = Books.objects.filter(slug=self.kwargs.get('slug'))
        post.update(count=F('count') + 1)

        context['time'] = timezone.now()

        return context
    
    


