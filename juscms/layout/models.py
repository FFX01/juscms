from django.db import models
from django.template.defaultfilters import slugify


class AbstractLayout(models.Model):
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
    element_left = models.TextField(
        verbose_name='Header Left',
        blank=True,
    )
    element_center = models.TextField(
        verbose_name='Header Center',
        blank=True,
    )
    element_right = models.TextField(
        verbose_name='Header Right',
        blank=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)


class Header(AbstractLayout):
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
