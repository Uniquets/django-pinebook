from django import forms
from django.contrib.auth.models import User
from users.models import City,School
from django.forms import ModelChoiceField

class loginForm(forms.Form):
    username = forms.CharField(
        required="True"
        , max_length=18
        , label='用户名'
        , error_messages={
            'required': '用户名不能为空'
                                    })
    password = forms.CharField(
        required="True"
        ,max_length=18
        ,label='密码'
        ,error_messages={
            'required': '密码不能为空'
                                    })

class registerForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        error_messages={'required': u'用户名不能为空'},
    )
    password = forms.CharField(
        max_length=16,
        min_length=8,
        label='密码',
        widget=forms.PasswordInput,
        error_messages={'required': u'密码不能为空','min_length': u'密码长度应大于6', 'max_length': u'密码长度应小于16'}
    )

    surepassword = forms.CharField(
        max_length=18,
        min_length=8,
        label='确认密码',
        widget=forms.PasswordInput,
        error_messages={'required': u'请重新输入密码','min_length':u'密码长度应大于6', 'max_length': u'密码长度应小于16'}
    )
    email = forms.EmailField(
        label='邮箱',
        error_messages={'required': u'邮箱不能为空','invalid': u'请输入正确的邮箱'}
    )
    sex = forms.ChoiceField(
        label="性别",
        choices=[('男', '男'), ('女', '女')]
    )
    telephone = forms.CharField(
        max_length=11,
        label='电话号码',
        error_messages={'required': u'电话号码不能为空'}
    )
    city = forms.ModelChoiceField(
        error_messages={'required': u'请选择您所在的城市'},
        label="城市",
        queryset=City.objects.all(),
        empty_label='请选择城市',
)
    school = forms.ModelChoiceField(
        error_messages={'required': u'请选择您所在的学校'},
        label="学校",
        queryset=School.objects.all(),
        empty_label='请选择学校',
)
    grade = forms.ChoiceField(label="年级",
                              choices=[('2015', '2015'), ('2016', '2016'), ('2017', '2017'),
                                       ('2018', '2018'), ('2019', '2019'), ('0000', '已离校')])

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 6:
            raise forms.ValidationError("用户名应大于6个字符")
        elif len(username) > 16:
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
