class ModelService:
    @staticmethod
    def get_queryset(model_class, **kwargs):
        return model_class.objects.filter(**kwargs)
