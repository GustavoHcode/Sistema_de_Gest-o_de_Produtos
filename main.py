from flask import Flask 
from infrastructure.sqlite3_repository import SQLiteProductRepository
from infrastructure.sqlite3_sale_repository import SQLiteSaleRepository
from infrastructure.sqlite3_sale_item_repository import SQLiteSaleItemRepository
from core.use_case.product_use_case.product_use_case import CreateProduct, ListProduct, RemoveProduct, EditProduct
from core.use_case.sale_use_case.sale_use_case import CreateSale
from core.use_case.sale_item_use_case.sale_item_use_case import ListSaleItem, RemoveSaleItem, Metricas
from web.routes import create_product_blueprint


def create_app():

    app = Flask(__name__,
                template_folder='web/templates',
                static_folder='web/static')
    
    product_repository = SQLiteProductRepository()
    sale_repository = SQLiteSaleRepository()
    sale_item_repository = SQLiteSaleItemRepository()

    uc_create = CreateProduct(product_repository)
    uc_list = ListProduct(product_repository)
    uc_delete_product = RemoveProduct(product_repository)
    uc_edit_product = EditProduct(product_repository)

    uc_create_sale = CreateSale(sale_repository)

    uc_list_sale_item = ListSaleItem(sale_item_repository)
    uc_remove_sale_item = RemoveSaleItem(sale_item_repository)
    uc_list_metricas = Metricas(sale_item_repository)
    

    product_blueprint = create_product_blueprint(uc_create, uc_list, uc_delete_product, uc_edit_product, uc_create_sale, uc_list_sale_item, uc_remove_sale_item, uc_list_metricas)
    app.register_blueprint(product_blueprint)

    return app

if __name__ == "__main__":
    app = create_app()

    app.run(debug=True)