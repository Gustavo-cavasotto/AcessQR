from usuarios.models import Usuario


class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                # Obtém o objeto usuário completo baseado no usuário autenticado
                user_object = Usuario.objects.get(nome=request.user.username)
                # Adiciona o objeto ao request para uso global
                request.usuario = user_object
            except Usuario.DoesNotExist:
                request.usuario = None
        else:
            request.usuario = None

        response = self.get_response(request)

        return response

    def process_template_response(self, request, response):
        if hasattr(request, 'usuario') and request.usuario is not None:
            response.context_data['usuario'] = request.usuario
        return response
