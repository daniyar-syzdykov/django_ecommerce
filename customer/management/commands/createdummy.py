from django.core.management.base import BaseCommand, CommandError
from store.models import Product
from customer.models import Customer, Order, OrderDetails
from customer.api.serializers import CustomerCreationSerializer
from store.api.serializers import ProductCreationSerializer

"TODO it is easy to make only one function to create all of the objects"


class Command(BaseCommand):
    help = 'Creates dummy customers, products and orders with order details for testing purposes'

    def add_arguments(self, parser) -> None:
        parser.add_argument('amount', type=int)

    def create_dummy_customers(self, amount) -> list[dict]:
        customers = []
        last_customer_id = Customer.objects.last()
        last_customer_id = Customer(id=0) if not last_customer_id else last_customer_id
        for n in range(last_customer_id.id + 1, amount + last_customer_id.id + 1):
            username = f'testuser{n}'
            password_1 = f'testpass{n}'
            password_2 = f'testpass{n}'
            customer = {'username': username,
                        'password': password_1, 'password_2': password_2}
            customers.append(customer)
        return customers

    def create_dummy_products(self, amount):
        products = []
        last_product_id = Product.objects.last()
        last_product_id = Product(id=0) if not last_product_id else last_product_id
        for n in range(last_product_id.id + 1, amount + last_product_id.id + 1):
            name = f'product{n}'
            description = f'desription{n}'
            price = n * 100
            product = {'name': name,
                       'description': description, 'price': price}
            products.append(product)
        return products

    def save_new_customers(self, customers):
        for customer in customers:
            new_customer = CustomerCreationSerializer(data=customer)
            if not new_customer.is_valid():
                raise CommandError('Customer already exists')
            new_customer.save()
            # print(new_customer)
            self.stdout.write(self.style.SUCCESS(
                'Created customer "%s"' % new_customer['username'].value))

    def save_new_products(self, products):
        for product in products:
            new_product = ProductCreationSerializer(data=product)
            if not new_product.is_valid():
                raise CommandError('Product already exists')
            new_product.save()
            self.stdout.write(self.style.SUCCESS(
                'Created product "%s"' % new_product['name'].value))

    def handle(self, *args, **options):
        amount = options['amount']
        customers = self.create_dummy_customers(amount)
        products = self.create_dummy_products(amount)
        self.save_new_customers(customers)
        self.save_new_products(products)
