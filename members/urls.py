from django.contrib.auth import views as auth_views
from django.urls import path

from . import views  # 导入views模块
from .views import delete_profile_view, make_messages_view, AuthorListView, add_member  # 导入你的视图

urlpatterns = [
    # 用户注册和登录相关路径
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.LogoutView.as_view(next_page='/'), name='logout'),

    # 账户激活相关路径
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('signup_success/', views.signup_success_view, name='signup_success'),  # 注册成功页面
    path('activation_invalid/', views.activation_invalid_view, name='activation_invalid'),  # 激活无效页面

    # 用户资料和编辑
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/delete/', delete_profile_view, name='delete_profile'),  # 删除用户资料

    # 重置密码
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # 会员管理
    path('members/delete/<int:user_id>/', views.delete_member, name='delete_member'),
    path('make_messages/', make_messages_view, name='make_messages'),
    
    # 管理员添加会员的路径
    path('admin/add_member/', add_member, name='add_member'),  
]