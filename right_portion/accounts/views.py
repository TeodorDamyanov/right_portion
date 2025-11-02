from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import generic as views
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from .forms import RPUserCreateForm, LoginForm, RPUserEditForm
from .models import RPUser


class UserRegisterView(views.CreateView):
    model = RPUser
    form_class = RPUserCreateForm
    template_name = 'accounts/register_page.html'
    success_url = reverse_lazy('index')


class UserLoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'accounts/login-page.html'
    next_page = reverse_lazy('index')


class UserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')


class UserEditView(views.UpdateView):
    model = RPUser
    form_class = RPUserEditForm
    template_name = 'accounts/profile-edit-page.html'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.pk})


class UserDetailsView(views.DetailView):
    template_name = 'accounts/profile-details-page.html'
    model = RPUser

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     foods = self.object.food_set.all()
    #     paginator = Paginator(foods, 2)
    #     page_num = self.request.GET.get('page') or 1
    #     page_obj = paginator.get_page(page_num)

    #     context.update({
    #         "paginator": paginator,
    #         "page_num": page_num,
    #         "page_obj": page_obj,
    #         "foods": foods
    #     })

    #     return context


class UserDeleteView(views.DeleteView):
    model = RPUser
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('index')

    def post(self, *args, pk):
        self.request.user.delete()