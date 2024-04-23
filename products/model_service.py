class ModelService:
    @staticmethod
    def get_item(model_class, **kwargs):
        return model_class.objects.get(**kwargs)
