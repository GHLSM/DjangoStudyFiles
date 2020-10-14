from django import forms
from app01 import models


class MyRegForm(forms.Form):
    username = forms.CharField(label='用户名',
                               min_length=3,
                               max_length=8,
                               error_messages={
                                   'required': '用户名不为空',
                                   'min_length': '用户名至少为三位',
                                   'max_length': '用户名最大八位',
                               },
                               widget=forms.widgets.TextInput(attrs={'class': 'form-control'})
                               )

    password = forms.CharField(label='密码',
                               min_length=6,
                               max_length=16,
                               error_messages={
                                   'required': '密码不为空',
                                   'min_length': '密码至少为六位',
                                   'max_length': '密码最大十六位',
                               },
                               widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
                               )

    confirm_pwd = forms.CharField(label='确认密码',
                                  min_length=6,
                                  max_length=16,
                                  error_messages={
                                   'required': '密码不为空',
                                   'min_length': '密码至少为六位',
                                   'max_length': '密码最大十六位',
                                  },
                                  widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
                                  )

    email = forms.EmailField(label='邮箱',
                             error_messages={
                                 'required': '邮箱不为空',
                                 'invalid': '邮箱格式不正确',
                             },
                             widget=forms.widgets.EmailInput(attrs={'class': 'form-control'})
                             )

    # 钩子函数
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # 数据库中校验
        is_exist = models.UserInfo.objects.filter(username=username)
        if is_exist:
            self.add_error('username', '用户名已存在')
        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_pwd = self.cleaned_data.get('confirm_pwd')
        if not password == confirm_pwd:
            self.add_error('confirm_pwd', '两次输入密码不一致')
        return self.cleaned_data
