from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('products', views.ProductViewSet, basename='products')

router.register('collections', views.CollectionViewSet)

router.register('carts', views.CartViewSet, basename='carts')

router.register('customers', views.CustomerViewSet, basename='customers')

router.register('orders', views.OrderViewSet, basename='orders')

# routers.NestedDefaultRouter(parent router, 'parent', lookup='products')
products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')

carts_router = routers.NestedDefaultRouter(
    router, 'carts', lookup='cart')

# register child (nested router)
products_router.register(
    'reviews', views.ReviewViewSet,
    basename='product-reviews'
)

products_router.register(
    'images', views.ProductImageViewSet,  basename='product-images'
)

carts_router.register(
    'items', views.ItemViewSet,
    basename='cart-items'
)
# URLConf


urlpatterns = router.urls + products_router.urls + carts_router.urls


# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(),
#          name='collection-detail'),

# ]
