from abc import ABC, abstractmethod

'''
Lo usamos cuando queremos adornar un objeto con nuevos comportamientos o caracteristicas

Los objetos son estaticos y podemos otorgarle funcionalidades en runtime
'''

# ------------------------ Objetos ------------------
class Beverage(ABC): # Component, Abstract superclass
    def get_description(self):
        return self._description
    @abstractmethod
    def cost(self):
        pass
    
class HouseBlend(Beverage): # Concrete component
    _description = "A latin american beans"
    def cost(self):
        return 1.30      
class DarkRoast(Beverage): # Concrete component
    _description = "A bitter flavor"
    def cost(self):
        return 1.20     
class Espresso(Beverage): # Concrete component
    _description = "Latin-American and Asian flavors"
    def cost(self):
        return 1.10
class Decaf(Beverage): # Concrete component
    _description = "Decafeine Coffe"
    def cost(self):
        return 1.00

# ------------------------ Decoradores  ------------------
class Decorator(Beverage): # abstract class
    beverageComponent: Beverage
    def __init__(self, beverage: Beverage) -> None:
        self.beverageComponent = beverage
        
class CondimentDecorator(Decorator): # interface
    beverageComponent: Beverage
    def __new__(cls, beverage):
        if isinstance(beverage, SizeDecorator):
            print("Can't compose over size decorator. Size decorators must compose at the end")
            return beverage        
        else:
            return super().__new__(cls)
    
    def get_description(self):
        return f"{self.beverageComponent.get_description()}, {self._description}"
    @abstractmethod
    def cost(self):
        pass
    
class Milk(CondimentDecorator): # Concrete Decorator
    _description = "With milk"
    def cost(self):
        return self.beverageComponent.cost() + 0.10
class Mocha(CondimentDecorator): # Concrete Decorator
    _description = "With Mocha"
    def cost(self):
        return self.beverageComponent.cost() + 0.20       
class Soy(CondimentDecorator): # Concrete Decorator
    _description = "With soy"
    def cost(self):
        return self.beverageComponent.cost() + 0.30       
class Whip(CondimentDecorator): # Concrete Decorator
    _description = "With whip"
    def cost(self):
        return self.beverageComponent.cost() + 0.40

class SizeDecorator(Decorator): # interface
    @abstractmethod
    def get_description(self):
        pass
    @abstractmethod
    def cost(self):
        pass
class Large(SizeDecorator):
    def get_description(self):
        return f"Large {self.beverageComponent.get_description()}"
    def cost(self):
        return self.beverageComponent.cost()*1.5
class Medium(SizeDecorator):
    def get_description(self):
        return f"Medium {self.beverageComponent.get_description()}"
    def cost(self):
        return self.beverageComponent.cost()*1.3
class Small(SizeDecorator):
    def get_description(self):
        return f"Small {self.beverageComponent.get_description()}"
    def cost(self):
        return self.beverageComponent.cost()*1.0
        
def main():
    coffe = Espresso()
    coffe = Soy(coffe)    
    coffe = Large(coffe)
    coffe = Milk(coffe) # no se incluye
    
    print(f"Cost: {round(coffe.cost(),2)}\nDescription: {coffe.get_description()}")
    
    


if __name__ == "__main__":
    main()