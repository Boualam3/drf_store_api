from django.contrib import admin, messages
from django.db.models import Count, Value, F, CharField, ExpressionWrapper

from django.utils.html import format_html, urlencode
from django.urls import reverse

from .models import Promotion, Collection, Product, Customer, Address, Order, OrderItem, Cart, CartItem, ProductImage

from tags.models import TaggedItem


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img class="thumbnail" src="{instance.image.url}" alt="{instance.image.name}" />')
        return ' '


class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    inlines = [ProductImageInline]
    list_display = [
        'title', 'unit_price',
        'inventory_status',
        'collection_title'
    ]
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    prepopulated_fields = {
        'slug': ['title']
    }
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )

    class Media:
        css = {
            'all': ['store/style.css']
        }


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name',
                    'last_name', 'membership', 'orders']
    list_select_related = ['user']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith',
                     'last_name__istartswith', ]

    def orders(self, customer):

        # reverse('admin:app_model_page')
        url = (reverse('admin:store_customer_changelist')
               + '?'
               + urlencode({
                   'customer__id': str(customer.id)
               }))
        return format_html('<a href="{}">{}</a>', url, f'{customer.orders} Orders')

    def get_queryset(self, request):
        orders_count = ExpressionWrapper(
            Count('order'), output_field=CharField())
        return super().get_queryset(request).annotate(
            orders=orders_count
        )


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = OrderItem
    min_num = 1
    max_num = 10


class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer_order']
    list_select_related = ['customer']

    """
    We can just specify 'customer' on list_display and we got first_name and last_name of customer on order .
    But I use define function to more customize if we need more then first_name and last_name  
    """

    def customer_order(self, order):
        return format_html('<a href="">{}</a>',  f'order_{order.customer.first_name}_{order.customer.last_name}')


class CollectionAdmin(admin.ModelAdmin):
    """ 
     we dont 'product_count' in our Collection Model
     it seen like error but we sepecify  get_queryset function for that , then we add @admin.display...
     for make it sortable

    """
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # reverse('admin:app_model_page')
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({
                   'collection__id': str(collection.id)
               })
               )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


class OrderItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Promotion)
admin.site.register(Address)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
