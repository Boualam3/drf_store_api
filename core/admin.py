from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from tags.admin import TaggedItem
from store.models import Product
from .models import User
from store.admin import ProductImageInline

# lets recap : to extend user model (lock at core.models) we should extend AbstractUser
# 2- in the settings file we define AUTH_USER_MODEL = 'core.User' in our case
# we never reference User model directly we use settings.AUTH_USER_MODEL


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name")
            },
        ),
    )


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    # min_num = 1
    # max_num = 10
    # extra = 0


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline, ProductImageInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
