class Worker:

    def exec(self, *args, **kwargs):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}"
