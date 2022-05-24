from flask import request
from flask_restx import Api, Resource, fields
from milkanalyzer import db, bcrypt
from milkanalyzer.models import User, AIModel, Value, Order, AIModel, Value
from milkanalyzer import new_app, new_api



app=new_app()

api=new_api(app)

aimodel_model=api.model(
    'AIModel',
    {
        'id':fields.Integer(),
        'name':fields.String(),
        'type':fields.String(),
        'description':fields.String(),
        'aimodel_picture':fields.String(),
    }
)

value_model=api.model(
    'Value',
    {
        'id':fields.Integer(),
        'name':fields.String(),
        'proportion':fields.String(),
        'description':fields.String(),
        'aimodel_id':fields.Integer(),
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


@api.route('/aimodels')
class AIModels(Resource):

    @api.marshal_list_with(aimodel_model,code=200,envelope="aimodels")
    def get(self):
        ''' Get all aimodels '''
        aimodels=AIModel.query.all()
        return aimodels

    @api.marshal_with(aimodel_model,code=201,envelope="aimodel")
    @api.expect(aimodel_model)
    def post(self):
        ''' Create a new aimodel '''
        data=request.get_json()

        name=data.get('name')
        type=data.get('type')
        description=data.get('description')

        new_aimodel=AIModel(name=name, type=type, description=description)

        db.session.add(new_aimodel)

        db.session.commit()

        return new_aimodel

@api.route('/aimodels/<int:id>')
class AIModelResource(Resource):

    @api.marshal_with(aimodel_model,code=200,envelope="aimodel")
    def get(self,id):

        ''' Get a aimodel by id '''
        aimodel=AIModel.query.get_or_404(id)

        return aimodel,200

    @api.marshal_with(aimodel_model,envelope="aimodel",code=200)
    @api.expect(aimodel_model)
    def put(self,id):

        ''' Update a aimodel'''
        aimodel_to_update=AIModel.query.get_or_404(id)

        data=request.get_json()

        aimodel_to_update.name=data.get('name')

        aimodel_to_update.type=data.get('type')

        aimodel_to_update.description=data.get('description')

        db.session.commit()

        return aimodel_to_update,200

    @api.marshal_with(aimodel_model,envelope="aimodel_deleted",code=200)
    def delete(self,id):
        '''Delete a aimodel'''
        aimodel_to_delete=AIModel.query.get_or_404(id)

        db.session.delete(aimodel_to_delete)

        db.session.commit()

        return aimodel_to_delete,200


@api.route('/values')
class Values(Resource):

    @api.marshal_list_with(value_model,code=200,envelope="values")
    def get(self):
        ''' Get all values '''
        values=Value.query.all()
        return values

    @api.marshal_with(value_model,code=201,envelope="value")
    @api.expect(value_model)
    def post(self):
        ''' Create a new value '''
        data=request.get_json()

        name=data.get('name')
        proportion=data.get('proportion')
        description=data.get('description')
        aimodel_id=data.get('aimodel_id')

        new_value=Value(name=name, proportion=proportion, description=description, aimodel_id=aimodel_id)

        db.session.add(new_value)

        db.session.commit()

        return new_value

@api.route('/values/<int:id>')
class ValueResource(Resource):

    @api.marshal_with(value_model,code=200,envelope="value")
    def get(self,id):

        ''' Get a value by id '''
        value=Value.query.get_or_404(id)

        return value,200

    @api.marshal_with(value_model,envelope="value",code=200)
    @api.expect(value_model)
    def put(self,id):

        ''' Update a value'''
        value_to_update=Value.query.get_or_404(id)

        data=request.get_json()

        value_to_update.name=data.get('name')

        value_to_update.proportion=data.get('proportion')

        value_to_update.description=data.get('description')

        value_to_update.aimodel_id=data.get('aimodel_id')

        db.session.commit()

        return value_to_update,200

    @api.marshal_with(value_model,envelope="value_deleted",code=200)
    def delete(self,id):
        '''Delete a value'''
        value_to_delete=Value.query.get_or_404(id)

        db.session.delete(value_to_delete)

        db.session.commit()

        return value_to_delete,200


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