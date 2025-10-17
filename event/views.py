from django.shortcuts import render,redirect
from django.http import HttpResponse
from event.forms import EventModelForm,CategoryForm,ParticipantForm
from event.models import Participant,Event,Category
from django.contrib import messages
from django.db.models import Q,Count
from datetime import datetime,date
from django.utils.timezone import localdate
from users.views import is_organizer,is_admin
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
# Create your views here.

User = get_user_model()

def is_users(user):
    return user.groups.filter(name = 'User').exists()

def home_page(request):
    events = Event.objects.prefetch_related('rspv').order_by('date')[:6]
    context = {"events": events}
    return render(request,"home_page.html", context)

def participant_page(request):
    return render(request,"grids/participant_page.html")

def show_event(request):
    return HttpResponse("Events")

@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect('manager-dashboard')
    elif is_users(request.user):
        return redirect("user-dashboard")
    elif is_admin(request.user):
        return redirect("admin-dashboard")
    
    return redirect('no-permission')


@user_passes_test(is_organizer,login_url="no-permission")
def organizer_dashboard(request):
    events = Event.objects.prefetch_related('participants', 'rspv').all()
    for e in events:
        event = e
    return render(request,"dashboard/organizer_dashboard.html",{'events':events,'event':event})


@user_passes_test(is_users,login_url="no-permission")
def user_dashboard(request):
    type = request.GET.get('type','all')

    cr_day = datetime.now().date()
    events = Event.objects.prefetch_related('participants', 'rspv').all()
    participant = User.objects.all()
    print(participant)

    search_name= request.GET.get('name')
    search_location =request.GET.get('location')

    if search_name:
        events = events.filter(name__icontains = search_name)
    if search_location:
        events = events.filter(name__icontains = search_location)

    
    upcoming_events_qs = events.filter(date__gte=cr_day)
    past_events_qs = events.filter(date__lt=cr_day)


    if type =="participants":
        result = participant
    elif type == "total_events":
        result = events
    elif type == "upcoming":
        result = upcoming_events_qs
    elif type == "past":
        result = past_events_qs
    else:
        # default to showing all events if type is 'all' or unknown
        result = events

    

    counts ={
        'upcoming' : upcoming_events_qs.count(),
        'past' : past_events_qs.count(),
        'total_participant' : Participant.objects.values('id').distinct().count(),
        'total_event' : events.count()
    }
    
    context = {
        'counts' : counts,
        'result' : result,
        'type':type,
        'search_name' : search_name,
        'search_location' : search_location,
        'role' : 'user'

    }
    print(result)
    print(counts)

    return render(request,"dashboard/event_dashboard.html",context)

    

# @user_passes_test(is_admin,login_url="no-permission")
# def create_event(request):
#     event_form = EventModelForm()

#     if request.method == "POST":
#         event_form = EventModelForm(request.POST,request.FILES)
#         print("inside post")
#         if event_form.is_valid():
#             event_form.save()
        
#             if messages.success:
#                 messages.success(request,"Event Created Successfully")
#                 return redirect("create-event")
#             elif messages.error:
#                 messages.error(request,"something wrong")
#                 return redirect("create-event")
        
#     context = {"event_form":event_form}
#     return render(request,"event_form.html",context)

def is_admin_or_organizer(user):
    return is_admin(user) or is_organizer(user)



class CreateEventView(UserPassesTestMixin,CreateView):
    model = Event
    form_class = EventModelForm
    template_name = "event_form.html"
    success_url = reverse_lazy("create-event")

    def test_func(self):
        return is_admin(self.request.user) or is_organizer(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to create events.")
        return redirect("no-permission") 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_form"] = EventModelForm()
        return context
    
    def post(self, request, *args, **kwargs):
        event_form = EventModelForm(request.POST,request.FILES)
        print("inside post")
        if event_form.is_valid():
            event_form.save()
        
            if messages.success:
                messages.success(request,"Event Created Successfully")
                return redirect("create-event")
            elif messages.error:
                messages.error(request,"something wrong")
                return redirect("create-event")
    
    
    



# @user_passes_test(is_admin,login_url="no-permission")
# def update_event(request,id):
#     event = Event.objects.get(id = id)
#     event_form = EventModelForm(instance = event)


#     if request.method == "POST":
#         event_form = EventModelForm(request.POST,instance = event)

#         if event_form.is_valid():
            
#             event_form.save()

#             if messages.success:
#                 messages.success(request,"Event updated Successfully")
#                 return redirect("update-event")
#             elif messages.error:
#                 messages.error(request,"something wrong")
#                 return redirect("update-event")
        
#     context = {"event_form":event_form}
#     return render(request,"event_form.html",context)



class UpdateEventView(UpdateView):
    model = Event
    form_class = EventModelForm
    context_object_name = "event"
    pk_url_kwarg = "id"
    template_name = "event_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_form"] = self.get_form() 
        print("ob",self.get_object())
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print("ob",self.object)
        event_form = EventModelForm(request.POST,instance = self.object)

        if event_form.is_valid():
            
            event_form.save()

            if messages.success:
                messages.success(request,"Event updated Successfully")
                return redirect("update-event",id=event_form.id)
            elif messages.error:
                messages.error(request,"something wrong")
                return redirect("update-event")



