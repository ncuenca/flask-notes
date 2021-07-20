from app import app
from models import db, User

# Create all tables
db.drop_all()
db.create_all()

# Create test data
user1 = User.register(username="iyang", password="1234", email="1234@gmail.com", first_name="Ivan", last_name="Yang")
user2 = User.register(username="ncuenca", password="1234", email="12345@gmail.com", first_name="Nathan", last_name="Cuenca")

db.session.add_all([user1,user2])
db.session.commit()
