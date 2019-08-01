import time
from protocol import make_response

def send_time(request):
    timestr = 'Server time: ' + time.ctime(time.time())
    return make_response(request, 200, timestr)
