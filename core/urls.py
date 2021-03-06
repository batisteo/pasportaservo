from django.conf.urls import include, url
from django.contrib.auth.views import (
    LogoutView, PasswordResetCompleteView, PasswordResetConfirmView,
    PasswordResetDoneView, PasswordResetView,
)
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from .forms import SystemPasswordResetForm, SystemPasswordResetRequestForm
from .views import (
    AgreementRejectView, AgreementView, EmailUpdateView,
    EmailVerifyView, HomeView, LoginView, MassMailSentView,
    MassMailView, PasswordChangeDoneView,
    PasswordChangeView, RegisterView, UsernameChangeView,
)

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),

    url(_(r'^register/$'), RegisterView.as_view(), name='register'),
    url(_(r'^login/$'), view=LoginView.as_view(), name='login'),
    url(_(r'^logout/$'), view=LogoutView.as_view(next_page='/'), name='logout'),

    url(_(r'^agreement/'), include([
        url(r'^$', view=AgreementView.as_view(), name='agreement'),
        url(_(r'^reject/$'), view=AgreementRejectView.as_view(), name='agreement_reject'),
    ])),

    url(_(r'^password/'), include([
        url(r'^$', view=PasswordChangeView.as_view(), name='password_change'),
        url(_(r'^done/$'), view=PasswordChangeDoneView.as_view(), name='password_change_done'),
        url(_(r'^reset/'), include([
            url(r'^$',
                view=PasswordResetView.as_view(
                    form_class=SystemPasswordResetRequestForm,
                    html_email_template_name='email/password_reset.html',
                    email_template_name='email/password_reset.txt',
                    subject_template_name='email/password_reset_subject.txt',
                ),
                name='password_reset'),
            url(_(r'^sent/$'), view=PasswordResetDoneView.as_view(), name='password_reset_done'),
            url(r'^(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                view=PasswordResetConfirmView.as_view(
                    form_class=SystemPasswordResetForm,
                ),
                name='password_reset_confirm'),
            url(_(r'^done/$'), view=PasswordResetCompleteView.as_view(), name='password_reset_complete'),
        ])),
    ])),
    url(_(r'^username/$'), UsernameChangeView.as_view(), name='username_change'),
    url(_(r'^email/'), include([
        url(r'^$', EmailUpdateView.as_view(), name='email_update'),
        url(_(r'^verify/$'), EmailVerifyView.as_view(), name='email_verify'),
    ])),

    url(_(r'^admin/'), include([
        url(_(r'^mass-mail/'), include([
            url(r'^$', MassMailView.as_view(), name='mass_mail'),
            url(_(r'^sent/$'), MassMailSentView.as_view(), name='mass_mail_sent'),
        ])),
    ])),

    url(_(r'^ok$'), TemplateView.as_view(template_name='200.html')),
]
