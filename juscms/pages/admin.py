from django.contrib import admin

import nested_admin

from .models import Page, Row, Chunk


class ChunkInline(nested_admin.NestedStackedInline):
    model = Chunk


class RowInline(nested_admin.NestedStackedInline):
    model = Row
    inlines = [
        ChunkInline,
    ]


@admin.register(Page)
class PageAdmin(nested_admin.NestedAdmin):
    prepopulated_fields = {
        'slug': ('title',),
    }
    readonly_fields = (
        'path',
    )
    inlines = [
        RowInline,
    ]
