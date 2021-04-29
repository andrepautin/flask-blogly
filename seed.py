from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()

andre = User(first_name='Andre', last_name='Pautin')
susan = User(first_name='Susan', last_name='Tran', image_url='')

db.session.add(andre)
db.session.add(susan)
db.session.commit()

post1 = Post(post_title="Andre's post", post_content="blah blah blah", post_user_id=1)
post2 = Post(post_title="Susan's post", post_content="blah blah blah", post_user_id=2)

db.session.add(post1)
db.session.add(post2)
db.session.commit()

# create some posts

# db.add_all(list) 