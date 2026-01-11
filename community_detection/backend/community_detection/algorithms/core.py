from .evaluator import Evaluator


class InstanceCore:
    evaluations_per_snapshot = {}  # Atributo de clase compartido por todas las subclases

    def __init__(self):
        self.evaluator = Evaluator()
    
