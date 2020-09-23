

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from .forms import roomForm,examForm
from .models import Room, Events,Exam,Threshold,Assignment,SESSIONS,masterSchedule,Weakdays,EXAMSCH,SEATALLOC,Holiday,Session
from datetime import date, timedelta,datetime
import pyodbc
from django.db.models import Sum

@login_required(login_url="/accounts/login/")
def index(request):
    seatAlloc = SEATALLOC.objects.all()
    seatCount = seatAlloc.count
    examSch = EXAMSCH.objects.all()
    filled=0
    capacity=0;
    for e in examSch:
        capacity = capacity + e.CAPACITY
        filled = filled + e.FILLED
    if examSch.count() != 0:
        overall =int(100 - (filled/capacity))
    else:
        overall = 0

    getStartTime("A0900")
    getEndTime("A0900")


    return render(request, "schedule/index.html",{'seatAlloc':seatAlloc, 'examSch':examSch,'seatCount':seatCount,'overall':overall})

def getStartTime(str):
    code = str[0]
    time = str[1:3]+":"+str[3:5]
    startTime = datetime.strptime(time,"%H:%M")
    return startTime.time()


def getEndTime(str):
    code = str[0]
    time = str[1:3]+":"+str[3:5]
    startTime = datetime.strptime(time, "%H:%M")
    sCode=Session.objects.get(code=code)
    endTime = startTime + timedelta(minutes=sCode.time)
    # strTime=endTime.strftime("%H:%M")
    # end = datetime.strptime(strTime,"%H:%M")
    return endTime.time()


def createMasterSchedule(request):

    # if request.method == 'POST':
    #     dates = request.POST.get('dates')
    #     room = request.POST.get('room')
    #     r = Room.objects.get(title=room)
    #     examList = request.POST.getlist('examList')
    #     exam = Exam.objects.filter(title__in=examList)
    #
    #     for e in exam:
    #         assignment = Assignment()
    #         assignment.room = r
    #         assignment.exam = e
    #         assignment.save()

    Exams = Exam.objects.all()
    Rooms = Room.objects.all()
    return render(request, 'schedule/masterSchedule.html',{'Exams':Exams, 'Rooms':Rooms})

def updateMasterSchedule(request,id):
    schedule = masterSchedule.objects.get(id=id)

    if request.method == 'POST':

        roomid = request.POST.get('room')
        seats = request.POST.get('seats')
        room = getRoomDetail(roomid)
        if room.SEATS >= int(seats):
            #creating master Schedule
            master = masterSchedule.objects.get(id=id)
            master.exam = request.POST.get('exam')
            master.examMode = request.POST.get('examMode')
            master.examMedium = request.POST.get('examMed')
            master.seats = request.POST.get('seats')
            master.room = request.POST.get('room')
            master.subcode = request.POST.get('subcode')
            master.session = request.POST.get('session')
            master.regSchedule = request.POST.get('regSchedule')
            if request.POST.get('resSchedule'):
                master.resSchedule = request.POST.get('resSchedule')
            if request.POST.get('cerSchedule'):
                master.cerSchedule = request.POST.get('cerSchedule')
            master.componyId = request.POST.get('componyId')
            exDays=request.POST.getlist('examSchedule[]')
            # daysList = Weakdays.objects.filter(id__in=exDays)
            master.examSchedule.remove(*master.examSchedule.all())
            master.save()

            for r in exDays:
            #     day = Weakdays.objects.get(id=r)
            #     master.examSchedule.add(day)
            #     master.save()
                master.examSchedule.add(r)
                master.save()
            companyid = getCompanies(request)
            subcodes = getExamModules(request)
            exam = getExams(request)
            room = getRooms(request)
            session = getSessions(request)
            return roomTable(request)
        else:
            companyid = getCompanies(request)
            subcodes = getExamModules(request)
            exam = getExams(request)
            room = getRooms(request)
            session = getSessions(request)
            msg = "Room Capacity Exceeds"
            return render(request, 'schedule/updateMasterSchedule.html'
                          , {'exam': exam, 'room': room, 'session': session,'subcodes':subcodes,'companyid':companyid,'schedule':schedule,'msg':msg}
                          )
    companyid = getCompanies(request)
    subcodes = getExamModules(request)
    exam = getExams(request)
    room = getRooms(request)
    session = getSessions(request)
    return render(request, 'schedule/updateMasterSchedule.html'
                  , {'exam':exam , 'room':room , 'session':session,'subcodes':subcodes,'companyid':companyid,'schedule':schedule}
                  )

