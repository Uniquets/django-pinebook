from django import forms
from django.contrib.auth.models import User
from users.models import City,School
from django.forms import ModelChoiceField

class loginForm(forms.Form):
    username = forms.CharField(
        required="True"
        , max_length=18
        , label='用户名'
        , widget = forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': '用户名'})
        , error_messages={
            'required': '用户名不能为空'
                                    })
    password = forms.CharField(
        required="True"
        ,max_length=18
        ,label='密码'
        ,widget = forms.PasswordInput(attrs={'class': 'form-control col-6', 'placeholder': '密码'})
        ,error_messages={

            'required': '密码不能为空'
                                    })

class registerForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        error_messages={'required': u'用户名不能为空'},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'用户名'})
    )
    password = forms.CharField(
        max_length=16,
        min_length=8,
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'密码'}),
        error_messages={'required': u'密码不能为空','min_length': u'密码长度应大于6', 'max_length': u'密码长度应小于16'}
    )

    surepassword = forms.CharField(
        max_length=18,
        min_length=8,
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'两次密码请保持一致'}),
        error_messages={'required': u'请重新输入密码','min_length':u'密码长度应大于6', 'max_length': u'密码长度应小于16'}
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'格式xxx@xxx.com'}),
        error_messages={'required': u'邮箱不能为空','invalid': u'请输入正确的邮箱'}
    )
    telephone = forms.CharField(
        max_length=11,
        label='电话号码',
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'11位电话号码'}),
        error_messages={'required': u'电话号码不能为空'}
    )
    city = forms.ModelChoiceField(
        error_messages={'required': u'请选择您所在的城市'},
        label="城市",
        queryset=City.objects.all(),
        empty_label='请选择城市',
        widget=forms.Select(attrs={'class': 'form-control'})
)
    school = forms.ModelChoiceField(
        error_messages={'required': u'请选择您所在的学校'},
        label="学校",
        queryset=School.objects.all(),
        empty_label='请选择学校',
        widget=forms.Select(attrs={'class': 'form-control'})
)


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 16:
            raise forms.ValidationError("用户名应小于16个字符")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("该用户名已被占用")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        filter_result = User.objects.filter(email__exact=email)
        if len(filter_result) > 0:
            raise forms.ValidationError("该邮箱已被占用")
        return email


    def clean_telephone(self):
        tel = self.cleaned_data.get('telephone')
        if len(tel) != 11 or not tel.isdigit():
            raise forms.ValidationError("电话号码应为十一位数字")
            return tel
        return tel

class userinfoForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        error_messages={'required': u'用户名不能为空'},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'})
    )
    telephone = forms.CharField(
        max_length=11,
        label='电话号码',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '11位电话号码'}),
        error_messages={'required': u'电话号码不能为空'}
    )
    city = forms.ModelChoiceField(
        error_messages={'required': u'请选择您所在的城市'},
        label="城市",
        queryset=City.objects.all(),
        empty_label='请选择城市',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    school = forms.ModelChoiceField(
        error_messages={'required': u'请选择您所在的学校'},
        label="学校",
        queryset=School.objects.all(),
        empty_label='请选择学校',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 16:
            raise forms.ValidationError("用户名应小于16个字符")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("该用户名已被占用")
        return username
