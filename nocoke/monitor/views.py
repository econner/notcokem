from django.http import HttpResponse
from nocoke.monitor.models import Keg, Pour, Pulse
import datetime

def index(request):
    return HttpResponse("Hello World")
    
def flow(request):
    """
    Handle post request from Arduino to add a new pulse.
    """
    freq = request.GET['freq']
    cur_keg = Keg.objects.current_keg()
    
    pour_threshold = datetime.datetime.now() - datetime.timedelta(seconds=5)
    pulses = Pulse.objects.filter(created_at__gt=pour_threshold).order_by("-created_at")
    if pulses:
        prev_pulse = pulses[0]
        cur_pour = prev_pulse.pour
    else:
        cur_pour = Pour(size=0, keg=cur_keg)
    
    # freq / 7.5 gives flow rate in L / min
    # 1 L/min = 0.5635 oz / s
    rate = (float(freq) / 7.5) * 0.5635
    cur_pour.size += rate
    cur_pour.save()
    
    cur_pulse = Pulse(frequency=freq, pour=cur_pour)
    cur_pulse.save()
    
    return HttpResponse("Nothing to see here")
        