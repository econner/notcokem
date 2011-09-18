from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from nocoke.monitor.models import Keg, Pour, Pulse
from django.db.models import Sum
import datetime

def index(request):
    cur_keg = Keg.objects.current_keg()
    recent_pours = Pour.objects.filter(keg=cur_keg).order_by("-created_at")
    
    total_oz_poured = recent_pours.aggregate(Sum('size'))
    percent_remaining = (cur_keg.size - total_oz_poured['size__sum']) / cur_keg.size
    percent_remaining *= 100
    
    num_pours = len(recent_pours)
    
    return render_to_response(
        "index.html",
        { 
            "recent_pours": recent_pours,
            "percent_remaining": percent_remaining,
            "num_pours": num_pours,
        },
        context_instance = RequestContext(request)
    )
    
def flow(request):
    """
    Handle post request from Arduino to add a new pulse.  We first check
    if any pulses have occurred in the last 5 seconds.  If so, then we assume
    that this pulse belongs to the previous pour and coalesce it into that
    pour.  Otherwise, we assume it is part of a new pour.
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
        