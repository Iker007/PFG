from flask import request
from flask_restx import Api, Resource, fields
from getitnow import db, bcrypt
from getitnow.models import User, Restaurant, Product, SelectedProduct, Order
from getitnow import new_app, new_api



app=new_app()

api=new_api(app)

restaurant_model=api.model(
    'Restaurant',
    {
        'id':fields.Integer(),
        'name':fields.String(),
        'location':fields.String(),
        'description':fields.String(),
        'restaurant_picture':fields.String(),
    }
)

product_model=api.model(
    'Product',
    {
        'id':fields.Integer(),
        'name':fields.String(),
        'price':fields.Float(),
        'description':fields.String(),
        'restaurant_id':fields.Integer(),
    }
)

selected_product_model=api.model(
    'SelectedProduct',
    {
        'id':fields.Integer(),
        'name':fields.String(),
        'price':fields.Float(),
        'description':fields.String(),
        'restaurant_id':fields.Integer(),
    }
)

order_model=api.model(
    'Order',
    {
        'id':fields.Integer(),
        'date_ordered':fields.DateTime(),
        'price':fields.Float(),
        'description':fields.String(),
        'user_id':fields.Integer(),
    }
)

user_model=api.model(
    'User',
    {
        'id':fields.Integer(),
        'username':fields.String(),
        'email':fields.String(),
        'password':fields.String(),
        'address':fields.String(),
        'profile_picture':fields.String(),
        'orders':fields.Nested(order_model),
    }
)

@api.route('/users')
class Users(Resource):

    @api.marshal_list_with(user_model,code=200,envelope="users")
    def get(self):
        ''' Get all users '''
        users=User.query.all()
        return users

    @api.marshal_with(user_model,code=201,envelope="user")
    @api.expect(user_model)
    def post(self):
        ''' Create a new user '''
        data=request.get_json()

        username=data.get('username')
        email=data.get('email')
        hashed_pw = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
        password=hashed_pw
        address=data.get('address')

        new_user=User(username=username, email=email, password=password, address=address)

        db.session.add(new_user)

        db.session.commit()

        return new_user

@api.route('/user/<int:id>')
class UserResource(Resource):

    @api.marshal_with(user_model,code=200,envelope="user")
    def get(self,id):

        ''' Get a user by id '''
        user=User.query.get_or_404(id)

        return user,200

    @api.marshal_with(user_model,envelope="user",code=200)
    @api.expect(user_model)
    def put(self,id):

        ''' Update a user'''
        user_to_update=User.query.get_or_404(id)

        data=request.get_json()

        user_to_update.username=data.get('username')

        user_to_update.email=data.get('email')

        hashed_pw = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
        user_to_update.password=hashed_pw

        user_to_update.address=data.get('address')

        db.session.commit()

        return user_to_update,200

    @api.marshal_with(user_model,envelope="user_deleted",code=200)
    def delete(self,id):
        '''Delete a user'''
        user_to_delete=User.query.get_or_404(id)

        db.session.delete(user_to_delete)

        db.session.commit()

        return user_to_delete,200


@api.route('/restaurants')
class Restaurants(Resource):

    @api.marshal_list_with(restaurant_model,code=200,envelope="restaurants")
    def get(self):
        ''' Get all restaurants '''
        restaurants=Restaurant.query.all()
        return restaurants

    @api.marshal_with(restaurant_model,code=201,envelope="restaurant")
    @api.expect(restaurant_model)
    def post(self):
        ''' Create a new restaurant '''
        data=request.get_json()

        name=data.get('name')
        location=data.get('location')
        description=data.get('description')

        new_restaurant=Restaurant(name=name, location=location, description=description)

        db.session.add(new_restaurant)

        db.session.commit()

        return new_restaurant

@api.route('/restaurants/<int:id>')
class RestaurantResource(Resource):

    @api.marshal_with(restaurant_model,code=200,envelope="restaurant")
    def get(self,id):

        ''' Get a restaurant by id '''
        restaurant=Restaurant.query.get_or_404(id)

        return restaurant,200

    @api.marshal_with(restaurant_model,envelope="restaurant",code=200)
    @api.expect(restaurant_model)
    def put(self,id):

        ''' Update a restaurant'''
        restaurant_to_update=Restaurant.query.get_or_404(id)

        data=request.get_json()

        restaurant_to_update.name=data.get('name')

        restaurant_to_update.location=data.get('location')

        restaurant_to_update.description=data.get('description')

        db.session.commit()

        return restaurant_to_update,200

    @api.marshal_with(restaurant_model,envelope="restaurant_deleted",code=200)
    def delete(self,id):
        '''Delete a restaurant'''
        restaurant_to_delete=Restaurant.query.get_or_404(id)

        db.session.delete(restaurant_to_delete)

        db.session.commit()

        return restaurant_to_delete,200


