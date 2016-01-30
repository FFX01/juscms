from django.contrib import admin

from jusutils.mixins import SingleInstanceAdminMixin

from .models import Header, Footer


@admin.register(Header)
class HeaderAdmin(SingleInstanceAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(Footer)
class FooterAdmin(SingleInstanceAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',),
    }
