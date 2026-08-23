class Human:
    # pass
    faults = 0
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def speak(self):
        print(f"Hi {self.name} Are you {self.age} years old?")
    @classmethod
    def makeFaults(cls):
        cls.faults +=1
        print(cls.faults)
    @staticmethod
    def measureTemp(temp):
        return "Normal" if (temp == 37) else "Not Normal"
class Mammal:
    def __init__(self, type_at):
        self.type_at = type_at
        print("Mammal __init__ is running")
        
class Employee(Human,Mammal):
    def __init__(self, name, age, salray, type_at):
        # Human.__init__(self, name, age)
        # super(Employee, self).__init__(name, age)
        super().__init__(name, age, type_at)
        self.salray = salray
    def work(self):
        print("I`m working now")


# man = Human("Amr", 20)
# man2 = Human("Ahmed", 20)
# print(man.name, man.age)
# man.faults = 1
# print("Man : ", man.faults)
# print("Man 2: ", man2.faults)
# print("Human : ", Human.faults)
# Human.faults = 1
# print("Man : ", man.faults)
# print("Man 2: ", man2.faults)
# print("Human : ", Human.faults)

# print(man.speak()) # => None
# man2.speak()

# Human.makeFaults() # => 1
# man3 = Human("Mohammed", 22)
# man3.makeFaults() # => 2
# Human.makeFaults() # => 3

# print(Human.measureTemp(45)) # => Not Normal

emp = Employee("Ahmed", 22, 500)
emp.speak()
emp.work()
