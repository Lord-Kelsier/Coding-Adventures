from abc import ABC, abstractmethod
from random import randint

'''
Queremos que un comportamiento sea observado por distintas entidades
'''

# ------------------- Observadores -------------------------
class Observer(ABC):
    @abstractmethod
    def Update(self, **kwargs):
        pass
    
class WeatherDisplay1(Observer):
    def __init__(self) -> None:
        self.name = "WeatherDisplay1"
        self.temperature = None
        self.humidity = None
        self.preassure = None
    def Update(self, temp, hum, pres, **kwargs):
        self.temperature = temp
        self.humidity = hum
        self.preassure = pres
        print(self)
    def __repr__(self) -> str:
        return f"{self.name}: \n\ttemperature: {self.temperature}\n\thumidity {self.humidity}\n\tpressure: {self.preassure}"
class WeatherDisplay2(Observer):
    def __init__(self) -> None:
        self.name = "WeatherDisplay2"
        self.temperature = None
    def Update(self, temp, **kwargs):
        self.temperature = temp
        print(self)
    def __repr__(self) -> str:
        return f"{self.name}: \n\ttemperature: {self.temperature}"
class WeatherDisplay3(Observer):
    def __init__(self) -> None:
        self.name = "WeatherDisplay3"
        self.humidity = None
        self.preassure = None
    def Update(self, hum, pres, **kwargs):
        self.humidity = hum
        self.preassure = pres
        print(self)
    def __repr__(self) -> str:
        return f"{self.name}: \n\thumidity {self.humidity}\n\tpressure: {self.preassure}"

# ------------------- Observado -------------------------
class Subject(ABC):
    @abstractmethod
    def AddObserver(self, observer: Observer):
        pass
    @abstractmethod
    def RemoveObserver(self, observer: Observer):
        pass
    @abstractmethod
    def NotifyObservers(self, **kwargs):
        pass

class WeatherStation(Subject):
    def __init__(self) -> None:
        self.observers = list()
    
    def AddObserver(self, observer: Observer):
        if observer not in self.observers:
            self.observers.append(observer) 

    def RemoveObserver(self, observer: Observer):
        if observer in self.observers:
            self.observers.remove(observer)
    
    def NotifyObservers(self):
        temp = self.GetTemperature()
        hum = self.GetHumidity()
        pres = self.GetPreassure()
        for observer in self.observers:
            observer.Update(temp=temp, hum=hum, pres=pres)
            
    def GetTemperature(self):
        return randint(-273, 300)
    def GetHumidity(self):
        return randint(-273, 300)
    def GetPreassure(self):
        return randint(-273, 300)
        
if __name__ == '__main__':
    disp1 = WeatherDisplay1()
    disp2 = WeatherDisplay2()
    disp3 = WeatherDisplay3()
    
    station = WeatherStation()
    station.AddObserver(disp1)
    station.NotifyObservers()

    station.AddObserver(disp2)
    station.AddObserver(disp3)
    station.RemoveObserver(disp1)
    station.NotifyObservers()
    
    station.AddObserver(disp1)
    station.NotifyObservers()