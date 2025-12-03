from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('play/', views.play, name='play'),
    path('tournament/', views.tournament, name='tournament'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('watch/<str:code>/', views.watch_game, name='watch_game'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('guest/', views.guest_mode, name='guest_mode'),
    
    # API endpoints
    path('api/game/create/', views.api_create_game, name='api_create_game'),
    path('api/game/<str:code>/state/', views.api_game_state, name='api_game_state'),
    path('api/game/<str:code>/move/', views.api_game_move, name='api_game_move'),
    path('api/game/<str:code>/join/', views.api_join_game, name='api_join_game'),
    path('api/game/<str:code>/resign/', views.api_resign, name='api_resign'),
    path('api/game/<str:code>/draw/', views.api_offer_draw, name='api_offer_draw'),
    path('api/game/<str:code>/session/', views.api_check_session, name='api_check_session'),
]