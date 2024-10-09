import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model, views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .forms import MemberSignUpForm, MemberProfileForm, MemberForm
from .models import MemberProfile
from django.views.generic import ListView
from .models import Member, MemberProfile  # 确保模型导入正确

User = get_user_model()

# 示例的 ListView
class AuthorListView(ListView):
    model = Member
    template_name = 'member_list.html'  # 你需要创建这个模板

# 邮件发送函数
def send_activation_email(user, request):
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    activate_url = reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
    full_url = f"http://{current_site.domain}{activate_url}"

    # 渲染HTML模板
    html_content = render_to_string('activation_email.html', {
        'user': user,
        'full_url': full_url,
    })
    text_content = f"Hi {user.username},\n\nPlease activate your account by clicking the link below:\n{full_url}"

    subject = 'Activate Your Account - Welcome!'
    from_email = 'a6020820914@gmail.com'  # 请更改为有效的发件人邮箱
    recipient_list = [user.email]

    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
        print(f"Activation email sent to {user.email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# 注册视图
def signup_view(request):
    if request.method == 'POST':
        form = MemberSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # 用户未激活
            user.save()

            # 发送激活邮件
            send_activation_email(user, request)
            MemberProfile.objects.create(user=user)  # 创建 MemberProfile 实例

            messages.success(request, '註冊成功！请检查您的邮箱以激活账户。')
            return redirect('signup_success')
    else:
        form = MemberSignUpForm()

    return render(request, 'signup.html', {'form': form})

# 登录视图
def login_view(request):
    # 清除之前的所有消息
    messages.get_messages(request).used = True  # 清除消息

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                login(request, user)
                messages.success(request, '登入成功！')
                return redirect('home')
            else:
                messages.error(request, '用戶名或密碼錯誤。')
        else:
            messages.error(request, '表單無效，請檢查輸入内容。')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

class LogoutView(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)

# 用户资料视图
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

# 删除用户资料视图
@login_required
def delete_profile_view(request):
    user_profile = get_object_or_404(MemberProfile, user=request.user)

    # 删除头像文件
    if user_profile.avatar and os.path.isfile(user_profile.avatar.path):
        os.remove(user_profile.avatar.path)

    user_profile.delete()  # 删除用户资料
    messages.success(request, '资料删除成功！')
    return redirect('profile')  # 或者重定向到其他页面

# 注册成功视图
def signup_success_view(request):
    return render(request, 'signup_success.html')

# 激活链接无效视图
def activation_invalid_view(request):
    return render(request, 'activation_invalid.html')

# 账户激活视图
def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)  # 激活成功后自动登录
        messages.success(request, '帳戶激活成功！')
        return redirect('home')
    else:
        messages.error(request, '激活連結無效或已過期。')
        return render(request, 'activation_invalid.html')

# 用户资料编辑视图
@login_required
def profile_edit_view(request):
    user_profile = get_object_or_404(MemberProfile, user=request.user)

    if request.method == 'POST':
        form = MemberProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            # 处理头像删除
            if 'delete_avatar' in request.POST and user_profile.avatar:
                user_profile.avatar.delete(save=False)  # 删除文件
                user_profile.avatar = None  # 清空数据库中的头像字段

            # 处理头像上传
            new_avatar = request.FILES.get('avatar')
            if new_avatar:
                user_profile.avatar = new_avatar  # 设置新头像
            
            form.save()  # 保存 MemberProfile
            
            # 更新用户的电子邮件和用户名
            user = request.user
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()  # 保存用户信息

            return JsonResponse({"message": "资料更新成功！"}, status=200)  # 返回成功消息
        else:
            return JsonResponse({"message": "更新失败！", "errors": form.errors}, status=400)  # 返回错误信息

    else:
        form = MemberProfileForm(instance=user_profile)

    return render(request, 'profile_edit.html', {'form': form, 'user_profile': user_profile})

# 检查用户是否是管理员的自定义装饰器
def is_admin(user):
    return user.is_staff  # 确保用户具有管理员权限

@user_passes_test(is_admin)  # 仅限管理员使用此功能
def delete_member(request, user_id):
    """删除指定的用户并返回管理会员页面"""
    user = get_object_or_404(User, id=user_id)  # 获取用户或返回404
    user.delete()  # 删除用户
    messages.success(request, "会员已成功删除！")  # 显示成功消息
    return redirect('manage_members')  # 重定向到管理会员页面

@user_passes_test(is_admin)  # 仅限管理员使用此功能
def manage_members(request):
    """显示所有会员的管理页面"""
    members = User.objects.all()  # 获取所有用户
    return render(request, 'admin/members/manage_members.html', {'members': members})  # 渲染模板

def make_messages_view(request):
    # 处理逻辑
    return render(request, 'template_name.html')

def add_new_member(request):  # 重命名函数以避免冲突
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin')  # 替换为你希望重定向的 URL
    else:
        form = MemberForm()
    
    return render(request, 'add_member.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)  # 或者根据你的需求定义更复杂的权限
def add_member(request):  # 如果需要保留这个功能，确保它有独特的用途
    # 您可以在这里实现添加会员的逻辑
    pass