from flask import Blueprint, render_template, request, redirect, url_for 
from core.domain.product.product import Product
from core.domain.sale.sale import Sale 
from datetime import datetime
def create_product_blueprint(uc_create, uc_list, uc_delete_produto, uc_edit_product, uc_create_sale, uc_list_sale_item, uc_remove_sale_item, uc_list_metricas):
    bp = Blueprint('products', __name__)

    @bp.route('/')
    def home_page():
        return render_template('index.html')
    
    @bp.route('/produtos')
    def produto_page():
        
        produtos = uc_list.execute()
    
        return render_template('products.html', produtos=produtos)
    
    @bp.route('/produtos/novo', methods=['POST'])
    def cadastrar_produtos():
        dados = {
            'name': request.form.get('nome'),
            'amount': int(request.form.get('quantidade')),
            'sale_price': float(request.form.get('preco_venda')),
            'sale_buy': float(request.form.get('preco_compra'))

        }
        uc_create.execute(dados)

        return redirect(url_for('products.produto_page'))
    
    @bp.route('/produtos/deletar/<int:id>', methods=['GET'])
    def deletar_produto(id):
    
        uc_delete_produto.execute(id)

        return redirect(url_for('products.produto_page'))

    @bp.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
    def editar_produto(id):
        if request.method == 'POST':
            product = Product(
                id=id, 
                name=request.form.get('nome'),
                amount=int(request.form.get('quantidade', 0)),
                sale_price=float(request.form.get('preco_venda', 0)),
                buy_price=float(request.form.get('preco_compra', 0))
            )
         
            uc_edit_product.execute(product)
            return redirect(url_for('products.produto_page'))

    
        todos_produtos = uc_list.execute()
        produto = next((p for p in todos_produtos if p['id'] == id), None)
        if not produto:
            return "Produto não encontrado", 404

        return render_template('edit-produto.html', produto=produto)
    @bp.route('/metricas')
    def page_metricas():
        monthly_profits = uc_list_metricas.execute()
        return render_template('metricas.html', monthly_profits=monthly_profits)
        

    @bp.route('/vendas', methods=['GET','POST'])
    def vendas_page():
        if request.method == 'POST':
            sale_date = request.form.get('data')
            if not sale_date:
                sale_date = datetime.now().strftime("%Y-%m-%d")
            sale = Sale(
                date=sale_date,
                product_id=int(request.form.get('id')),
                quantity=int(request.form.get('quantidade'))
            )
            uc_create_sale.execute(sale)
            redirect(url_for('products.page_metricas'))
        produtos = uc_list.execute() 
        list_sale_items = uc_list_sale_item.execute()
        return render_template('vendas.html', list_sale_items=list_sale_items, produtos=produtos)
    
    @bp.route('/vendas/excluir/<int:sale_id>', methods=['GET'])
    def remove_sale_item(sale_id):
        uc_remove_sale_item.execute(sale_id)

        return redirect(url_for('products.vendas_page'))

    return bp

    
    
    