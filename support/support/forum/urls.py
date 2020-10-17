from django.urls import path
from . import views
from .views import (
    QueryCreateView,
    QueryListView,
    QueryUpdateView,
    QueryDeleteView,
    QueryDetailView,
    QueryLikeAPIToggle,
    QueryLikeToggle,
    AnswerCreateView,
    AnswerDeleteView,
    AnswerUpdateView,
    AnswerDetailView,
)

app_name = 'forum'

urlpatterns = [
    # forum url
    path('', views.home, name='home'),
    path('forum/', QueryListView.as_view(), name='list'),

    # query urls
    path('forum/query/new/', QueryCreateView.as_view(), name='query-create'),
    path('forum/query/<slug:slug>/', QueryDetailView.as_view(), name='detail'),
    path('forum/query/<slug:slug>/update/',
         QueryUpdateView.as_view(),
         name='query-update'),
    path('forum/query/<slug:slug>/delete/',
         QueryDeleteView.as_view(),
         name='query-delete'),
    path('forum/query/<slug:slug>/like/',
         QueryLikeToggle.as_view(),
         name='query-likes-toggle'),
    path('api/forum/query/<slug:slug>/like/',
         QueryLikeAPIToggle.as_view(),
         name='query-likes-api-toggle'),

    # answer urls
    path('forum/query/<slug:qslug>/answer/create/',
         AnswerCreateView.as_view(),
         name='answer-create'),
    path('forum/query/<slug:qslug>/answer/<slug:slug>/',
         AnswerDetailView.as_view(),
         name='answer-detail'),
    path('forum/query/<slug:qslug>/answer/update/<slug:slug>',
         AnswerUpdateView.as_view(),
         name='answer-update'),
    path('forum/query/<slug:qslug>/answer/delete/<slug:slug>/',
         AnswerDeleteView.as_view(),
         name='answer-delete'),
]
