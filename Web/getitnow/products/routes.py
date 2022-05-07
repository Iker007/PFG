
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_required, current_user
from getitnow.models import Product, Restaurant, SelectedProduct
from getitnow.products.forms import ProductForm
from getitnow import db

products = Blueprint('products', __name__)

@products.route("/restaurant/<int:id>/product/new", methods=['GET', 'POST'])
@login_required
def new_product(id):
    if current_user.username != 'admin':
        abort(403)
    else:
        product_form = ProductForm()
        if product_form.validate_on_submit():
            product = Product(name=product_form.name.data, price=product_form.price.data, description=product_form.description.data)
            product.restaurant_id = id
            db.session.add(product)
            db.session.commit()
            flash('Product information succesfully added!', 'success')
            return redirect(url_for('main.home'))
        return render_template('add_product.html', title='New product', form=product_form, legend='Add product')

@products.route("/restaurant/<int:restaurant_id>/product/<int:id>")
def product(restaurant_id, id):
    product = Product.query.get_or_404(id)
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    selected_products = SelectedProduct.query.all()
    restaurant_id = restaurant_id
    return render_template('product.html', title=product.name, product=product, restaurant=restaurant, selected_products=selected_products)

@products.route("/restaurant/<int:restaurant_id>/product/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_product(restaurant_id, id):
    product = Product.query.get_or_404(id)
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    restaurant_id = restaurant_id
    if current_user.username != 'admin':
        abort(403)
    update_product_form = ProductForm()
    if update_product_form.validate_on_submit():
        product.name = update_product_form.name.data
        product.price = update_product_form.price.data
        product.description = update_product_form.description.data
        db.session.commit()
        flash('Product information succesfully updated!', 'success')
        return redirect(url_for('products.product', restaurant_id=restaurant.id, id=product.id))
    elif request.method == 'GET':
        update_product_form.name.data = product.name
        update_product_form.price.data = product.price
        update_product_form.description.data = product.description
    return render_template('add_product.html', title='Update product', form=update_product_form, legend='Update product', restaurant=restaurant)

@products.route("/restaurant/<int:restaurant_id>/product/<int:id>/delete", methods=['POST'])
@login_required
def delete_product(restaurant_id, id):
    product = Product.query.get_or_404(id)
    restaurant_id = restaurant_id
    if current_user.username != 'admin':
        abort(403)
    db.session.delete(product)
    db.session.commit()
    flash('Product information succesfully removed!', 'success')
    return redirect(url_for('main.home'))

@products.route("/restaurant/<int:restaurant_id>/product/<int:id>/add", methods=['GET', 'POST'])
@login_required
def add_product(restaurant_id, id):
    product = Product.query.get_or_404(id)
    selected_product = SelectedProduct(name=product.name, price=product.price, description=product.description, restaurant_id=product.restaurant_id)
    restaurant_id = restaurant_id
    db.session.add(selected_product)
    db.session.commit()
    flash('Product added to chart!', 'success')
    return redirect(url_for('main.home'))
