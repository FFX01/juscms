from django.contrib import admin

import nested_admin

from .models import Page, Row, Chunk


class ChunkInline(nested_admin.NestedStackedInline):
    """
    Class for registering Inline functionality for Chunk model. This allows
    users to add chunks to pages inside the page admin interface.

    Inherits From:
        NestedStackedInline(model): This model comes from the
            django-nested-admin package. This allows the nesting of model forms
            inside the django admin interface.

    Attributes:
        model(object): The model that this class applies to. This model will
            have it's model form rendered on the django admin page edit form.
    """
    model = Chunk


class RowInline(nested_admin.NestedStackedInline):
    """
    Same as ChunkInline class except it is used to register the Row model.

    Attributes:
        model(object): The model that will have it's model form rendered in the
            page edit admin interface.
        inlines(object): The model form class that will be rendered as an
            inline of this model object's model form.
    """
    model = Row
    inlines = [
        ChunkInline,
    ]


@admin.register(Page)
class PageAdmin(nested_admin.NestedAdmin):
    """
    Class that registers the Page model in the django admin interface.

    Attributes:
        prepopulated_fields(dictionary): Specifies any fields that will be
            populated automatically by referencing other model form fields.
            In this case we are populating the slug field with the slug version
            of the page title field.
        readonly_fields(tuple): Fields that are read-only. These fields are
            cannot be modified by the user but are important for the user to
            see. In this case this is the automatically generated page path.
            It is important that the user cannot modify this field as it is
            the primary query argument for retrieving the page instance in the
            base view class get function.
        inlines(list): Model forms that will be rendered as part of the page
            model form in the django admin interface.
    """
    prepopulated_fields = {
        'slug': ('title',),
    }
    readonly_fields = (
        'path',
    )
    inlines = [
        RowInline,
    ]
