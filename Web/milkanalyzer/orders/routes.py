
from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import login_required, current_user
from milkanalyzer.models import SelectedProduct, Order
from milkanalyzer import db

orders = Blueprint('orders', __name__)

@orders.route("/order/new", methods=['GET', 'POST'])
@login_required
def new_order():
    selected_products = SelectedProduct.query.all()
    total_price = 0
    order_description = "Products:"
    for product in selected_products:
        total_price = total_price + product.price
        order_description = order_description + '\n' + product.name
    order = Order(price=total_price, description=order_description, user_id=current_user.id)
    db.session.add(order)
    db.session.query(SelectedProduct).delete()
    db.session.commit()
    flash('Order confirmed!', 'success')
    return redirect(url_for('main.home'))

@orders.route("/orders")
@login_required
def order_list():
    orders = Order.query.filter_by(user_id = current_user.id).all()
    selected_products = SelectedProduct.query.all()
    return render_template('orders.html', title='Your orders', orders=orders, selected_products=selected_products)