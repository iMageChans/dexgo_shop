from django.urls import path
from .views import RegisterView, LoginView, GenerateInviteCodeView, ShareInviteCodeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('generate-invite-code/', GenerateInviteCodeView.as_view(), name='generate-invite-code'),
    path('share-invite-code/', ShareInviteCodeView.as_view(), name='share-invite-code'),

]
