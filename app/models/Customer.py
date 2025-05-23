from app.extensions import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    name = db.Column(db.String(40))
    address = db.Column(db.String(200), nullable = False)
    image = db.Column(db.String(100), nullable = True) 
    product_id =db.Column(db.Integer, db.ForeignKey("products.id"))
    created_at = db.Column(db.DateTime, default= datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())

    def __init__ (self, product_id, address,name, image=None):
          super(Customer, self).__init__()
                         
          self.product_id = product_id   
          self.address = address           
          self.image= image
          self.name= name

    def customer_info(self):      
          return  f" {self.name} {self.address}"
