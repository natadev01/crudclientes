from models import db, Client, Address
from faker import Factory

fake = Factory.create()

db.drop_all()
db.create_all()
for num in range(5):
    fullname = fake.name().split()
    name = fullname[0]
    lastName = ' '.join(fullname[1:])
    email = fake.email()
    phone = fake.phone_number()
    my_client = Client(name=name, lastName=lastName, email=email, phone=phone)

    db.session.add(my_client)

db.session.commit()


for num in range(5):
    address = fake.address()
    my_address = Address(address=address, client_id=num)
    db.session.add(my_address)

db.session.commit()