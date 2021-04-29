from models import User, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

andre = User(first_name='Andre', last_name='Pautin')
susan = User(first_name='Susan', last_name='Tran', image_url='')

db.session.add(andre)
db.session.add(susan)

db.session.commit()

# db.add_all(list) 