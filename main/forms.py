# coding: utf-8
from main.models import Item
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext
from django.contrib.auth import authenticate

class ItemForm(ModelForm):
	
	class Meta:
 		model = Item
		exclude = ['user', 'categories']


class Html5Mixin(object):
    """
    Mixin for form classes. Adds HTML5 features to forms for client
    side validation by the browser, like a "required" attribute and
    "email" and "url" input types.
    """

    def __init__(self, *args, **kwargs):
        super(Html5Mixin, self).__init__(*args, **kwargs)
        if hasattr(self, "fields"):
            # Autofocus first field
            first_field = next(iter(self.fields.values()))
            first_field.widget.attrs["autofocus"] = ""

            for name, field in self.fields.items():
                if settings.FORMS_USE_HTML5:
                    if isinstance(field, forms.EmailField):
                        self.fields[name].widget.input_type = "email"
                    elif isinstance(field, forms.URLField):
                        self.fields[name].widget.input_type = "url"
                if field.required:
                    self.fields[name].widget.attrs["required"] = ""

class LoginForm(Html5Mixin, forms.Form):
    """
    Fields for login.
    """
    username = forms.CharField(label=u"Մուտք")
    password = forms.CharField(label=u"Ծածկագիր",
                               widget=forms.PasswordInput(render_value=False))

    def clean(self):
        """
        Authenticate the given username/email and password. If the fields
        are valid, store the authenticated user for returning via save().
        """
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        self._user = authenticate(username=username, password=password)
        if self._user is None:
            raise forms.ValidationError(
                             ugettext("Invalid username/email and password"))
        elif not self._user.is_active:
            raise forms.ValidationError(ugettext("Your account is inactive"))
        return self.cleaned_data

    def save(self):
        """
        Just return the authenticated user - used for logging in.
        """
        return getattr(self, "_user", None)

class ProfileForm(Html5Mixin, forms.ModelForm):
    """
    ModelForm for auth.User - used for signup and profile update.
    If a Profile model is defined via ``AUTH_PROFILE_MODULE``, its
    fields are injected into the form.
    """

    password = forms.CharField(label="Password",
                                widget=forms.PasswordInput(render_value=False))
    mobile = forms.CharField(label=u"Հեռ. համար", required=False)
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "mobile")
        

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self._signup = self.instance.id is None
        user_fields = User._meta.get_all_field_names()
        try:
            self.fields["username"].help_text = ugettext(
                        "Only letters, numbers, dashes or underscores please")
        except KeyError:
            pass
        for field in self.fields:
            # Make user fields required.
            if field in user_fields:
                self.fields[field].required = True
            # Disable auto-complete for password fields.
            # Password isn't required for profile update.
            if field.startswith("password"):
                self.fields[field].widget.attrs["autocomplete"] = "off"
                self.fields[field].widget.attrs.pop("required", "")
                if not self._signup:
                    self.fields[field].required = False
                    if field == "password1":
                        self.fields[field].help_text = ugettext(
                        "Leave blank unless you want to change your password")
        

    def clean_username(self):
        """
        Ensure the username doesn't exist or contain invalid chars.
        We limit it to slugifiable chars since it's used as the slug
        for the user's profile view.
        """
        username = self.cleaned_data.get("username")
        
        lookup = {"username__iexact": username}
        try:
            User.objects.exclude(id=self.instance.id).get(**lookup)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
                            ugettext("This username is already registered"))

    def clean_password2(self):
        """
        Ensure the password fields are equal, and match the minimum
        length defined by ``ACCOUNTS_MIN_PASSWORD_LENGTH``.
        """
        password = self.cleaned_data.get("password")

        if password:
            errors = []
            if len(password) < settings.ACCOUNTS_MIN_PASSWORD_LENGTH:
                errors.append(
                        ugettext("Password must be at least %s characters") %
                        settings.ACCOUNTS_MIN_PASSWORD_LENGTH)
            if errors:
                self._errors["password"] = self.error_class(errors)
        return password

    def clean_email(self):
        """
        Ensure the email address is not already registered.
        """
        email = self.cleaned_data.get("email")
        qs = User.objects.exclude(id=self.instance.id).filter(email=email)
        if len(qs) == 0:
            return email
        raise forms.ValidationError(
                                ugettext("This email is already registered"))

    def save(self, *args, **kwargs):
        """
        Create the new user. If no username is supplied (may be hidden
        via ``ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS`` or
        ``ACCOUNTS_NO_USERNAME``), we generate a unique username, so
        that if profile pages are enabled, we still have something to
        use as the profile's slug.
        """

        kwargs["commit"] = False
        user = super(ProfileForm, self).save(*args, **kwargs)
        try:
            username = self.cleaned_data["username"]
        except KeyError:
            if not self.instance.username:
                username = self.cleaned_data["email"].split("@")[0]
                qs = User.objects.exclude(id=self.instance.id)
                user.username = unique_slug(qs, "username", slugify(username))
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        elif self._signup:
            try:
                user.set_unusable_password()
            except AttributeError:
                # This could happen if using a custom user model that
                # doesn't inherit from Django's AbstractBaseUser.
                pass
        user.save()

        
        if self._signup:
            if (settings.ACCOUNTS_VERIFICATION_REQUIRED or
                settings.ACCOUNTS_APPROVAL_REQUIRED):
                user.is_active = False
                user.save()
            else:
                
                user = authenticate(username=username, password=password)
        return user

    def get_profile_fields_form(self):
        return ProfileFieldsForm