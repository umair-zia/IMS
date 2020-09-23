from django.db import models
from datetime import datetime
from datetime import date
class Room(models.Model):
    title = models.CharField(max_length=100)
    capacity = models.IntegerField()
    venueID = models.IntegerField()
    roomID = models.IntegerField()
    reservedfor = models.CharField(max_length=100)
    invigilator = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Schedule(models.Model):
    date = models.DateField(default=None)

class Weakdays(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Registration(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Exam(models.Model):
    # recordId = models.IntegerField(default=None)
    code = models.CharField(default=None,max_length=100)
    mode = models.CharField(default=None,max_length=100)
    medium = models.CharField(default=None,max_length=100)
    sessionId = models.IntegerField(default=None)
    componyId = models.IntegerField(default=None)
    registrationSchedule = models.IntegerField(default=None)
    resultSchedule = models.IntegerField(default=None)
    assessor = models.CharField(default=None,max_length=100)
    courseCode = models.CharField(default=None,max_length=100)
    certificateSchedule = models.IntegerField(default=None)
    title = models.CharField(max_length=100)
    examDates = models.ManyToManyField(Weakdays,default=None)
    seats = models.IntegerField()
    startTime=models.TimeField()
    endTime=models.TimeField()
    bstartTime=models.TimeField()
    bendTime=models.TimeField()

    def __str__(self):
        return self.title

class Assignment(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)




class Alert(models.Model):
    title = models.CharField(max_length=100)
    detail = models.CharField(max_length=255)

class Threshold(models.Model):
    available = models.IntegerField()
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)

    def get_percentage(self):
        perc = 100 - round(self.available * 100 / self.room.capacity)
        return perc

class SESSIONS(models.Model):
    STARTTIME = models.CharField(max_length=8)
    ENDTIME = models.CharField(max_length=8)
    SESSIONCODE = models.CharField(max_length=5)

class Session(models.Model):
    code = models.CharField(max_length=1)
    time = models.IntegerField(default=None)

class masterSchedule(models.Model):
    exam = models.CharField(max_length=100)
    examMode = models.CharField(max_length=100)
    examMedium = models.CharField(max_length=100)
    componyId = models.CharField(null=True,max_length=100)
    seats = models.IntegerField()
    room = models.CharField(max_length=100)
    subcode = models.CharField(default="-",max_length=100)
    examSchedule = models.ManyToManyField(Weakdays, blank=True)
    session = models.CharField(max_length=100)
    regSchedule = models.IntegerField(default=None)
    cerSchedule = models.IntegerField(default=None,null=True)
    resSchedule = models.IntegerField(default=None,null=True)
    def __str__(self):
        return self.exam


class EXAMSCH(models.Model):
    RECID = models.AutoField(primary_key=True)
    EXAMCODE = models.CharField(max_length=10)
    EXAMMEDIUM = models.CharField(max_length=1)
    EXAMMODE = models.CharField(max_length=1)
    EXAMDATE = models.IntegerField()
    REGDATE = models.IntegerField()
    RESULTDATE = models.IntegerField()
    CERTDATE = models.IntegerField()
    SESSIONID = models.CharField(max_length=5)
    VENUEID = models.CharField(max_length=5)
    ROOMID = models.CharField(max_length=5)
    CAPACITY = models.IntegerField()
    FILLED = models.IntegerField()
    SUBCODE = models.CharField(max_length=10)
    SEATNO = models.IntegerField()
    INVIGILATOR = models.CharField(max_length=12)
    CREATED = models.CharField(max_length=10)

    def get_percentage(self):
        perc = round(self.FILLED * 100 / self.CAPACITY)
        return perc
    def __str__(self):
        return self.EXAMCODE
    def getDate(self):
        s=str(self.EXAMDATE)
        year=int(s[0:4])
        month = int(s[4:6])
        day = int(s[6:8])
        date = datetime(year=year, month=month, day=day)
        return date.strftime('%Y-%m-%d')


class SEATALLOC(models.Model):
    RECID = models.AutoField(primary_key=True)
    EXAMCODE = models.CharField(max_length=10)
    SUBCODE = models.CharField(max_length=10)
    EXAMMEDIUM = models.CharField(max_length=1)
    EXAMMODE = models.CharField(max_length=1)
    EXAMDATE = models.IntegerField(default=0)
    SESSIONID = models.CharField(max_length=5)
    COMPANYID = models.CharField(max_length=12)
    REGDATE = models.IntegerField(default=0)
    SEATS = models.IntegerField(default=0)
    FILLED = models.IntegerField(default=0)
    VENUEID = models.CharField(max_length=5)
    ROOMID = models.CharField(max_length=5)
    RESERVERDFOR = models.CharField(max_length=1)
    Assessor = models.CharField(max_length=50)
    CourseCode = models.CharField(max_length=12)
    def get_percentage(self):
        perc =100 - round(self.FILLED * 100 / self.SEATS)
        return perc
    def get_percentageAvailable(self):
        perc =100 - round( self.FILLED * 100 / self.SEATS)
        return perc

    def __str__(self):
        return self.EXAMCODE

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    seatAlloc = models.ForeignKey(SEATALLOC, on_delete=models.CASCADE,default=None)
    examSch = models.ForeignKey(EXAMSCH, on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.name

class Holiday(models.Model):
    date = models.DateField(default=None)
    def __str__(self):
        return str(self.date)