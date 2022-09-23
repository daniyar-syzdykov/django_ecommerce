from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import ProductSerializer, ProductCreationSerializer
from ..models import Product


@api_view(['GET', ])
def test_view(request: Request):
    return Response({'hi', 'there'})


@api_view(['GET', 'POST', ])
def products(request: Request):
    if request.method == 'GET':
        products = Product.objects.all()
        response = ProductSerializer(products, many=True)
        return Response({'success': True, 'data': response.data})

    elif request.method == 'POST':
        new_product = ProductCreationSerializer(data=request.data)
        if not new_product.is_valid():
            return Response({'success': False, 'message': new_product.errors})
        new_product.save()
        return Response({'success': True, 'message': 'Prodict created succesfully'})


def get_prudoct_by_id(request: Request, id: int):
    response = Response(
        {'success': False, 'message': 'Internal server error', 'code': 500})
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        message = f'Product with id: {id} does not exist.'
        response = Response(
            {'success': False, 'message': message, 'code': 404})
    else:
        serialized_product = ProductSerializer(product)
        response = Response({'success': True, 'data': serialized_product.data})
    return response


def update_product_by_id(request: Request, id: int):
    response = Response(
        {'success': False, 'message': 'Internal server error', 'code': 500})
    try:
        Product.objects.filter(id=id).update(**request.data)
    except Product.DoesNotExist:
        message = f'Product with id: {id} does not exist.'
        response = Response(
            {'success': False, 'message': message, 'code': 404})
    else:
        message = f'Product with id: {id} was updated.'
        response = Response({'success': True, 'message': message})
    return response


def delete_product_by_id(request, id):
    response = Response(
        {'success': False, 'message': 'Internal server error', 'code': 500})
    try:
        product = Product.objects.filter(id=id).delete()
    except Product.DoesNotExist:
        message = f'Product with id: {id} does not exist.'
        response = Response(
            {'success': False, 'message': message, 'code': 404})
    else:
        message = f'Product with id: {id} was deleted.'
        serialized_product = ProductSerializer(product)
        response = Response(
            {'success': True, 'message': message, 'data': serialized_product.data})
    return response


@api_view(['GET', 'PATCH', 'DELETE', ])
def product_by_id(request: Request, id: int):
    response = Response(
        {'success': False, 'message': 'Internal server error', 'code': 500})
    if request.method == 'GET':
        return get_prudoct_by_id(request, id)
    elif request.method == 'PATCH':
        return update_product_by_id(request, id)
    elif request.method == 'DELETE':
        return delete_product_by_id(request, id)
    return response


@api_view(['GET', ])
def delete_product(request, id):
    response = Response(
        {'success': False, 'message': 'Internal server error', 'code': 500})
    try:
        Product.delete(id=id)
    except Product.DoesNotExist:
        message = f'Product with id: {id} does not exists'
        response = Response(
            {'success': False, 'message': message, 'code': 404})
    else:
        message = f'Product with id: {id} was deleted'
        response = Response({'success': True, 'message': message})
    return response
