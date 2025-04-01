from .models import Category

def categories_context(request):
    """Disponibiliza todas as categorias para os templates"""
    return {'categories': Category.objects.all()}