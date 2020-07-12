from django.urls import path, include
from app import views
from django.conf.urls import url
urlpatterns = [
    path('content',views.article_content),
    path('index',views.get_index_page),
    # path('detail', app.views.get_detail_page)
    path('detail/<int:article_id>',views.get_detail_page),
    url('detail/add_dis/(\d+)',views.add_dis),
    path('add_blog',views.add_blog),
]

