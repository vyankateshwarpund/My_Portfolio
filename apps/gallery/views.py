from django.views.generic import ListView
from .models import GalleryItem

class GalleryView(ListView):
    model = GalleryItem
    template_name = 'gallery.html'
    context_object_name = 'gallery_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = GalleryItem.CATEGORY_CHOICES
        return context
