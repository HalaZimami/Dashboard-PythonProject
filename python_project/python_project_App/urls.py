from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.index),	
    path('register',views.register),
    path('signup',views.signup),
    path('signin',views.signin),
    path('login',views.login),
    path('dashboard',views.dashboard),
    path('note',views.note),
    path('addnote',views.add_note),
    path('change/<int:note_id>',views.edit_note),
    path('update/note/<int:note_id>',views.update_note),
    path('posts',views.posts),
    path('addpost',views.add_post),
    path('edit/<int:post_id>',views.edit_information),
    path('update/<int:post_id>',views.update_post),
    path('comment/<int:id>',views.comment),
    path('addcomment/<int:id>',views.add_Comments),
    path('image', views.image),
    path('image/delete/<int:id>', views.delete_image, name='delete_image'),
    path('files/', views.files_list, name='file_list'),
    path('files/upload/', views.upload_file, name='upload_file'),
    path('files/<int:id>/', views.delete_file, name='delete_file'),
    path('remove/<int:note_id>',views.delete_Note),
    path('add_todo',views.add_todo),
    path('delete/<int:id>',views.delete_todo),
    path('algo',views.algo),
    path('Algorithm',views.add_algorithm),
    path('profile',views.profile),
    path('logout',views.logout),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    