from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from customer.models import Customer, Order, OrderDetails


class CustomerSrializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        # fields = ['usernmae', 'email', 'whish_list', 'first_name', 'last_name']
        fields = '__all__'


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
        # fields = '__all__'
        extra_kwargs = {
            'username': {'required': True},
            # 'password': {'write_only': True, 'required': True, }
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_2']:
            raise serializers.ValidationError(
                {'password': 'Passwords does not match.'})
        return attrs

    def save(self):
        customer = Customer(
            username=self.validated_data['username'],
        )
        # if password != password_2:
        #     raise serializers.ValidationError(
        #         {'success': False, 'message': 'Passwords does not match.'})
        customer.set_password(self.validated_data['password'])
        customer.save()
        return customer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'
