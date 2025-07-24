from django.urls import path
from users.views import sign_up,sign_in,sign_out,activate_user,admin_dashboard,delete_participant,assign_role,create_group,group_list
from users.views import CustomLoginView,ProfileView,EditProfileView,ChangePassword,CustomPasswordResetView,CustomPasswordResetConfirmView
from django.contrib.auth.views import PasswordChangeDoneView

urlpatterns = [
    path("sign-up/",sign_up,name="sign-up"),
    path("sign-in/",CustomLoginView.as_view(),name="sign-in"),
    path("logout/",sign_out,name="logout"),
    path("activate/<int:user_id>/<str:token>/",activate_user),
    path("admin-dashboard",admin_dashboard,name="admin-dashboard"),
    path("delete-participant/<int:id>/",delete_participant,name="delete-participant"),
    path("admin/<int:user_id>/assign-role/",assign_role,name="assign-role"),
    path("admin/create-group/",create_group,name="create-group"),
    path("admin/group-list/",group_list,name="group-list"),
    path("profile/",ProfileView.as_view(), name="profile"),
    path("password-change/",ChangePassword.as_view(),name="password_change"),
    path("password-change/done/", PasswordChangeDoneView.as_view(template_name ="accounts/password_change_done.html"), name="password_change_done"),
    path("password-reset/",CustomPasswordResetView.as_view(),name = "password_reset"),
    path("password-reset/confirm/<uidb64>/<token>/",CustomPasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path("edit-profile/",EditProfileView.as_view(),name='edit_profile')

]

