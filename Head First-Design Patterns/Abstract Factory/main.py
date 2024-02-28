from abc import ABC, abstractmethod

'''
Encapsula la creacion de familias de objetos.
La delegamos a fabricas concretas de familias de objetos, 
cada una de estas fabricas es posee uno o varios factory methods
'''

# --------------------------- abstract Sofa ----------------------
class Sofa(ABC):
    @abstractmethod
    def cleanSofa(self): pass
# --------------------------- abstract Table ----------------------
class Table(ABC):
    @abstractmethod
    def cleanTable(self): pass
# --------------------------- abstract Factory ----------------------
class FurnitureFactory(ABC):
    sofa: Sofa
    table: Table
    @abstractmethod
    def createSofa(self): pass
    
    @abstractmethod
    def createTable(self): pass

    def cleanFurniture(self):
        self.sofa.cleanSofa()
        self.table.cleanTable()
    
# --------------------------- Concrete Sofa ----------------------
class ModernSofa(Sofa):
    def cleanSofa(self):
        print("Cleaning a Modern Sofa")

class VictorianSofa(Sofa):
    def cleanSofa(self):
        print("Cleaning a Victorian Sofa")
# --------------------------- Concrete Table ----------------------
class ModernTable(Table):
    def cleanTable(self):
        print("Cleaning a Modern table")

class VictorianTable(Table):
    def cleanTable(self):
        print("Cleaning a Victorian table")
# --------------------------- Concrete Factory ----------------------
class ModernFurnitureFactory(FurnitureFactory): 
    def createSofa(self):
        self.sofa = ModernSofa()
    def createTable(self):
        self.table = ModernTable()

class VictorianFurnitureFactory(FurnitureFactory):
    def createSofa(self):
        self.sofa = VictorianSofa()
    def createTable(self):
        self.table = VictorianTable()
# ---------------------------------------------------------------

if __name__ == '__main__':
    furnitureFactory = ModernFurnitureFactory()
    furnitureFactory.createSofa()
    furnitureFactory.createTable()
    furnitureFactory.cleanFurniture()

    furnitureFactory = VictorianFurnitureFactory()
    furnitureFactory.createSofa()
    furnitureFactory.createTable()
    furnitureFactory.cleanFurniture()
    