def createRoom(request):

    if request.method == 'POST':
        form = roomForm(request.POST)

        if form.is_valid():
            # Room = form.save(commit=False)
            # Room.save()

            return index(request)

    else:
        form = roomForm()
    return render(request, 'schedule/createRoom.html', {'form': form})

def createAdhoc(request):
    if request.method == 'POST':
        print("hello adhoc")
        date = request.POST.get('date')
        if not Holiday.objects.filter(date=date):
            exam = request.POST.get('exam')
            if request.POST.get('certificateDate'):
                certificateDate = datetime.strptime(request.POST.get('certificateDate'),"%Y-%m-%d")
                CERTDATE = certificateDate.strftime('%Y%m%d')
            else:
                CERTDATE=0
            if request.POST.get('resultDate'):
                resultDate = datetime.strptime(request.POST.get('resultDate'),"%Y-%m-%d")
                RESULTDATE = resultDate.strftime('%Y%m%d')
            else:
                RESULTDATE=0

            registrationDate = datetime.strptime(request.POST.get('registrationDate'),"%Y-%m-%d")
            examDate = datetime.strptime(date, "%Y-%m-%d")
            REGDATE = registrationDate.strftime('%Y%m%d')
            componyId = request.POST.get('componyId')
            subcode = request.POST.get('subcode')
            examMedium = request.POST.get('examMedium')
            examMode = request.POST.get('examMode')
            room = request.POST.get('room')
            ROOM=getRoomDetail(room)
            seats = request.POST.get('seats')
            sessionId = request.POST.get('session')
            session=getSessionDetail(sessionId)
            EXAMDATE = examDate.strftime('%Y%m%d')
            # startTime = datetime.strptime(session.STARTTIME, '%H:%M %p').time()
            # endTime = datetime.strptime(session.ENDTIME, '%H:%M %p').time()
            startdatetime = datetime.combine(examDate, getStartTime(sessionId))
            enddatetime = datetime.combine(examDate, getEndTime(sessionId))
            if not EXAMSCH.objects.filter(EXAMDATE=EXAMDATE,SESSIONID=sessionId,ROOMID=room):
                FILLED = seats
                examSch = EXAMSCH(
                    EXAMCODE=exam, EXAMMEDIUM=examMedium, EXAMMODE=examMode, EXAMDATE=EXAMDATE
                    , REGDATE=REGDATE, RESULTDATE=RESULTDATE, CERTDATE=CERTDATE, SESSIONID=sessionId, VENUEID="SCI"
                    , ROOMID=room, CAPACITY=ROOM.SEATS, FILLED=FILLED, SUBCODE=subcode, SEATNO=0
                )
                examSch.save()
                seatAlloc = SEATALLOC()
                seatAlloc.EXAMCODE = exam
                seatAlloc.SUBCODE = subcode
                seatAlloc.EXAMMEDIUM = examMedium
                seatAlloc.EXAMMODE = examMode
                seatAlloc.SESSIONID = session
                seatAlloc.COMPANYID = componyId
                seatAlloc.REGDATE = REGDATE
                seatAlloc.SEATS = seats
                seatAlloc.FILLED = 0
                seatAlloc.VENUEID = "SCI"
                seatAlloc.ROOMID = room
                seatAlloc.save()

                event = Events(name=str(exam), start=startdatetime, end=enddatetime, seatAlloc=seatAlloc,
                               examSch=examSch)
                event.save()

                if request.POST.get('resultDate'):
                    event = Events(name=str(exam + " Result"), start=resultDate, end=resultDate,
                                   seatAlloc=seatAlloc, examSch=examSch)
                    event.save()
                if request.POST.get('certificateDate'):
                    event = Events(name=str(exam + " Certificates"), start=certificateDate,
                                   end=certificateDate, seatAlloc=seatAlloc, examSch=examSch)
                    event.save()

                event = Events(name=str(exam + " Registraion Ends"), start=registrationDate,
                               end=registrationDate, seatAlloc=seatAlloc, examSch=examSch)
                event.save()
        else:
            print("no Space")

    return calendar(request)












def printForm(request):
    for key, value in request.POST.items():
        print('Key: %s' % (key))
        print('Value %s' % (value))

def findnextweekday(date,d):
    date += timedelta(days=d)
    if date.weekday() == 6:
        date += timedelta(days=1)
    if date.weekday() == 5:
        date += timedelta(days=2)
    return date
def findpreviosweekday(date,d):
    date -= timedelta(days=d)
    if date.weekday() == 6:
        date -= timedelta(days=1)
    if date.weekday() == 5:
        date -= timedelta(days=2)
    return date

