#%%奕誠
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Member  # 确保你的 Member 模型在 models.py 中定义
from django.forms import FileInput  # 导入 FileInput

User = get_user_model()

# 注册表单
class MemberSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)  # 确保 email 字段是必填的

    class Meta:
        model = Member  # 使用自定义的 Member 模型
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# 用户资料表单
class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = Member  # 使用自定义的 Member 模型
        fields = ['username', 'email', 'avatar']  # 包含 avatar 字段，并允许用户编辑
        widgets = {
            'avatar': FileInput(),  # 使用 FileInput 而不是 ClearableFileInput，去除“清除”选项
        }
        labels = {
            'avatar': '頭像',  # 修改头像字段的标签
        }
        help_texts = {
            'avatar': '勾選以刪除當前頭像',  # 修改提示文本为繁体字
        }

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['username', 'email', 'password']  # 根据需要添加字段