@api.route('/products')
class Products(Resource):

    @api.marshal_list_with(product_model,code=200,envelope="products")
    def get(self):
        ''' Get all products '''
        products=Product.query.all()
        return products

    @api.marshal_with(product_model,code=201,envelope="product")
    @api.expect(product_model)
    def post(self):
        ''' Create a new product '''
        data=request.get_json()

        name=data.get('name')
        price=data.get('price')
        description=data.get('description')
        restaurant_id=data.get('restaurant_id')

        new_product=Product(name=name, price=price, description=description, restaurant_id=restaurant_id)

        db.session.add(new_product)

        db.session.commit()

        return new_product

@api.route('/products/<int:id>')
class ProductResource(Resource):

    @api.marshal_with(product_model,code=200,envelope="product")
    def get(self,id):

        ''' Get a product by id '''
        product=Product.query.get_or_404(id)

        return product,200

    @api.marshal_with(product_model,envelope="product",code=200)
    @api.expect(product_model)
    def put(self,id):

        ''' Update a product'''
        product_to_update=Product.query.get_or_404(id)

        data=request.get_json()

        product_to_update.name=data.get('name')

        product_to_update.price=data.get('price')

        product_to_update.description=data.get('description')

        product_to_update.restaurant_id=data.get('restaurant_id')

        db.session.commit()

        return product_to_update,200

    @api.marshal_with(product_model,envelope="product_deleted",code=200)
    def delete(self,id):
        '''Delete a product'''
        product_to_delete=Product.query.get_or_404(id)

        db.session.delete(product_to_delete)

        db.session.commit()

        return product_to_delete,200


@api.route('/selectedproducts')
class SelectedProducts(Resource):

    @api.marshal_list_with(selected_product_model,code=200,envelope="selected_products")
    def get(self):
        ''' Get all selected products '''
        selected_products=SelectedProduct.query.all()
        return selected_products

    @api.marshal_with(selected_product_model,code=201,envelope="selected_product")
    @api.expect(selected_product_model)
    def post(self):
        ''' Create a new selected product '''
        data=request.get_json()

        name=data.get('name')
        price=data.get('price')
        description=data.get('description')
        restaurant_id=data.get('restaurant_id')

        new_selected_product=SelectedProduct(name=name, price=price, description=description, restaurant_id=restaurant_id)

        db.session.add(new_selected_product)

        db.session.commit()

        return new_selected_product

@api.route('/selectedproducts/<int:id>')
class SelectedProductResource(Resource):

    @api.marshal_with(selected_product_model,code=200,envelope="selected_product")
    def get(self,id):

        ''' Get a selected product by id '''
        selected_product=SelectedProduct.query.get_or_404(id)

        return selected_product,200

    @api.marshal_with(selected_product_model,envelope="selected_product",code=200)
    @api.expect(selected_product_model)
    def put(self,id):

        ''' Update a selected product'''
        selected_product_to_update=SelectedProduct.query.get_or_404(id)

        data=request.get_json()

        selected_product_to_update.name=data.get('name')

        selected_product_to_update.price=data.get('price')

        selected_product_to_update.description=data.get('description')

        selected_product_to_update.restaurant_id=data.get('restaurant_id')

        db.session.commit()

        return selected_product_to_update,200

    @api.marshal_with(selected_product_model,envelope="selected_product_deleted",code=200)
    def delete(self,id):
        '''Delete a selected product'''
        selected_product_to_delete=SelectedProduct.query.get_or_404(id)

        db.session.delete(selected_product_to_delete)

        db.session.commit()

        return selected_product_to_delete,200


@api.route('/order')
class Orders(Resource):

    @api.marshal_list_with(order_model,code=200,envelope="orders")
    def get(self):
        ''' Get all orders '''
        order=Order.query.all()
        return order

    @api.marshal_with(order_model,code=201,envelope="order")
    @api.expect(order_model)
    def post(self):
        ''' Create a new order '''
        data=request.get_json()

        date_ordered=data.get('date_ordered')
        price=data.get('price')
        description=data.get('description')
        user_id=data.get('user_id')

        new_order=Order(date_ordered=date_ordered, price=price, description=description, user_id=user_id)

        db.session.add(new_order)

        db.session.commit()

        return new_order

@api.route('/order/<int:id>')
class OrderResource(Resource):

    @api.marshal_with(order_model,code=200,envelope="order")
    def get(self,id):

        ''' Get a order by id '''
        order=Order.query.get_or_404(id)

        return order,200

    @api.marshal_with(order_model,envelope="order",code=200)
    @api.expect(order_model)
    def put(self,id):

        ''' Update a order'''
        order_to_update=Order.query.get_or_404(id)

        data=request.get_json()

        order_to_update.date_ordered=data.get('date_ordered')

        order_to_update.price=data.get('price')

        order_to_update.description=data.get('description')

        order_to_update.user_id=data.get('user_id')

        db.session.commit()

        return order_to_update,200

    @api.marshal_with(order_model,envelope="order_deleted",code=200)
    def delete(self,id):
        '''Delete a order'''
        order_to_delete=Order.query.get_or_404(id)

        db.session.delete(order_to_delete)

        db.session.commit()

        return order_to_delete,200

if __name__ == "__main__":
    app.run(debug=True)