def createExam(request):
    if request.method == 'POST':
        form = examForm(request.POST)

        if form.is_valid():
            # Exam = form.save(commit=False)
            # Exam.save()
            # form.save_m2m()
            return index(request)

    else:
        form = examForm()
    return render(request, 'schedule/createExam.html', {'form': form})

def roomTable(request):
    master = masterSchedule.objects.all()

    return render(request,'schedule/room-table.html',{'master': master})

def createSchedule(request):
    if request.method == 'POST':
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        sdate = datetime.strptime(startDate, '%Y-%m-%d')  # start date
        edate = datetime.strptime(endDate, '%Y-%m-%d')  # end date
        delta = edate - sdate  # as timedelta
        masters = masterSchedule.objects.all()
        for m in masters:
            print(m.exam)
            session = getSessionDetail(m.session)
            for i in range(delta.days + 1):
                day = sdate + timedelta(days=i)
                print(day.strftime('%Y-%m-%d'))
                d=day.strftime('%A')
                if not Holiday.objects.filter(date=day.strftime('%Y-%m-%d')):
                    if d in m.examSchedule.values_list('name',flat=True):
                        # startTime=datetime.strptime(session.STARTTIME, '%H:%M %p').time()
                        # endTime=datetime.strptime(session.ENDTIME, '%H:%M %p').time()
                        # startTime=datetime.strptime(getStartTime(m.session), '%H:%M %p').time()
                        # endTime=datetime.strptime(getEndTime(m.session), '%H:%M %p').time()
                        startdatetime = datetime.combine(day, getStartTime(m.session))
                        enddatetime = datetime.combine(day , getEndTime(m.session))
                        print(startdatetime)
                        print(enddatetime)
                        rd= findpreviosweekday(startdatetime,m.regSchedule)
                        if m.resSchedule:
                            rsd = findnextweekday(startdatetime, m.resSchedule)
                            RESULTDATE = rsd.strftime('%Y%m%d')
                        else:
                            RESULTDATE = 0
                        if m.cerSchedule:
                            cerd = findnextweekday(startdatetime, m.cerSchedule)
                            CERTDATE = cerd.strftime('%Y%m%d')
                        else:
                            CERTDATE = 0

                        REGDATE = rd.strftime('%Y%m%d')
                        EXAMDATE = day.strftime('%Y%m%d')
                        ROOM = getRoomDetail(m.room)
                        if not EXAMSCH.objects.filter(EXAMDATE=EXAMDATE,SESSIONID=m.session,ROOMID=m.room):
                            FILLED = m.seats
                            examSch = EXAMSCH(
                                EXAMCODE=m.exam,EXAMMEDIUM=m.examMedium,EXAMMODE=m.examMode,EXAMDATE=EXAMDATE
                                ,REGDATE=REGDATE,RESULTDATE=RESULTDATE,CERTDATE=CERTDATE,SESSIONID=m.session,VENUEID="SCI"
                                ,ROOMID=m.room,CAPACITY=ROOM.SEATS,FILLED=FILLED,SUBCODE=m.subcode,SEATNO=0
                                              )
                            examSch.save()
                            seatAlloc = SEATALLOC()
                            seatAlloc.EXAMCODE=m.exam
                            seatAlloc.SUBCODE = m.subcode
                            seatAlloc.EXAMMEDIUM = m.examMedium
                            seatAlloc.EXAMMODE = m.examMode
                            seatAlloc.SESSIONID = m.session
                            seatAlloc.COMPANYID= m.componyId
                            seatAlloc.REGDATE = REGDATE
                            seatAlloc.SEATS=m.seats
                            seatAlloc.FILLED=0
                            seatAlloc.VENUEID = "SCI"
                            seatAlloc.ROOMID = m.room
                            seatAlloc.save()

                            event = Events(name=str(m.exam), start=startdatetime, end=enddatetime, seatAlloc=seatAlloc,
                                           examSch=examSch)
                            event.save()
                            if m.resSchedule:
                                resultEvent = findnextweekday(startdatetime, m.resSchedule)
                                event = Events(name=str(m.exam + " Result"), start=resultEvent, end=resultEvent,
                                               seatAlloc=seatAlloc, examSch=examSch)
                                event.save()
                            if m.cerSchedule:
                                certificateEvent = findnextweekday(startdatetime, m.cerSchedule)
                                event = Events(name=str(m.exam + " Certificates"), start=certificateEvent,
                                               end=certificateEvent, seatAlloc=seatAlloc, examSch=examSch)
                                event.save()
                            registrationEvent = findpreviosweekday(startdatetime, m.regSchedule)
                            event = Events(name=str(m.exam + " Registraion Ends"), start=registrationEvent,
                                           end=registrationEvent, seatAlloc=seatAlloc, examSch=examSch)
                            event.save()
                        else:
                            pexamSch = EXAMSCH.objects.filter(EXAMDATE=EXAMDATE, SESSIONID=m.session, ROOMID=m.room).order_by('-RECID')[0]
                            available = pexamSch.CAPACITY - pexamSch.FILLED
                            print(available)
                            if available >= m.seats :
                                pexamSch.FILLED = pexamSch.FILLED + m.seats
                                pexamSch.save()
                                FILLED = pexamSch.FILLED
                                examSch = EXAMSCH(
                                    EXAMCODE=m.exam, EXAMMEDIUM=m.examMedium, EXAMMODE=m.examMode, EXAMDATE=EXAMDATE
                                    , REGDATE=REGDATE, RESULTDATE=RESULTDATE, CERTDATE=CERTDATE, SESSIONID=m.session,
                                    VENUEID="SCI"
                                    , ROOMID=m.room, CAPACITY=ROOM.SEATS, FILLED=FILLED, SUBCODE=m.subcode, SEATNO=0
                                )
                                examSch.save()
                                seatAlloc = SEATALLOC()
                                seatAlloc.EXAMCODE = m.exam
                                seatAlloc.SUBCODE = m.subcode
                                seatAlloc.EXAMMEDIUM = m.examMedium
                                seatAlloc.EXAMMODE = m.examMode
                                seatAlloc.SESSIONID = m.session
                                seatAlloc.COMPANYID = m.componyId
                                seatAlloc.REGDATE = REGDATE
                                seatAlloc.SEATS = m.seats
                                seatAlloc.FILLED = 0
                                seatAlloc.VENUEID = "SCI"
                                seatAlloc.ROOMID = m.room
                                seatAlloc.save()

                                event = Events(name=str(m.exam), start=startdatetime, end=enddatetime, seatAlloc=seatAlloc,
                                               examSch=examSch)
                                event.save()
                                if m.resSchedule:
                                    resultEvent = findnextweekday(startdatetime, m.resSchedule)
                                    event = Events(name=str(m.exam + " Result"), start=resultEvent, end=resultEvent,
                                                   seatAlloc=seatAlloc, examSch=examSch)
                                    event.save()
                                if m.cerSchedule:
                                    certificateEvent = findnextweekday(startdatetime, m.cerSchedule)
                                    event = Events(name=str(m.exam + " Certificates"), start=certificateEvent,
                                                   end=certificateEvent, seatAlloc=seatAlloc, examSch=examSch)
                                    event.save()
                                registrationEvent = findpreviosweekday(startdatetime, m.regSchedule)
                                event = Events(name=str(m.exam + " Registraion Ends"), start=registrationEvent,
                                               end=registrationEvent, seatAlloc=seatAlloc, examSch=examSch)
                                event.save()
                            else:
                                print("No Space")
                else:
                    print("holiday")
        return render(request, 'schedule/schedule.html')
    return render(request,'schedule/createSchedule.html')


