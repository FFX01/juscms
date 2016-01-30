from django.core.exceptions import ValidationError


class SingleInstanceMixin(object):
    # TODO fix this method so creating a new header does not throw error
    """
    Mixin class to ensure only one instance of a particular model can be
    created.
    """
    def clean(self):
        """
        Extends a model's clean method to check if there are already any
        instances of the model. If another model instance of the same type
        exists, this method will throw a validation error.
        """
        model = self.__class__
        if model.objects.count() > 0:
            if self.id:
                if self.id != model.objects.get()[:1].id:
                    raise ValidationError('Can only create one %s' % model.__name__)
            else:
                raise ValidationError('Can only create one %s' % model.__name__)
        super(SingleInstanceMixin, self).clean()


class SingleInstanceAdminMixin(object):
    """
    Mixin class for registering models in the Django admin. Hides the 'add'
    button if there is already an instance of the model.
    """
    def has_add_permission(self, request):
        """
        Checks if a model instance has already been created. If it has, it
        removes add permissions so a user cannot add a new new instance.
        """
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        return super(SingleInstanceAdminMixin, self).has_add_permission(request)
