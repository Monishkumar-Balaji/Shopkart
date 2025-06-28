from .models import Product

def trending_products(request):
    return {
        'trending_products': Product.objects.filter(trending=True, status=0).order_by('?')[:5]
    }