def schedule(request):
    return render(request, 'schedule/schedule.html')

def calendar(request):
    companyid = getCompanies(request)
    subcodes = getExamModules(request)
    exam = getExams(request)
    room = getRooms(request)
    session = getSessions(request)
    events = Events.objects.all()
    context = {
        'exam': exam,
        'room': room,
        'session': session,
        'subcodes': subcodes,
        'companyid': companyid,
        'events':events
    }
    return render(request,'schedule/calendar.html',context)

def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)


def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)


def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)

def SESSIONSview(request):
    conn=pyodbc.connect('Driver={sql server};'
                        'Server=sciuat.database.windows.net;'
                        'Database=sciuat;'
                        'UID=devteam;'
                        'PWD=Temp12345678;'
                        )
    cursor=conn.cursor()
    cursor.execute("select * from SESSIONS")
    result=cursor.fetchall()
    return render(request,'schedule/test.html',{'SESSIONS':result})

def getExams(request):
    conn=pyodbc.connect('Driver={sql server};'
                        'Server=sciuat.database.windows.net;'
                        'Database=sciuat;'
                        'UID=devteam;'
                        'PWD=Temp12345678;'
                        )
    cursor=conn.cursor()
    cursor.execute("select * from Exams")
    result=cursor.fetchall()
    return result

