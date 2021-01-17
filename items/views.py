from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Item


def get_item_dict(item):
    return dict(id=item.id, title=item.title, description=item.description, image=item.image.url, weight=item.weight,
                price=item.price)


@api_view(http_method_names=['GET'])
def item_detail(request, pk):
    try:
        item = Item.objects.get(pk=pk)
        return Response(get_item_dict(item))
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(http_method_names=['GET'])
def items(request):
    items = Item.objects.all()
    return Response([get_item_dict(item) for item in items])