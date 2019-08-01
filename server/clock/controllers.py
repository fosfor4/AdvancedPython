import time
from protocol import make_response
from decorators import logged

@logged
def send_time(request):
    timestr = 'Server time: ' + time.ctime(time.time())
    return make_response(request, 200, timestr)
