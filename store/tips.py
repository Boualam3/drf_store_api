from .models import Product
# for improve  the performance

# * Preload related objects
Product.objects.select_related('...')
Product.objects.prefetch_related('...')


# * Load only what you need
Product.objects.only('title')
Product.objects.defer('description')


# * Use values
# with values we get dict
Product.objects.values()
# with values_list we got list
Product.objects.values_list()

# * Count properly
Product.objects.count()
len(Product.objects.all())  # Bad

# * Bulk create/update
# if we want to create or update multiple objects its more efficient to use bulk_create/bulk_update then creating a bunch of objects in loop we send one instruction to create multiple records
Product.objects.bulk_create([])
