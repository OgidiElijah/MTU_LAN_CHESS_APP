from django.conf import settings

def mtu_chess_config(request):
    """Expose MTU_CHESS_CONFIG to all templates as 'MTU_CHESS_CONFIG'."""
    return {'MTU_CHESS_CONFIG': getattr(settings, 'MTU_CHESS_CONFIG', {})}