


class {{ cookiecutter.node_cls }}Algro:
    model_cls = None

    def __init__(self, model_fp):
        self.mdoel = self.init_model(model_fp)
    
    def init_model(self, model_fp):
        return self.model_cls(model_fp)

    def predict(self, raw):
        return {
            'labels': ['person', 'dog'],
            'class_ids': [0, 1],
            'scores': [0.9, 0.8],
            'boxes': [[120, 120, 120, 120], [130, 130, 130, 130]]
        }