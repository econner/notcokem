from django.db import models

class KegManager(models.Manager):
    """
    Custom manager for the Keg model.  
    """
    def current_keg(self):
        keg_qs = self.all().order_by("-created_at")
        if keg_qs:
            return keg_qs[0]
        return None

class Keg(models.Model):
    beer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    size = models.IntegerField(default=0) # size in ounces
    
    objects = KegManager()
    
    def __unicode__(self):
        return "%s" % self.beer
    
class Pour(models.Model):
    keg = models.ForeignKey(Keg)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    size = models.FloatField(default=0)
    
    def __unicode__(self):
        return "%.2foz out of %s at %s" % (self.size, self.keg, self.created_at) 
    
class Pulse(models.Model):
    frequency = models.IntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pour = models.ForeignKey(Pour)
    
    def __unicode__(self):
        return "%d in (%s)" % (self.frequency, self.pour)

