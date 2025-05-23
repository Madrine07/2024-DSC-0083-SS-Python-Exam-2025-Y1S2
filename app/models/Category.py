from app.extensions import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = "categories"
    category_id = db.Column(db.Integer, primary_key=True, nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id")) 
    created_at = db.Column(db.DateTime, default= datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())

    def __init__ (self, product_id):
          super(Category, self).__init__()
                         
          self.product_id = product_id  

    def category_info(self):      
          return  f" {self.product_id}"
          