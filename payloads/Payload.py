from faker import Faker
import random
from datamodels.Product import Product
from datamodels.User import User
from datamodels.Name import Name
from datamodels.Geolocation import Geolocation
from datamodels.Address import Address
from datamodels.CartProduct import CartProduct
from datamodels.Cart import Cart
from datetime import datetime


class Payload:
    faker = Faker()
    categories = ["electronics", "furniture", "clothing", "books", "beauty"]

    def product_payload(self) -> Product:
        title = self.faker.unique.catch_phrase()
        price = float(self.faker.pricetag().replace("$", "").replace(",", ""))
        description = self.faker.sentence()
        image_url = "https://i.pravatar.cc/100"
        category = random.choice(self.categories)
        return Product(title, price, description, image_url, category)

    def user_payload(self) -> User:
        # Name
        firstname = self.faker.first_name()
        lastname = self.faker.last_name()
        name = Name(firstname=firstname, lastname=lastname)

        # Geolocation
        lat = self.faker.latitude()
        lng = self.faker.longitude()
        geolocation = Geolocation(lat=str(lat), lng=str(lng))

        # Address
        city = self.faker.city()
        street = self.faker.street_name()
        number = random.randint(1, 100)
        zipcode = self.faker.zipcode()
        address = Address(city=city, street=street, number=number, zipcode=zipcode, geolocation=geolocation)

        email = self.faker.email()
        username = self.faker.user_name()
        password = self.faker.password()
        phone = self.faker.phone_number()

        return User(email=email, username=username, password=password, name=name, address=address, phone=str(phone))


    #cart
    def cart_payload(self,user_id:int)->Cart:
        product_id = random.randint(1,100)
        quantity = random.randint(1,10)
        cart_product = CartProduct(productId=product_id,quantity=quantity)
        today = datetime.today().strftime("%Y-%m-%d")
        return Cart(userId=user_id,date=today,products=[cart_product])


