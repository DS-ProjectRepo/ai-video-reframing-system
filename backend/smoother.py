class ExponentialSmoother:
    def __init__(self, initial_value, alpha=0.1):
        self.alpha = alpha
        self.value = initial_value

    def update(self, new_value):
        self.value = (
            self.alpha * new_value + (1 - self.alpha) * self.value
        )
        return self.value
