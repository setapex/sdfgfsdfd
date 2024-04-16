class ModelService:
    def get_item(self, model_class, **kwargs):
        return model_class.objects.get(**kwargs)

    def create_item(self, model_class, **kwargs):
        return model_class.objects.create(**kwargs)

    def update_item(self, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()

    def delete_item(self, instance):
        instance.delete()

    def get_queryset(self, model_class, **kwargs):
        return model_class.objects.filter(**kwargs)

    def delete_queryset(self, model_class, **kwargs):
        model_class.objects.filter(**kwargs).delete()
