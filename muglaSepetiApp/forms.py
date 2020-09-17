
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from muglaSepetiApp.models import Profile, Address


class InputForm(forms.Form):

    def __init__(self, request=None, *args, **kwargs):
        super(InputForm, self).__init__(request, *args, **kwargs)
        for key in self.fields:
            if self.fields[key].widget.input_type != "checkbox":
                self.fields[key].widget.attrs.update({'class': 'form-control', 'placeholder': self.fields[key].label})
            else:
                self.fields[key].widget.attrs.update({'class': 'radio-inline', 'placeholder': self.fields[key].label})


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(label=_('Beni hatırla'), initial=False,
                                     required=False)

    def __init__(self, request=None, *args, **kwargs):
        self.user_cache = None
        super(LoginForm, self).__init__(request, *args, **kwargs)
        self.fields['username'].icon = "icofont-ui-message"
        self.fields['username'].class_val = "form-control"
        self.fields['password'].icon = "icofont-lock"
        self.fields['password'].class_val = "form-control"
        self.fields['remember_me'].class_val = "radio-inline"


class RegisterForm(UserCreationForm, InputForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    aggree_terms = forms.BooleanField(label=_('Kayıt koşullarını kabul ediyorum'), required=True,
                                      help_text=_('Kayıt olabilmek için koşullarımızı kabul etmelisiniz.'))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def __init__(self, request=None, *args, **kwargs):
        super(RegisterForm, self).__init__(request, *args, **kwargs)
        # for field_name in self.fields:
        #     self.fields[field_name].class_val = "form-control"
        # self.fields['aggree_terms'].class_val = "radio-inline"

        self.fields['username'].icon = "icofont-ui-user"
        # self.fields['first_name'].icon = "icofont-ui-message"
        # self.fields['last_name'].icon = "icofont-ui-message"
        self.fields['email'].icon = "icofont-ui-email"
        self.fields['password1'].icon = "icofont-ui-lock"
        self.fields['password2'].icon = "icofont-ui-lock"
        self.fields['aggree_terms'].error_messages = {'required': self.fields['aggree_terms'].help_text}


class ChangeUserForm(forms.ModelForm, InputForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class CreateAddressForm(forms.ModelForm, InputForm):
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ('owner',)


class ChangeProfileForm(forms.ModelForm, InputForm):
    # address = forms.ModelChoiceField(queryset=Address.objects.all(),
    #                                  to_field_name='name',
    #                                  empty_label="Select Address")

    class Meta:
        model = Profile
        fields = ('address', 'birth_date', 'phone')
        # fields = '__all__'

    def __init__(self, request=None, *args, **kwargs):
        super(ChangeProfileForm, self).__init__(request, *args, **kwargs)
        self.fields['birth_date'].widget.input_type = 'date'
        self.fields['birth_date'].widget.format = '%Y-%m-%d'
        self.fields['address'].queryset = Address.objects.filter(owner=self.instance.user.id)
        self.fields['address'].empty_label = _("Şuanki Adresinizi Seçiniz")


class ChangePasswordForm(PasswordChangeForm, InputForm):
    pass
