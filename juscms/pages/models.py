from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from mptt.models import MPTTModel, TreeForeignKey


class Page(MPTTModel):
    title = models.CharField(
        verbose_name='Page Title',
        blank=False,
        null=False,
        max_length=120,
    )
    slug = models.SlugField(
        verbose_name='Page URL Slug',
        blank=True,
        max_length=200,
    )
    path = models.CharField(
        verbose_name='Page URL Path',
        blank=True,
        max_length=800,
        unique=True,
    )
    seo_title = models.CharField(
        verbose_name='Page SEO Title',
        blank=True,
        max_length=120,
    )
    seo_description = models.CharField(
        verbose_name='Page SEO Description',
        blank=True,
        max_length=255,
    )
    parent = TreeForeignKey(
        'self',
        verbose_name='Parent Page',
        blank=True,
        null=True,
        related_name='children',
        db_index=True,
    )
    template = models.CharField(
        verbose_name='Template File Path',
        blank=False,
        max_length=300,
        default='page.html',
    )
    is_home = models.BooleanField(
        verbose_name='Set this page as home page?',
        help_text="This will override the current home page.",
        default=False,
    )

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    class MPTTMeta:
        order_insertion_by = ['title']

    def build_path(self):
        path = ''
        path_list = self.get_ancestors(include_self=True)
        for item in path_list:
            path += item.slug + '/'
        return path

    def get_absolute_url(self):
        return reverse(
            'pages:base_view',
            kwargs={'path': self.path},
        )

    def save(self, *args, **kwargs):
        if not self.is_home:
            new_slug = slugify(self.title)
            if not self.slug:
                self.slug = new_slug
            elif self.slug:
                if self.slug != new_slug:
                    self.slug = new_slug
            super(Page, self).save(*args, **kwargs)
        else:
            current_home = Page.objects.filter(is_home=True)
            if current_home:
                for item in current_home:
                    item.is_home = False
                    item.save()
            super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class HTMLContent(models.Model):
    html_id = models.CharField(
        verbose_name='HTML ID',
        blank=True,
        max_length=60,
    )
    html_class = models.CharField(
        verbose_name='HTML Class',
        blank=True,
        max_length=120,
    )

    class Meta:
        abstract = True


class Row(HTMLContent):
    parent = models.ForeignKey(
        Page,
        verbose_name='Parent Page',
        related_name='rows',
        blank=False,
        null=False,
    )
    template = models.CharField(
        verbose_name='HTML Template',
        blank=False,
        null=False,
        max_length=300,
        default='pages/row.html',
    )

    class Meta:
        verbose_name = 'Row'
        verbose_name_plural = 'Rows'

    def __str__(self):
        if not self.html_id and not self.html_class:
            return "Row ID: %s" % self.id
        elif self.html_id and not self.html_class:
            return "Row - Id: %s" % self.html_id
        elif self.html_id and self.html_class:
            return "Row - Id: %s, Class: %s" % (self.html_id, self.html_class)


class Chunk(HTMLContent):
    parent = models.ForeignKey(
        Row,
        verbose_name='Parent Row',
        related_name='chunks',
        blank=False,
        null=False,
    )
    template = models.CharField(
        verbose_name='HTML Template',
        blank=False,
        null=False,
        max_length=300,
        default='pages/chunk.html',
    )
    content = models.TextField(
        verbose_name='HTML Content',
        blank=True,
    )

    class Meta:
        verbose_name = 'Chunk'
        verbose_name_plural = 'Chunks'

    def __str__(self):
        if not self.html_id and not self.html_class:
            return "Row ID: %s" % self.id
        elif self.html_id and not self.html_class:
            return "Row - Id: %s" % self.html_id
        elif self.html_id and self.html_class:
            return "Row - Id: %s, Class: %s" % (self.html_id, self.html_class)


@receiver(post_save, sender=Page)
def update_path(sender, instance, **kwargs):
    if not instance.is_home:
        if not instance.path:
            instance.path = instance.build_path()
            instance.save()
        elif instance.path:
            new_path = instance.build_path()
            if instance.path != new_path:
                instance.path = new_path
                instance.save()
            else:
                pass
    else:
        instance.path = ''
        instance.save()