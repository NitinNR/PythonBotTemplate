class MyClass:
    class_variable = 10

    def __init__(self, instance_variable):
        self.instance_variable = instance_variable

    # @classmethod
    def class_method(cls):
        print("This is a class method.")
        print(f"Accessing class variable: {cls.class_variable} {cls.instance_variable}")

    @staticmethod
    def static_method():
        print("This is a static method.")

    def instance_method(self):
        print("This is an instance method.")
        print(f"Accessing instance variable: {self.instance_variable}")


# Create an instance of MyClass
my_instance = MyClass(42)

my_instance.class_method()