# @user_passes_test(is_organizer,login_url="no-permission")
# def delete_event(request,id):
#     if request.method == "POST":
#         event = Event.objects.get(id=id)
#         event.delete()
#         messages.success(request,"Event Delete Successfully")
#         return redirect('organizer-dashboard')
#     else:
#         messages.error(request,"something went wrong")
#         return redirect('organizer-dashboard')


class DeleteEventView(DeleteView):
    model = Event
    pk_url_kwarg = "id"
    success_url = reverse_lazy("dashboard")

    def delete(self, request, *args, **kwargs):
        messages.success(request,"Event Delete Successfully")
        return super().delete(request, *args, **kwargs)


@user_passes_test(is_admin_or_organizer,login_url="no-permission")
def create_category(request):
    category_form = CategoryForm()

    if request.method =="POST":
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()

            if messages.success:
                messages.success(request,"Category Created Successfully")
                return redirect("create-category")
            elif messages.error:
                messages.error(request,"something wrong")
                return redirect("create-category")
    context = {"category_form":category_form}
    return render(request,"category_form.html",context)



class CreateCategoryEvent(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "category_form.html"
    success_url = reverse_lazy("create-category")

    def post(self, request, *args, **kwargs):
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()

            if messages.success:
                messages.success(request,"Category Created Successfully")
                return redirect("create-category")
            elif messages.error:
                messages.error(request,"something wrong")
                return redirect("create-category")





# def create_participant(request):
#     participant_form = ParticipantForm()

#     if request.method == "POST":
#         participant_form = ParticipantForm(request.POST)
#         print("inside post")

#         if participant_form.is_valid():
#             participant_form.save()

#             if messages.success:
#                 messages.success(request,"Event Created Successfully")
#                 return redirect("create-participant")
#             elif messages.error:
#                 messages.error(request,"something wrong")
#                 return redirect("create-participant")


#     context = {"participant_form":participant_form}
#     return render(request,"create_participant.html",context)

@login_required
def event_detials(request,event_id):
    event = Event.objects.get(id = event_id)
    return render(request,"event_detials.html",{"event":event})



def dashboard(request):
    if is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_users(request.user):
        return redirect('event-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    return redirect('no-permission')     



@login_required
def rspv_event(request,event_id):
    event = Event.objects.get(id = event_id)

    if request.user in event.rspv.all():
        messages.success(request,"you have already rspv to this event")
    else:
        event.rspv.add(request.user)
        event.save()
        
        subject = f"Rspv conformation for {event.name}"
        message = f"your successfully RSPV for {event.name}"
        recipient_list = [request.user.email]

        send_mail(subject,message,settings.EMAIL_HOST_USER,recipient_list)
    
    return redirect("event-dashboard")


from django.shortcuts import render


def about_us(request):
    context = {
        'company_name': 'EventHook',
        'tagline': 'We build delightful stuff',
        'description': (
        "We are a passionate team committed to delivering quality "
        "products and creating great user experiences."
        ),
        'year_founded': 2020,
        'team': [
        {
        'name': 'Mahfuz',
        'role': 'Founder & CEO',
        'bio': 'Visionary leader and tech enthusiast.',
        'photo': 'https://via.placeholder.com/100',
        'linkedin': 'https://linkedin.com',
        'twitter': 'https://twitter.com',
        },
        {
        'name': 'Jahidul',
        'role': 'Designer',
        'bio': 'Creates beautiful and accessible designs.',
        'photo': 'https://via.placeholder.com/100',
        'linkedin': '',
        'twitter': 'https://twitter.com',
        },
        {
        'name': 'Sabbir',
        'role': 'Developer',
        'bio': 'Loves clean code and solving problems.',
        'photo': 'https://via.placeholder.com/100',
        'linkedin': 'https://linkedin.com',
        'twitter': '',
        }
        ],
        'quick_facts': {
        'projects': '100+',
        'customers': '80+',
        'location': 'Remote / Dhaka'
        },
        'contact': {
        'email': 'Eventhook.com',
        'phone': '+8801518962201'
        }
    }
    return render(request, 'about_us.html', context)


def contact(request):
    return render(request, 'contact.html')