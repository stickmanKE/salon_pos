def get_current_salon(request):
    return getattr(request.user, 'salon', None)