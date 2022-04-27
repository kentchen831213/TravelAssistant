from django.urls import path
from . import views


app_name = 'comment'
urlpatterns = [
    # path('comment_base/', comment_base, name='comment_base'),
    path('comment_detail/', views.comment_detail, name='comment_detail'),
    path('comment_detail/<int:comment_id>/', views.comment_delete, name='comment-delete'),
    path('comment_edit/<int:comment_id>', views.comment_edit, name='comment-edit'),
    path('comment_update/<int:comment_id>', views.comment_update, name='comment-update'),
    # path('comment_detail/<int:comment_id>', views.comment_delete, name='comment_delete'),
    # path('comment_detail/', views.comment_delete, name='comment_delete'),
]
