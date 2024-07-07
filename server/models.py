from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    # add relationship
    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates="restaurant")
    # add serialization rules
    serialize_rules = ("-restaurant_pizzas.restauraunt",)
    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates="pizza")
    # add serialization rules
    serialize_rules = ("-restaurant_pizzas.pizza",)

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    restaurant = db.relationship("Restaurant", back_populates="restaurant_pizzas")
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))
    pizza = db.relationship("Pizza", back_populates="restaurant_pizzas")


    # add serialization rules
    serialize_rules = ['-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas']


    # add validation
    @validates('price')
    def validate_price(self, key, new_price):
        if not (1 <= new_price <= 30):
            raise ValueError('price must be between 1 and 30')
        else:
            return new_price
    

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"