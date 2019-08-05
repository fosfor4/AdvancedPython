from protocol import make_response
from decorators import logged

@logged
def send_message(request):
    return make_response(request, 200)
