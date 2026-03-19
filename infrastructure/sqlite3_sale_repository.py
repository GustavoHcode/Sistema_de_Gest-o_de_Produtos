import sqlite3
from datetime import datetime
from core.domain.sale.sale_interface import InterfaceSale
from core.domain.sale.sale import Sale

class SQLiteSaleRepository(InterfaceSale):
    def __init__(self, db_path="DistribDB.db"):
        self.db_path = db_path
        self._criar_tabela()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _criar_tabela(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sale (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL
            );
        """)
        conn.commit()
        conn.close()

    def save(self, sale: Sale):
        conn = self._get_connection()
        cursor = conn.cursor()

        product_id = sale.product_id
        quantity = sale.quantity
        sale_date = sale.date

        cursor.execute("SELECT amount, sale_price FROM product WHERE id = ?", (product_id,))
        product = cursor.fetchone()

        if product is None:
            print("Produto não existe")
            conn.close()
            return False

        stock, price = product
        if stock < quantity:
            print("Estoque insuficiente")
            conn.close()
            return False

        cursor.execute("INSERT INTO sale (date) VALUES (?)",
                       (sale.date,))
        sale_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO sale_item (sale_id, product_id, quantity, price) VALUES (?,?,?,?)",
            (sale_id, product_id, quantity, price)
        )

        cursor.execute(
            "UPDATE product SET amount = amount - ? WHERE id = ?",
            (quantity, product_id)
        )

        conn.commit()
        conn.close()
        return True