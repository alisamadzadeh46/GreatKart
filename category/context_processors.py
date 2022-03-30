from .models import Category


def menu_link(request):
    links = Category.objects.all()
    ca = Category.objects.filter(parent=None)[:5]
    return dict(links=links, ca=ca)
