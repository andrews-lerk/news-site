from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.contrib.auth.models import User
from django.http import FileResponse

from .models import *
from .decorators import counted


def veiw_home_page(request):
    question_form = UserQuestionForm
    return render(request, 'news/index.html', {'ff': question_form})


def veiw_news_page(request):
    """ View all news """
    question_form = UserQuestionForm
    model = NewPost.objects.order_by('-pk')
    side_bar = model[:10]
    paginate = Paginator(model, 2)
    page_number = request.GET.get('page')
    page_obj = paginate.get_page(page_number)
    cat_models = Tag.objects.order_by('-pk')
    return render(request, 'news/news_blog.html',
                  {'ff': question_form, 'model': page_obj, 'cat_models': cat_models, 'model_': model,
                   'side_bar': side_bar})


def veiw_tag_page(request):
    """ View news via tag filter  """
    question_form = UserQuestionForm
    models = NewPost.objects.filter(cat__slug__in=request.POST.getlist('name')).distinct()
    side_bar = models[:10]
    cat_models = Tag.objects.order_by('-pk')
    data = {'ff': question_form, 'model': models, 'cat_models': cat_models,
                   'side_bar': side_bar}
    if request.POST:
        lst_checked = request.POST.getlist('name')
        data['check'] = lst_checked
    return render(request, 'news/news_blog.html', data)


@counted
def veiw_personal_page(request, post_slug):
    """ View detail new """
    question_form = UserQuestionForm
    model = NewPost.objects.filter(slug=post_slug)
    comments = model.first().comments.all()
    comment_form = WriteCommentForm(request.POST or None)
    return render(request, 'news/new_personal.html',
                  {'ff': question_form, 'model': model, 'comments': comments, 'form': comment_form})


def view_apps_page(request):
    question_form = UserQuestionForm
    projects = Applications.objects.all()
    return render(request, 'news/apps_page.html', {'ff': question_form, 'pr': projects})


class SignUp(CreateView):
    form_class = RegisterForm
    template_name = 'news/register.html'
    success_url = reverse_lazy('signin')


class SignIn(LoginView):
    form_class = AuthenticationForm
    template_name = 'news/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form, err='* Incorrect username or password!'))


def log_out(request):
    logout(request)
    return redirect('signin')


def create_comment(request):
    form = WriteCommentForm(request.POST or None)
    url = request.META['HTTP_REFERER'].split('/')
    slug = url[-2]
    post = NewPost.objects.filter(slug=slug)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.auth_user = request.user
        comment.text = form.cleaned_data['text']
        comment.content_type = ContentType.objects.get_for_model(model=NewPost)
        comment.object_id = post.first().id
        comment.save()
    return redirect('personal_new', post_slug=slug)


def create_question(request):
    form = UserQuestionForm(request.POST or None)
    if form.is_valid():
        q = form.save(commit=False)
        q.user_name = form.cleaned_data['user_name']
        q.text = form.cleaned_data['text']
        q.save()
    return redirect('home')


def delete_comment(request, comment_id):
    Comment.objects.filter(pk=comment_id).delete()
    return redirect(request.META['HTTP_REFERER'])


def view_profile(request):
    question_form = UserQuestionForm
    form__ = ChangeUsername(request.POST if request.POST and request.POST['submit'] == 'Change name' else None)
    form_ = ChangePass(request.POST if request.POST and request.POST['submit'] == 'Change pass' else None)
    param = {'form': form__,
             'change': form_,
             'ff': question_form
             }
    check = True if request.POST and request.POST['submit'] == 'Change name' else False
    if check:
        param['error'] = '*This name is already exists!'
    if ChangePass(request.POST):
        param['err'] = form_
    print(request.POST)
    return render(request, 'news/profile.html', param)


def change_username(request):
    form__ = ChangeUsername(request.POST or None)
    if form__.is_valid():
        try:
            User.objects.filter(username=request.user).update(username=form__.cleaned_data['change_name'])
            return redirect('profile')
        except:
            print(request.POST['submit'])
            return view_profile(request)


def change_pass(request):
    form = ChangePass(request.POST or None)
    if form.is_valid() and form.cleaned_data['new_pass'] == form.cleaned_data['new_pass_confirmation']:
        u = User.objects.get(username=request.user)
        u.set_password(form.cleaned_data['new_pass'])
        u.save()
        return redirect('signin')
    return view_profile(request)


def download(request, file_id):
    file = Applications.objects.filter(pk=file_id)
    response = FileResponse(open(file.first().file.path, 'rb'))
    return response


def download_resume(request):
    file = Resume.objects.first()
    response = FileResponse(open(file.file.path, 'rb'))
    return response
