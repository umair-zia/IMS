
from django.contrib import admin
from .models import Exam,Room,Assignment,Events,Threshold,Alert,Weakdays,Registration,masterSchedule,EXAMSCH,SEATALLOC,Holiday,Session
# Register your models here.
# admin.site.register(Exam)
# admin.site.register(Room)
# admin.site.register(Assignment)
admin.site.register(Events)
# admin.site.register(Threshold)
admin.site.register(Alert)
admin.site.register(Weakdays)
# admin.site.register(Registration)
admin.site.register(masterSchedule)
admin.site.register(EXAMSCH)
admin.site.register(SEATALLOC)
admin.site.register(Holiday)
admin.site.register(Session)