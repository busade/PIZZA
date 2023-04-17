from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import db
from werkzeug.exceptions import Conflict, BadRequest



order_namespace= Namespace('order', description="Namespace for order")

order_model = order_namespace.model(
                'Order',{
                        'id': fields.Integer(),
                        'size': fields.String(description="size of an order", required = True,
					            enum=["SMALL","MEDIUM","LARGE","EXRA_LARGE"]),	
                        'flavor':fields.String(description='Flavor of the pizza', required= True),
                        'quantity':fields.String(description = 'quantity of the order', required= True),
                        'status':fields.String(description=' Status of order', 
                                                     enum=['PENDING', 'IN-TRANSIT', 'DELIVERED'])
                }
)


@order_namespace.route('/orders')
class OrderGetCreate(Resource):
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description= "Retrieve all Orders"
            )
    @jwt_required()
    def get (self):
        """Get all order"""
        order = Order.query.all()
        return order, HTTPStatus.OK


    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description= "Post an Order"
    )
    @jwt_required()
    def post(self):
        """Make an Order"""
        username= get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        print (current_user)
        data = order_namespace.payload
        new_order = Order(
                        size = data['size'],
                        flavor= data['flavor'],
                        quantity = data['quantity']

        )
        new_order.users= current_user
        new_order.save()
        return new_order,HTTPStatus.CREATED

@order_namespace.route('/orders/<int:order_id>')
class GetUpdateDelete(Resource):
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description= "Retrieve an Order by id",
        params={
                "order_id":"An ID for a given Order"
        }
    )
    @jwt_required()
    def get(self, order_id):
        """Retrieve an order by id"""
        order= Order.get_by_id(order_id)
        return order,HTTPStatus.OK
    
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description= "Update an order by id",
        params={
                "order_id":"An ID for a given Order"
        }
    )
    @jwt_required()
    def put (self,order_id):
        """Update an Order by id"""
        order_to_update= Order.get_by_id(order_id)
        data = order_namespace.payload
        order_to_update.size =data['size']
        order_to_update.quantity=data['quantity']
        order_to_update.flavor= data['flavor']

        db.session.commit()
        return order_to_update, HTTPStatus.ACCEPTED
    
    @order_namespace.doc(
        description= "Delete an order by id",
        params={
                "order_id":"An ID for a given Order"
        }
    )
    @jwt_required()
    def delete(self, order_id):
        """Delete an order by id"""
        order_to_delete= Order.get_by_id(order_id)
        db.session.delete(order_to_delete)
        db.session.commit()
        return{'Message': "Order deleted successfully"}, HTTPStatus.OK
    






@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByUser(Resource):
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description= "Retrieve a  user's specific order",
        params={
                "order_id":"An ID for a given Order",
                "user_id":"the user's id"
        }
    )
    @jwt_required()
    def get(self, user_id, order_id):
        """Get a user's specific order"""
        user = User.get_by_id(user_id)
        order = Order.query.filter_by(id=order_id).filter_by(users=user).first()
        return order, HTTPStatus.OK
        




@order_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description= "Retrieve all Orders by a particular user",
        params={
                "user_id":"An ID for a user"
        }
    )
    @jwt_required()
    def get (self,user_id):
        """Get all orders by a specific User"""
        try:
            user = User.get_by_id(user_id)
            order = user.order
            return order, HTTPStatus.OK
        except Exception as e:
            raise Conflict("Invalid user_id")



@order_namespace.route('/orders/status/<int:order_id>')
class UpdateOrderStatus(Resource):
    @order_namespace.marshal_with(order_model)
    @order_namespace.expect(order_model)
    @order_namespace.doc(
        description= "Update the status of an order",
        params={
                "order_id":"An ID for a given Order"
        }
    )
    @jwt_required()
    def patch(self, order_id):
        """Update the status of an order"""
        data = order_namespace.payload
        try:
            order_to_update= Order.get_by_id(order_id)
            order_to_update.status = data['status']
        except Exception as e:
            raise Conflict("Invalid order id")

        return order_to_update, HTTPStatus.ACCEPTED

    