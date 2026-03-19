import sqlite3
from core.domain.sale_item.sale_item_interface import InterfaceSaleItem

class SQLiteSaleItemRepository(InterfaceSaleItem):
    def __init__(self, db_path="DistribDB.db"):
        self.db_path = db_path
        self._criar_tabela()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _criar_tabela(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sale_item (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                price REAL,
                FOREIGN KEY(sale_id) REFERENCES sale(id),
                FOREIGN KEY(product_id) REFERENCES product(id)
            );
        """)
        conn.commit()
        conn.close()

    def list(self):
       
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row  
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                si.sale_id, 
                s.date, 
                si.quantity, 
                p.name AS product_name, 
                p.sale_price
            FROM sale_item si
            JOIN sale s ON si.sale_id = s.id
            JOIN product p ON si.product_id = p.id
            ORDER BY si.sale_id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]
    
    def remove(self, sale_id):
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM sale_item WHERE id = ? ",
            (sale_id,)
        )
        conn.commit()

    def monthly_profit(self):
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                strftime('%Y-%m', s.date) AS month,
                SUM((si.price - p.buy_price) * si.quantity) AS profit
                FROM sale_item si
                JOIN sale s ON si.sale_id = s.id
                JOIN product p ON si.product_id = p.id
                GROUP BY month
                ORDER BY month
                        """)

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]      
