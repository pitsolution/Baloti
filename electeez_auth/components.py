from django.urls import include, path, reverse
from django_registration.forms import RegistrationForm
from ryzom.components import components as html
from ryzom.py2js.decorator import JavaScript
from .models import User
from electeez.mdc import (
    MDCButton,
    MDCButtonOutlined,
    MDCTextButton,
    MDCFormField,
    MDCTextFieldFilled,
    MDCTextFieldOutlined,
    CSRFInput,
)


class RegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User


class OAuthConnect(html.Div):
    def __init__(self, view):
        self.google_btn = MDCButtonOutlined('continue with google')
        self.facebook_btn = MDCButton('continue with facebook', p=False)
        self.apple_btn = MDCButton('continue with apple')

        super().__init__(
            self.google_btn,
            self.facebook_btn,
            self.apple_btn,
            cls='card',
            style='display: flex; flex-flow: column wrap;'
        )


class EmailLoginCard(html.Div):
    def __init__(self, view, ctx):
        self.email_field = MDCTextFieldOutlined(
            'Email',
            'email_input',
            'email_input_label',
            name='email'
        )

        self.password_field = MDCTextFieldOutlined(
            'Password',
            'password_input',
            'password_input_label',
            type='password',
            name='password'
        )
        self.forgot_pass = MDCTextButton('forgot password?')
        self.login = MDCButton('continue')
        self.form = html.Form(
            CSRFInput(view),
            self.email_field,
            self.password_field,
            html.Div(
                self.forgot_pass,
                self.login,
                style='display: flex; justify-content: space-between;'
            ),
            method='POST',
            style='display: flex; flex-flow: column wrap; '
        )
        super().__init__(
            html.Div(
                html.H4('Welcome to Electeez', style='text-align: center;'),
                OAuthConnect(view),
                html.Span('Or enter email and password:', cls='center-text'),
                self.form,
                cls='card'
            )
        )

    def click_events():
        def handle_forgot(event):
            route('/accounts/password_reset/')

        def handle_login(event):
            getElementByUuid(form_id).submit()

        getElementByUuid(login_id).addEventListener('click', handle_login)
        getElementByUuid(forgot_id).addEventListener('click', handle_forgot)

    def render_js(self):
        return JavaScript(self.click_events, {
            'forgot_id': self.forgot_pass._id,
            'login_id': self.login._id,
            'form_id': self.form._id
        })


class LogoutCard(html.Div):
    def __init__(self, view, ctx):
        self.login_btn = MDCButton('Login again')
        super().__init__(
            html.H4('You have been logged out'),
            html.Div(
                'Thank you for spending time on our site today.',
                cls='section'),
            html.Div(
                self.login_btn,
                style='display:flex; justify-content: flex-end;'),
            cls='card',
            style='text-align: center'
        )

    def click_events():
        def handle_login(event):
            route('/accounts/login/')

        getElementByUuid(login_id).addEventListener('click', handle_login)

    def render_js(self):
        return JavaScript(self.click_events, {
            'login_id': self.login_btn._id,
        })


class PasswordResetCard(html.Div):
    def __init__(self, view, ctx):
        self.email_field = MDCTextFieldOutlined(
            'Email',
            'email_input',
            'email_input_label',
            name='email'
        )
        self.form = html.Form(
            CSRFInput(view),
            self.email_field,
            method='POST',
            style='display: flex; flex-flow: column wrap; '
        )
        self.submit = MDCButton('reset password')

        super().__init__(
            html.Div(
                html.H4('Reset your password', style='text-align: center;'),
                html.Div(
                    self.form,
                ),
                html.Div(
                    self.submit,
                    style='display: flex; justify-content: flex-end;'
                ),
                cls='card'
            )
        )

    def render_js(self):
        def reset_pass():
            def handle_reset(evemt):
                getElementByUuid(form_id).submit()

            getElementByUuid(submit_id).addEventListener('click', handle_reset)

        return JavaScript(reset_pass, dict(
            submit_id=self.submit._id,
            form_id=self.form._id
        ))


class PasswordResetDoneCard(html.Div):
    def __init__(self, view, ctx):
        super().__init__(
            html.H4('A link has been sent to your email address'),
            html.A('Go to login page', href=reverse('login'))
        )


class EmailRegistrationCard(html.Div):
    form_class = RegistrationForm

    def __init__(self, view, ctx):
        form = ctx.get('form', None) if ctx else None
        self.email_field = MDCTextFieldOutlined(
            'Email',
            'email_input',
            'email_input_label',
            type='email',
            name='email',
            required=True
        )
        self.password1_field = MDCTextFieldOutlined(
            'Password',
            'password_input',
            'password_input_label',
            type='password',
            name='password1',
            required=True,
            minlength=8
        )
        self.password2_field = MDCTextFieldOutlined(
            'Repeat password',
            'password2_input',
            'password2_input_label',
            type='password',
            name='password2',
            required=True,
            minlength=8
        )
        self.form = html.Form(
            CSRFInput(view),
            self.email_field,
            self.password1_field,
            html.Span('Your password has to match the following criteria:', style='font-weight: bold;'),
            html.Ul(
                html.Li('Contains at least 8 characters'),
                html.Li('Not too similar to your other personal informations'),
                html.Li('Not entirely numeric'),
                html.Li('Not a commonly used password'),
            ),
            self.password2_field,
            method='POST',
            style='display: flex; flex-flow: column wrap; '
        )
        self.signup = MDCButton('Sign up')

        if form:
            for k in form.errors.keys():
                if attr := getattr(self, k + '_field', None):
                    for e in form.errors[k]:
                        attr.set_error(e)

        super().__init__(
            html.Div(
                html.H4('Looks like you need to register', style='text-align: center;'),
                self.form,
                html.Div(
                    self.signup,
                    style='display: flex; justify-content: flex-end;'
                ),
                html.Span('Or use:', cls='center-text'),
                OAuthConnect(view),
                cls='card'
            )
        )

    def render_js(self):
        def reset_pass():
            def handle_reset(evemt):
                getElementByUuid(form_id).submit()

            getElementByUuid(submit_id).addEventListener('click', handle_reset)

        return JavaScript(reset_pass, dict(
            submit_id=self.signup._id,
            form_id=self.form._id
        ))


class RegistrationCompleteCard(html.Div):
    def __init__(self, view, ctx):
        super().__init__(
            html.H4('Check your emails to finish !'),
            html.Div(
                'An activation link has been sent to your email address, ' +
                'please open it to finish the signup process.',
                style='margin-bottom: 24px'
            ),
            html.Div(
                'Then, come back and login to participate to your election.',
                style='margin-bottom: 24px;'
            ),
            cls='card',
            style='text-align: center'
        )



