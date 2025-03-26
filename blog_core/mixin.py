from django.http import Http404

class DraftDispatchMixin:
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.status != 'published':
            raise Http404("A postagem que você procura não existe ou não está disponível.")
        return super().dispatch(request, *args, **kwargs)
