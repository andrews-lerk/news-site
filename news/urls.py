from .views import *
from django.urls import path, re_path


urlpatterns = [
    path('', veiw_home_page, name='home'),
    path('news/', veiw_news_page, name='news'),
    path('post/<slug:post_slug>/', veiw_personal_page, name='personal_new'),
    path('tags/', veiw_tag_page, name='tag_view'),
    path('sign-up/', SignUp.as_view(), name='signup'),
    path('sign-in/', SignIn.as_view(), name='signin'),
    path('log-out/', log_out, name='logout'),
    path('create-comment/', create_comment, name='create_comment'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('profile/', view_profile, name='profile'),
    path('change-name/', change_username, name='change_name'),
    path('change-pass/', change_pass, name='change_pass'),
    path('create-question/', create_question, name='create_question'),
    path('applications/', view_apps_page, name='view_apps'),
    path('download/<int:file_id>/', download, name='download'),
    path('download-resume/', download_resume, name='resume')
]