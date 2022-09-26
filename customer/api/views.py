from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from ..models import Customer, Order, OrderDetails
from store.models import Product
from .serializers import CustomerSrializer, CustomerCreationSerializer, OrderSerializer, OrderDetailsSerializer
from utils import api_response


@api_view(['GET', ])
def test_view(request: Request):
    response = Response({'success': False})
    print(dir(response))


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_users(request: Request):
    users = Customer.objects.all()
    ret = CustomerSrializer(users, many=True)
    return api_response(success=True, data=ret.data)


@api_view(['GET', ])
@permission_classes([IsAdminUser])
def get_user_by_id(request: Request, id):
    try:
        user: Customer = Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        message = f'User with id: {id} not found'
        return api_response(success=False, status_code=404, message=message)

    ret = CustomerSrializer(user)
    return api_response(success=True, status_code=200, data=ret.data)


@api_view(['POST', ])
def register_new_user(request: Request):
    new_user = CustomerCreationSerializer(data=request.data)
    if not new_user.is_valid():
        message = 'Serialazation error'
        return api_response(success=False, status_code=500, message=message, data=new_user.errors)
    customer = new_user.save()
    customer = CustomerSrializer(customer)
    return Response({'success': True, 'user': customer.data})


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def add_to_wish_list(request: Request):
    product_id = request.data.get('product_id', None)
    if not product_id:
        message = f'Pls provide product id'
        return api_response(success=False, status_code=400, message=message)
    if not Product.objects.filter(id=product_id).exists():
        message = f'Product with id: {product_id} does not exists.'
        return api_response(success=False, status_code=404, message=message)
    user = Customer.objects.get(id=request.user.id)
    user.wish_list.add(product_id)
    return api_response(success=True, status_code=201)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart(request: Request):
    product_id = request.data.get('product_id', None)
    if not Product.objects.filter(id=product_id).exists():
        message = f'Product with id: {product_id} does not exists.'
        return api_response(success=False, message=message)
    user: Customer = Customer.objects.get(id=request.user.id)

    if request.method == 'POST':
        user.cart.add(product_id)
        return api_response(success=True, message='Product was added to customers cart')

    elif request.method == 'DELETE':
        user.cart.remove(product_id)
        return api_response(success=True, message='Product was deleted from customers cart')


def query_products(product_ids: list[int]) -> list[Product] | None:
    ret = []
    products: Product = Product.objects.all()
    for product in products:
        if product.id in product_ids:
            ret.append(product)
    return ret if ret else None


def get_user_cart(user: Customer) -> list[int] | None:
    cart = Customer.objects.get(id=user.id)
    cart = CustomerSrializer(cart)['cart'].value
    return cart


def create_new_order(user: Customer, products: list[Product]):
    new_order: Order = Order(customer=user)
    new_order.save()
    ordered_objects = []
    for product in products:
        order_details = OrderDetails(
            order=new_order,
            product=product,
            status='In delivery')
        order_details.save()
        ordered_objects.append(order_details)
    return ordered_objects


def delete_from_cart(user: Customer, products: list[Product]):
    "TODO make this function more raliable"
    for product in products:
        try:
            user.cart.remove(product.id)
        except Exception as e:
            print(e)


@api_view(['POST', ])
@permission_classes([IsAdminUser, ])
def make_staff(request: Request):
    employee: Customer = Customer.objects.filter(
        id=request.data['employee_id']).update(is_staff=True)
    message = f'User is now employee'
    return api_response(success=True, message=message)



@api_view(['GET', ])
def get_order(request: Request, id: int):
    order = Order.objects.get(id=id)
    order = OrderSerializer(order)
    return api_response(success=True, data=order.data)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def purchase(request: Request):
    cart = get_user_cart(request.user)
    if not cart:
        return api_response(success=False, status_code=400, message='Your cart is empty')

    products = query_products(cart)
    if not products:
        return api_response(success=False, message='These products no longer exists')

    final_price = sum([product.price for product in products])
    ordered = create_new_order(request.user, products)
    # print(ordered)
    delete_from_cart(request.user, products)

    data = {'id': request.user.id, 'products': cart, 'final price': final_price}
    return api_response(success=True, data=data)
