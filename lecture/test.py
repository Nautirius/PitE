def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class MyClass:
    def __init__(self, value):
        self.value = value


a = MyClass(10)
b = MyClass(20)

print(a is b)
