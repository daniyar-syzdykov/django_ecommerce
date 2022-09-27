from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from customer.models import Customer, Order, OrderDetails


class CustomerCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(Customer.objects.all()), ])
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    password_2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Customer
        fields = ['username', 'password', 'password_2']
        extra_kwargs = {
            'username': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_2']:
            raise serializers.ValidationError(
                {'error': 'Passwords does not match.'})
        return attrs

    def save(self):
        customer = Customer(
            username=self.validated_data['username'],
        )
        customer.set_password(self.validated_data['password'])
        customer.save()
        return customer


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class CustomerSrializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'
