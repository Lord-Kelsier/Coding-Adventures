from abc import ABC, abstractmethod
'''
La usamos cuando comportamiento o caracteristica varia
dependiendo del objeto o varia en el tiempo.

los objetos son "estaticos" y su comportamiento es "dinamico"

'''
class FlyBehavior(ABC):
    
    @abstractmethod
    def Fly(self):
        pass
class FlyWithWings(FlyBehavior):
    
    def Fly(self):
        print("I'm normally flying")
class FlyNoWay(FlyBehavior):
    
    def Fly(self):
        print("I can't fly")

class QuackBehavior(ABC):
    @abstractmethod
    def Quack(self):
        pass
class Quack(QuackBehavior):
    def Quack(self):
        print("Quack")
class Squeak(QuackBehavior):
    def Quack(self):
        print("Squeak")
class MuteQuack(QuackBehavior):
    def Quack(self):
        print("I can't quack or squeak")

class Duck(ABC):
    flyBehavior = None
    quackBehavior = None
    def swim(self):
        print("Just a normal Duck swiming")

    def display(self):
        print("Hellor world, I'm a Duck")
    def quack(self):
        self.quackBehavior.Quack()
    def fly(self):
        self.flyBehavior.Fly()
        pass
class MallardDuck(Duck):
    flyBehavior = FlyWithWings()
    quackBehavior = Quack()
    
class RedHeadDuck(Duck):
    flyBehavior = FlyWithWings()
    quackBehavior = Quack()
    
class RubberDuck(Duck):
    flyBehavior = FlyNoWay()
    quackBehavior = Squeak()
    
class DecoyDuck(Duck):
    flyBehavior = FlyNoWay()
    quackBehavior = MuteQuack()
    
        
if __name__ == '__main__':
    duck = MallardDuck()
    duck.quack()
    duck.fly()
    
    duck.flyBehavior = FlyNoWay()
    duck.quack()
    duck.fly()

    duck = RedHeadDuck()
    duck.quack()
    duck.fly()
    
    duck = RubberDuck()
    duck.quack()
    duck.fly()

    duck = DecoyDuck()
    duck.quack()
    duck.fly()