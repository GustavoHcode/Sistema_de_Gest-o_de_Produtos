from infrastructure.sqlite3_sale_item_repository import SQLiteSaleItemRepository

class ListSaleItem:
    def __init__(self, repository: SQLiteSaleItemRepository):
        self.repository = repository

    def execute(self): 
        dados = self.repository.list()
        return dados

class RemoveSaleItem:
    def __init__(self, repository: SQLiteSaleItemRepository):
        self.repository = repository

    def execute(self,sale_id):
        dados = self.repository.remove(sale_id)
        return dados

class Metricas:
    def __init__(self, repository: SQLiteSaleItemRepository):
        self.repository = repository
        
    def execute(self):
        dados = self.repository.monthly_profit()
        return dados

                 
                
        