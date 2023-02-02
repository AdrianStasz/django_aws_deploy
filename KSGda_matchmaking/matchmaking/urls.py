from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('reset_password', 
        auth_views.PasswordResetView.as_view(template_name="matchmaking/password_reset.html"), 
        name="reset_password"
        ),
    path('reset_password_sent', 
        auth_views.PasswordResetDoneView.as_view(template_name="matchmaking/password_reset_sent.html"), 
        name="password_reset_done"
        ),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="matchmaking/password_reset_form.html"), 
        name="password_reset_confirm"
        ),
    path('reset_password_complete', 
        auth_views.PasswordResetCompleteView.as_view(template_name="matchmaking/password_reset_done.html"), 
        name="password_reset_complete"
        ),

    path('', views.home, name="home"),
    path('profile/', views.profile, name="profile"),
    path('player/<str:pk>/', views.playerPage, name="player"),
    path('update_player/<str:pk>/', views.update_player, name="update_player"),
    path('promoter/<str:pk>/', views.promoter, name="promoter"),
    path('rate_players/<str:pk>/', views.rate_players, name="rate_players"),
    path('rate_players', views.rate_players, name="rate_players"),
    path('kick_player/<str:match_pk>/<str:player_pk>/', views.kick_player, name="kick_player"),
    path('yellow_card/<str:match_pk>/<str:player_pk>/', views.yellow_card_assign, name="yellow_card"),
    path('red_card/<str:match_pk>/<str:player_pk>/', views.red_card_assign, name="red_card"),
    path('red_card_error/', views.red_card_error, name="red_card_error"),
    path('add_permissions/', views.add_permissions, name="add_permissions"),
    path('add_permission_error/', views.add_permission_error, name="add_permission_error"),
    path('registration_token_change/', views.registration_token_change, name="registration_token_change"),
    path('player/<str:pk>/create_ticket/', views.create_ticket, name="create_ticket"),
    path('ticket/<str:pk>/', views.ticket, name="ticket"),
    path('tickets/', views.tickets, name="tickets"),
    path('ticket_count_error/', views.ticket_count_error, name="ticket_count_error"),
    path('accept_ticket/<str:pk>/', views.accept_ticket, name="accept_ticket"),
    path('decline_ticket/<str:pk>/', views.decline_ticket, name="decline_ticket"),

    path('matches/', views.matches, name="matches"),
    path('my_matches/', views.my_matches, name="my_matches"),
    path('match/<str:pk>/', views.match, name="match"),
    path('match/<str:pk>/comment/', views.add_comment, name="add_comment"),
    path('create_match/', views.create_match, name="create_match"),
    path('create_match_again/<str:pk>/', views.create_match_again, name="create_match_again"),
    path('create_match_form_error/', views.create_match_form_error, name="create_match_form_error"),
    path('create_match_error/', views.create_match_error, name="create_match_error"),
    path('update_match/<str:pk>/', views.update_match, name="update_match"),
    path('update_match_players/<str:pk>/', views.update_match_players, name="update_match_players"),
    path('update_match_result/<str:pk>/', views.update_match_result, name="update_match_result"),
    path('reserve_slots/<str:pk>/', views.reserve_slots, name="reserve_slots"),
    path('delete_match/<str:pk>/', views.delete_match, name="delete_match"),
    path('join_match/<str:pk>/', views.join_match, name="join_match"),
    path('leave_match/<str:pk>/', views.leave_match, name="leave_match"),
    path('history/', views.history, name="history"),
]
 