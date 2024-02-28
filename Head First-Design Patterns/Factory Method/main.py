from abc import ABC, abstractmethod

'''
Encapsula la creacion de objetos.
La delegamos a fabricas concretas, sin embargo, estos objetos 
deben tener una interfaz comun.
'''

# ---------------------- Productos  ---------------
class Pizza(ABC):
    def GetName(self):
        return self.__class__.__name__
    
class NyCheesePizza(Pizza): pass
class NyPepperoniPizza(Pizza): pass
class ChicagoPepperoniPizza(Pizza): pass
class ChicagoCheesePizza(Pizza): pass

# ---------------------- Fabricas ---------------
class PizzaStore(ABC):
    pizza: Pizza
    @abstractmethod
    def createPizza(self, pType)->Pizza: pass  # <----- Factory Method
    
    def orderPizza(self, pType):
        self.pizza = self.createPizza(pType)
        print(f"You order a/an: {self.pizza.GetName()}")

class NYPizzaStore(PizzaStore):
    def createPizza(self, pType) -> Pizza:
        if pType == "Cheese":
            return NyCheesePizza()
        elif pType == "Pepperoni":
            return NyPepperoniPizza()
class ChicagoPizzaStore(PizzaStore):
    def createPizza(self, pType) -> Pizza:
        if pType == "Cheese":
            return ChicagoCheesePizza()
        elif pType == "Pepperoni":
            return ChicagoPepperoniPizza()
        
if __name__ == "__main__":
    nyc = NYPizzaStore()
    chic = ChicagoPizzaStore()
    nyc.orderPizza("Cheese")
    chic.orderPizza("Pepperoni")
        