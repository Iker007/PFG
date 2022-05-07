
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_required, current_user
from getitnow.models import Restaurant, Product, SelectedProduct
from getitnow.restaurants.forms import RestaurantForm
from getitnow import db

restaurants = Blueprint('restaurants', __name__)

@restaurants.route("/restaurant/new", methods=['GET', 'POST'])
@login_required
def new_restaurant():
    if current_user.username != 'admin':
        abort(403)
    else:
        restaurant_form = RestaurantForm()
        if restaurant_form.validate_on_submit():
            restaurant = Restaurant(name=restaurant_form.name.data, location=restaurant_form.location.data, description=restaurant_form.description.data)
            db.session.add(restaurant)
            db.session.commit()
            flash('Restaurant information succesfully added!', 'success')
            return redirect(url_for('main.home'))
        return render_template('add_restaurant.html', title='New restaurant', form=restaurant_form, legend='Add restaurant')

@restaurants.route("/restaurant/<int:id>")
def restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    products = Product.query.filter_by(restaurant_id = restaurant.id).all()
    selected_products = SelectedProduct.query.all()
    return render_template('restaurant.html', title=restaurant.name, restaurant=restaurant, products=products, selected_products=selected_products)

@restaurants.route("/restaurant/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    if current_user.username != 'admin':
        abort(403)
    update_restaurant_form = RestaurantForm()
    if update_restaurant_form.validate_on_submit():
        restaurant.name = update_restaurant_form.name.data
        restaurant.location = update_restaurant_form.location.data
        restaurant.description = update_restaurant_form.description.data
        db.session.commit()
        flash('Restaurant information succesfully updated!', 'success')
        return redirect(url_for('restaurants.restaurant', id=restaurant.id))
    elif request.method == 'GET':
        update_restaurant_form.name.data = restaurant.name
        update_restaurant_form.location.data = restaurant.location
        update_restaurant_form.description.data = restaurant.description
    return render_template('add_restaurant.html', title='Update restaurant', form=update_restaurant_form, legend='Update restaurant')

@restaurants.route("/restaurant/<int:id>/delete", methods=['POST'])
@login_required
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    if current_user.username != 'admin':
        abort(403)
    db.session.delete(restaurant)
    db.session.commit()
    flash('Restaurant information succesfully removed!', 'success')
    return redirect(url_for('main.home'))
