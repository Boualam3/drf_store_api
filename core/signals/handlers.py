from django.dispatch import receiver
from store.signals import order_created


# here below  we apply customize signal handlers create by us so learn ore about signals and custom handlers signals

@receiver(order_created)
def on_order_created(sender, **kwargs):
    print(
        f"==================================\n{kwargs['order']}\n================================")
