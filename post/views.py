from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostCreateForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView


class PostCreateView(CreateView):
    form_class = PostCreateForm
    model = Post
    template_name = 'post/post_create.html'

    @method_decorator(login_required(login_url='post:post_list'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(self.request.user)
        return redirect('post:post_list')


class PostUpdateView(UpdateView):
    context_object_name = 'post'
    form_class = PostCreateForm
    model = Post
    pk_url_kwarg = 'post_id'

    # Для создания и обновления поста я использую один шаблон

    template_name = 'post/post_create.html'

    @method_decorator(login_required(login_url='post:post_list'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(self.request.user)
        return redirect('post:post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['update'] = 'update'
        return context


class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'

    def get_context_data(self):
        post_filter = self.kwargs.get('my_post', 'all_posts')

        context = super().get_context_data()
        context['posts'] = Post.objects.order_by('created_at')
        context['my_posts'] = post_filter

        '''
        Чтобы не дублировать код, один и тот-же кдласс обрабатывает 
        список постов всех пользователей, а также дает возможность текущему 
        пользователю посмотреть только его посты. 

        Так как классом будут пользоваться не только 
        аутентифицированные пользователи, я не могу закрыть доступ декоратором.

        Вместо декоратора, я проверяю аутентифицированность пользователя 
        проверкой 'if self.request.user.is_authenticated'. 

        Итого. Если пользователь аутентифицирован и нажал на кнопку "Мои 
        посты", пользователю отобразятся только его посты 

        '''

        if post_filter != 'all_posts' and self.request.user.is_authenticated:
            context['posts'] = self.request.user.post.all()
            context['my_posts'] = post_filter

        return context


class PostDetailView(DetailView):
    context_object_name = 'post'
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'post/post_detail.html'


class PostDeleteView(DeleteView):
    context_object_name = 'post'
    model = Post
    success_url = '/'
    pk_url_kwarg = 'post_id'
    template_name = 'post/post_delete.html'

    @method_decorator(login_required(login_url='post:post_list'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