def getRooms(request):
    conn=pyodbc.connect('Driver={sql server};'
                        'Server=sciuat.database.windows.net;'
                        'Database=sciuat;'
                        'UID=devteam;'
                        'PWD=Temp12345678;'
                        )
    cursor=conn.cursor()
    cursor.execute("select * from ROOMS")
    result=cursor.fetchall()
    return result

def getSessions(request):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=sciuat.database.windows.net;'
                          'Database=sciuat;'
                          'UID=devteam;'
                          'PWD=Temp12345678;'
                          )
    cursor = conn.cursor()
    cursor.execute("select * from SESSIONS")
    result = cursor.fetchall()
    return result

def getSessionDetail(id):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=sciuat.database.windows.net;'
                          'Database=sciuat;'
                          'UID=devteam;'
                          'PWD=Temp12345678;'
                          )
    cursor = conn.cursor()
    cursor.execute("select * from SESSIONS where SESSIONID= '"+ id +"'")
    result = cursor.fetchone()
    # print(result.SESSIONID)
    return result

def getRoomDetail(id):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=sciuat.database.windows.net;'
                          'Database=sciuat;'
                          'UID=devteam;'
                          'PWD=Temp12345678;'
                          )
    cursor = conn.cursor()
    cursor.execute("select * from ROOMS where ROOMID= '"+ id +"'")
    result = cursor.fetchone()
    # print(result.SESSIONID)
    return result

def getExamsch(request):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=sciuat.database.windows.net;'
                          'Database=sciuat;'
                          'UID=devteam;'
                          'PWD=Temp12345678;'
                          )
    cursor = conn.cursor()
    cursor.execute("select * from SESSIONS")
    result = cursor.fetchall()
    return result

def getExamModules(request):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=sciuat.database.windows.net;'
                          'Database=sciuat;'
                          'UID=devteam;'
                          'PWD=Temp12345678;'
                          )
    cursor = conn.cursor()
    cursor.execute("select * from Exam_Modules")
    result = cursor.fetchall()
    return result

def getCompanies(request):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=sciuat.database.windows.net;'
                          'Database=sciuat;'
                          'UID=devteam;'
                          'PWD=Temp12345678;'
                          )
    cursor = conn.cursor()
    cursor.execute("select * from COMPANIES")
    result = cursor.fetchall()
    return result



def createsExam(request):
    if request.method == 'POST':

        roomid = request.POST.get('room')
        seats = request.POST.get('seats')
        room = getRoomDetail(roomid)
        if room.SEATS >= int(seats):
            #creating master Schedule
            master = masterSchedule()
            master.exam = request.POST.get('exam')
            master.examMode = request.POST.get('examMode')
            master.examMedium = request.POST.get('examMed')
            master.seats = request.POST.get('seats')
            master.room = request.POST.get('room')
            master.subcode = request.POST.get('subcode')
            master.session = request.POST.get('session')
            master.regSchedule = request.POST.get('regSchedule')
            if request.POST.get('resSchedule'):
                master.resSchedule = request.POST.get('resSchedule')
            if request.POST.get('cerSchedule'):
                master.cerSchedule = request.POST.get('cerSchedule')
            master.componyId = request.POST.get('componyId')
            exDays=request.POST.getlist('examSchedule[]')
            # daysList = Weakdays.objects.filter(id__in=exDays)
            master.save()

            for r in exDays:
            #     day = Weakdays.objects.get(id=r)
            #     master.examSchedule.add(day)
            #     master.save()
                master.examSchedule.add(r)
                master.save()
            companyid = getCompanies(request)
            subcodes = getExamModules(request)
            exam = getExams(request)
            room = getRooms(request)
            session = getSessions(request)
            success = "Master Schedule has been created successfully"
            return render(request, 'schedule/sExam.html'
                          , {'exam': exam, 'room': room, 'session': session,'subcodes':subcodes,'companyid':companyid,'success':success}
                          )
        else:
            companyid = getCompanies(request)
            subcodes = getExamModules(request)
            exam = getExams(request)
            room = getRooms(request)
            session = getSessions(request)
            msg = "Room Capacity Exceeds"
            return render(request, 'schedule/sExam.html'
                          , {'exam': exam, 'room': room, 'session': session,'subcodes':subcodes,'companyid':companyid,'msg':msg}
                          )
    companyid = getCompanies(request)
    subcodes = getExamModules(request)
    exam = getExams(request)
    room = getRooms(request)
    session = getSessions(request)
    return render(request, 'schedule/sExam.html'
                  , {'exam':exam , 'room':room , 'session':session,'subcodes':subcodes,'companyid':companyid}
                  )

