from django.urls import path
from . import views

app_name = 'nl2ocl'
urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('random', views.random.as_view(), name='random'),
    path('easy', views.easy.as_view(), name='easy'),
    path('harder', views.harder.as_view(), name='harder'),
    path('sameModel/<int:rel>/', views.sameModel.as_view(), name='sameModel'),
    path('question/<int:rel>/', views.question.as_view(), name='question'),
    path('saveT/<int:rel>/', views.saveTranslation.as_view(), name='saveTranslation'),
    path('umlimage/<int:rel>/', views.getUMLImage.as_view(), name='umlimage'),

    path('new/<int:rel>/', views.newQuestion.as_view(), name='newQuestion'),
]