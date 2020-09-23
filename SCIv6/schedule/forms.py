from django.forms import ModelForm
from django import forms
from .models import Exam,Room,Assignment





class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'



class roomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(roomForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['capacity'].widget.attrs.update({'placeholder':'Capacity'})
        self.fields['venueID'].widget.attrs.update({'placeholder': 'Vanue ID'})
        self.fields['roomID'].widget.attrs.update({'placeholder': 'Room ID'})
        self.fields['title'].widget.attrs.update({'placeholder': 'Room'})
        self.fields['reservedfor'].widget.attrs.update({'placeholder': 'Reserved for..'})
        self.fields['invigilator'].widget.attrs.update({'placeholder': 'Invigilator'})


class examForm(ModelForm):


    class Meta:
        model = Exam
        fields = '__all__'
        widgets = {
                   # 'resultSchedule': DateInput(),
                   # 'registrationSchedule': DateInput(),
                   # 'certificateSchedule': DateInput(),
                   'startTime': TimeInput(),
                   'endTime': TimeInput(),
                   'bstartTime': TimeInput(),
                   'bendTime': TimeInput(),
                   }

    def __init__(self, *args, **kwargs):
        super(examForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        # self.fields['recordId'].widget.attrs.update({'placeholder': 'Record ID'})
        self.fields['code'].widget.attrs.update({'placeholder': 'Code'})
        self.fields['mode'].widget.attrs.update({'placeholder': 'Mode'})
        self.fields['medium'].widget.attrs.update({'placeholder': 'Medium'})
        self.fields['sessionId'].widget.attrs.update({'placeholder': 'Session Id'})
        self.fields['componyId'].widget.attrs.update({'placeholder': 'Compony ID'})
        self.fields['registrationSchedule'].widget.attrs.update({'placeholder': 'Days before Exam'})
        self.fields['resultSchedule'].widget.attrs.update({'placeholder': 'Days after Exam'})
        self.fields['assessor'].widget.attrs.update({'placeholder': 'Assessor'})
        self.fields['courseCode'].widget.attrs.update({'placeholder': 'Course code'})
        self.fields['certificateSchedule'].widget.attrs.update({'placeholder': 'Days after Exam'})

        self.fields['title'].widget.attrs.update({'placeholder': 'Title'})
        self.fields['seats'].widget.attrs.update({'placeholder': 'Seats'})
        self.fields['startTime'].widget.attrs.update({'placeholder': 'Start time'})
        self.fields['endTime'].widget.attrs.update({'placeholder': 'End Time'})
        self.fields['bstartTime'].widget.attrs.update({'placeholder': 'Break Start Time'})
        self.fields['bendTime'].widget.attrs.update({'placeholder': 'Break End Time'})




