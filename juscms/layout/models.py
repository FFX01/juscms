from django.db import models
from django.template.defaultfilters import slugify


class AbstractLayout(models.Model):
    """
    Base Layout object model. Used for adding content to essential HTML
    template pieces such as header and footer.

    Inherits From: Django's base model class.

    Attributes:
        name(string): Display name.
        slug(string): Slug generated from 'name'. Used for reference.
        html_ids(string): HTML ID as rtendered in the html template for a
            layout object instance.
        html_class(string): HTML Class as used in the html template for this
            layout object instance.
    """
    name = models.CharField(
        verbose_name='Header Name',
        blank=False,
        max_length=120,
    )
    slug = models.SlugField(
        verbose_name='Name Slug',
        help_text='Used for calling models in templates',
        blank=True,
        max_length=150,
    )
    html_ids = models.CharField(
        verbose_name='HTML Id',
        blank=True,
        max_length=120,
    )
    html_class = models.CharField(
        verbose_name='HTML Class',
        blank=True,
        max_length=200,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Overrides default save method to check if slug exists. If it does not,
        function will generate a slug from the object instance name.
        """
        if not self.slug:
            self.slug = slugify(self.name)


class Header(AbstractLayout):
    """
    This model is used to manage the HTML header as rendered in the template.

    Attributes:
        template(string): Path to Django template file used to render this
            object instance.
    """
    template = models.CharField(
        verbose_name='Template',
        blank=False,
        null=False,
        max_length=250,
        default='header.html',
    )

    class Meta:
        verbose_name = 'Header'
        verbose_name_plural = 'Headers'

    def __str__(self):
        return self.name


class Footer(AbstractLayout):
    """
    This model is used to manage the HTML footer as rendered in the template.

    Attributes:
        template(string): Path to Django template file used to render this
            object instance.
    """
    template = models.CharField(
        verbose_name='Template',
        blank=False,
        null=False,
        max_length=250,
        default='footer.html',
    )

    class Meta:
        verbose_name = 'Footer'
        verbose_name_plural = 'Footers'

    def __str__(self):
        return self.name


class BaseLayoutColumn(models.Model):
    html_ids = models.CharField(
        verbose_name='HTML Id',
        blank=True,
        max_length=120,
    )
    html_class = models.CharField(
        verbose_name='HTML Class',
        blank=True,
        max_length=200,
    )
    content = models.TextField(
        verbose_name='Column HTML Content',
        blank=True,
    )

    class Meta:
        abstract = True


class HeaderLayoutColumn(models.Model):
    parent = models.ForeignKey(
        Header,
        verbose_name='Parent Header',
        related_name='columns',
    )

    class Meta:
        verbose_name = 'Header Layout Column'
        verbose_name_plural = 'Header Layout Columns'

    def __str__(self):
        return "ID: %d - Parent: %s" % (self.id, self.parent.name)


class FooterLayoutColumn(models.Model):
    parent = models.ForeignKey(
        Footer,
        verbose_name='Parent Footer',
        related_name='columns',
    )

    class Meta:
        verbose_name = 'Footer Layout Column'
        verbose_name_plural = 'Footer Layout Columns'

    def __str__(self):
        return "ID: %d - Parent: %s" % (self.id, self.parent.name)