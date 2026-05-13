from django import forms 
from event.models import Event,Category,Participant


class EventForm(forms.Form):
    name = forms.CharField(max_length=100, label="Event Name")
    description = forms.CharField(widget=forms.Textarea,label = "Event Description")
    date = forms.DateField(widget=forms.SelectDateWidget, label="Date")
    time = forms.TimeField(widget=forms.TimeInput, label="Time")
    location = forms.CharField(widget=forms.Textarea, max_length=80,label="Location")
    category = forms.ChoiceField(widget=forms.CheckboxSelectMultiple, choices=[], required=True)


    def __init__(self,*args, **kwargs):
        categories = kwargs.pop("categories",[])
        super().__init__(*args,**kwargs)
        self.fields['category'].choices = [(cat.id, cat.name) for cat in categories]




class StyledFormMixin:
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widget()

    '''Mixing to apply to form field'''
    default_classes = "w-full"

    def get_placeholder(self, field_name, field):
        label = field.label or field_name.replace("_", " ")
        return f"Enter {label.lower()}"

    def apply_styled_widget(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder': self.get_placeholder(field_name, field)
                })
            elif isinstance(field.widget, forms.NumberInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': self.get_placeholder(field_name, field),
                    'min': 1
                })
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder': self.get_placeholder(field_name, field)
                })
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': self.get_placeholder(field_name, field)
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder': self.get_placeholder(field_name, field),
                    'rows':5
                })
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({
                    'class': self.default_classes
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    'class': self.default_classes
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2 rounded-xl bg-white/10 p-4"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })



class CategoryForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']

        labels = {
            'name':"Category Name"
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widget()


class EventModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Event

        fields =['name','description','date','time','location','capacity','category','asset']
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date'}),
            'time' : forms.TimeInput(attrs={'type':'time'}),
            # Use a nice single-select dropdown for category
            'category': forms.Select,
        }

        labels = {
            'name':"Event Name"
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widget()


class ParticipantForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Participant
        
        
        fields = ['name','email','event']

        widgets ={
            'event' : forms.CheckboxSelectMultiple
        }

        labels = {
            'name':"Participant Name"
        }
        
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widget()
