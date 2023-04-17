from django import forms
from .models import Calendar, Event , Edt , Slotedt


class EventForm(forms.ModelForm):

	class Meta:
	    model = Event
	    exclude =  ('type_of_event',)
	    fields =  ('__all__')

	def __init__(self, user, *args, **kwargs):
		super(EventForm, self).__init__(*args, **kwargs)
		self.fields['calendar'] = forms.ModelMultipleChoiceField(queryset=Calendar.objects.filter(user=user),required=False)

class CalendarForm(forms.ModelForm):

    class Meta:
        model = Calendar
        fields =  ('__all__')


class EdtForm(forms.ModelForm):
 
	class Meta:
		model = Edt
		fields =  ('__all__')



class ContentslotForm(forms.ModelForm):
 
	class Meta:
		model = Slotedt
		fields =  ('__all__')


