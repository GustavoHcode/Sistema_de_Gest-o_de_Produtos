from core.domain.sale.sale_interface import InterfaceSale

class CreateSale:
    def __init__(self, repository: InterfaceSale):
        self.repository = repository

    def execute(self, sale):
        self.repository.save(sale)
        

        