from django.urls import path
# from .views import test_view, get_all_users
from .views import test_view, get_all_users, get_user_by_id, register_new_user, add_to_wish_list,cart, purchase, get_order


urlpatterns = [
    # path('', test_view, name='test_view'),
    # path('', get_all_users)
    # path('', CustomersView.as_view(), name='customers_view')
    path('', get_all_users),
    path('test/', test_view),
    path('register/', register_new_user),
    path('wishlist/', add_to_wish_list),
    path('cart/', cart),
    path('<int:id>', get_user_by_id),
    path('purchase/', purchase),
    path('orders/<int:id>', get_order)
]
