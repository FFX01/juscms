from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from mptt.models import MPTTModel, TreeForeignKey


class Page(MPTTModel):
    """
    This is the basic page model. All user defined page models inherit from
    this model.

    Inherits From:
        MPTTModel: This model is from the django-mptt package. This is what
            allows Pages to be nested. This model uses Multi Preorder Tree
            Traversal to build a reference tree for objects.

    Attributes:
        title(string): The page title. Used mainly for reference in the admin
            interface.
        slug(string): The URL slug version of the page name. This is used to
            construct a URL path. The URL path is what is used to route the
            main view to the correct object instance.
        path(string): This is the 'Page' instance's URL path. This is generated
            when saving the model for the first time and regenerated when the
            'Page' instance's parent is changed.
        seo_title(string): This is the Page instance title as it appears in the
            HTML document. It appears between the '<title></title>' tags in the
            base template.
        seo_description(string): This is the Page instance meta description as
            it appears in the HTML document. It appears in the
            '<meta name="description">' tag.
        parent(object): The Page instance parent Page instance. Pages can be
            nested under other pages.
        template(string): The path to the Django HTML template file. If a user
            wants to change the layout of a page, they can either edit the
            default file directly or define their own.
        is_home(boolean): If set to true the page instance will be set as the
            home page, the path attribute will be set to a blank string, and
            the parent attribute will be set to None. Any other page that has
            this attribute set to True will have is_home set to False.
        style(string): This field is for adding additional custom CSS styling
            to a specific page instance. This CSS will then be dynamically
            inserted into the head element in 'base.html'. This ensures that
            page specific styles are not applied to the entire site.
    """
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
    style = models.TextField(
        verbose_name='Page Specific CSS',
        blank=True,
    )

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    class MPTTMeta:
        order_insertion_by = ['title']

    def build_path(self):
        """
        This method builds a string containing the Page instance URL path.

        Variables:
            path(string): Initialized as an empty string. Will be populated
                with a string containing the Page instance URL path.
            path_list(list): A list of this Page instance ancestors including
                this Page instance itself.

        Returns:
            path(string): The formatted URL path of this Page instance.
        """
        path = ''
        path_list = self.get_ancestors(include_self=True)
        for item in path_list:
            path += item.slug + '/'
        return path

    def get_absolute_url(self):
        """
        Generates the absolute URL of the Page instance. This is used in the
        admin to enable the 'View on site' button.
        """
        return reverse(
            'pages:base_view',
            kwargs={'path': self.path},
        )

    def save(self, *args, **kwargs):
        """
        This method overrides the default Django model save method in order
        to conditionally modify the Page instance attributes. It generates the
        Page instance slug and checks to see if the Page instance has it's
        is_home attribute set to True. If so, it sets the Page instance
        path attribute to an empty string, and the parent attribute to None. It
        also checks if the slug attribute has changed and updates it accordingly.
        """
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
                    if item != self:
                        item.is_home = False
                        item.save()
                self.path = ''
                self.parent = None
                super(Page, self).save(*args, **kwargs)
            else:
                self.path = ''
                self.parent = None
                super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class HTMLContent(models.Model):
    """
    This is the base abstract model for HTML content objects. All HTML content
    objects inherit from this class.

    Attributes:
        html_ids(string): This is the HTML id that will be applied to the HTML
            tag in the DOM. Used for styling.
        html_class(string): Same as the html_ids attribute except it populates
            the HTML class attribute. Used for styling.
    """
    html_ids = models.CharField(
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
    """
    Model used for generating HTML row objects.

    Attributes:
        parent(object): The parent page of this row. This is a one to many
            relationship. A page instance can have multiple row instances as
            children.
        template(string): Path to the template file used to render this model
            instance.
    """
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
        if not self.html_ids and not self.html_class:
            return "Row ID: %s" % self.id
        elif self.html_ids and not self.html_class:
            return "Row - Id: %s" % self.html_ids
        elif self.html_class and not self.html_ids:
            return "Row - Class: %s" % self.html_class
        elif self.html_ids and self.html_class:
            return "Row - Id: %s, Class: %s" % (self.html_ids, self.html_class)


class Chunk(HTMLContent):
    """
    Model used for generating HTML chunk objects.

    Attributes:
        parent(object): The parent Row for this Chunk instance. All chunks
            MUST have a parent Row.
        template(string): The path to the HTML template used to render the
            chunk instance.
        content(test/HTML): The user entered HTML content inside of this chunk.
            Will be rendered as part of the DOM.
    """
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
        if not self.html_ids and not self.html_class:
            return "Chunk ID: %s" % self.id
        elif self.html_ids and not self.html_class:
            return "Chunk - Id: %s" % self.html_ids
        elif self.html_class and not self.html_ids:
            return "Row - Class: %s" % self.html_class
        elif self.html_ids and self.html_class:
            return "Chunk - Id: %s, Class: %s" % (self.html_ids, self.html_class)


@receiver(post_save, sender=Page)
def update_path(sender, instance, **kwargs):
    """
    This function listens to the save signal sent by a Page instance after it
    has been created or modified and performs some logic to make sure that it
    is callable by the view and sits correctly into the page tree.
    """
    if instance.is_home is False:
        if not instance.path:
            if instance.parent:
                instance.move_to(instance.parent)
            instance.path = instance.build_path()
            instance.save()
        elif instance.path:
            new_path = instance.build_path()
            if instance.path != new_path:
                instance.path = new_path
                instance.save()
            else:
                pass
