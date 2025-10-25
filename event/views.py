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
    events = Event.objects.order_by('date')[:6]
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
    events = Event.objects.prefetch_related('participants').all()
    return render(request,"dashboard/organizer_dashboard.html",{'events':events})


@user_passes_test(is_users,login_url="no-permission")
def user_dashboard(request):
    type = request.GET.get('type','all')

    cr_day = datetime.now().date()
    events = Event.objects.prefetch_related('participants').all()
    participant = User.objects.all()
    print(participant)

    search_name= request.GET.get('name')
    search_location =request.GET.get('location')

    # Debug: Print search parameters
    print(f"Search name: {search_name}")
    print(f"Search location: {search_location}")
    print(f"Type: {type}")

    # Apply search filters
    if search_name:
        events = events.filter(name__icontains = search_name)
        print(f"Applied name filter. Events count: {events.count()}")
    if search_location:
        events = events.filter(location__icontains = search_location)
        print(f"Applied location filter. Events count: {events.count()}")

    # Calculate upcoming and past events from the filtered queryset
    upcoming_event = [event for event in events if event.date >= cr_day]
    past_event = [event for event in events if event.date < cr_day]

    # Determine result based on type, but preserve search filters
    if type == "participants":
        result = participant
    elif type == "total_events":
        result = events  # Already filtered by search
    elif type == "upcoming":
        result = events.filter(date__gte=cr_day)
    elif type == "past":
        result = events.filter(date__lt=cr_day)
    else:
        result = events

    # Debug: Print final result
    print(f"Final result count: {result.count()}")
    print(f"Final result: {list(result)}")

    counts ={
        'upcoming' : len(upcoming_event),
        'past' : len(past_event),
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
    success_url = reverse_lazy("event-dashboard")

    def test_func(self):
        return is_admin(self.request.user) or is_organizer(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to create events.")
        return redirect("no-permission") 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_form"] = context.get("form") or EventModelForm()
        context["is_update"] = False
        return context
    
    def post(self, request, *args, **kwargs):
        event_form = EventModelForm(request.POST, request.FILES)
        if event_form.is_valid():
            event = event_form.save()
            messages.success(request, "Event created successfully")
            return redirect("event-dashboard")
        messages.error(request, "Please correct the errors below")
        return render(request, self.template_name, {"event_form": event_form, "is_update": False})
    
    
    



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



class UpdateEventView(UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventModelForm
    context_object_name = "event"
    pk_url_kwarg = "id"
    template_name = "event_form.html"

    def test_func(self):
        return is_admin(self.request.user) or is_organizer(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to update events.")
        return redirect("no-permission")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_form"] = context.get("form") or self.get_form()
        context["is_update"] = True
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        event_form = EventModelForm(request.POST, request.FILES, instance=self.object)
        if event_form.is_valid():
            event = event_form.save()
            messages.success(request, "Event updated successfully")
            return redirect("update-event", id=event.id)
        messages.error(request, "Please correct the errors below")
        return render(request, self.template_name, {"event_form": event_form, "is_update": True, "event": self.object})



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


class DeleteEventView(UserPassesTestMixin, DeleteView):
    model = Event
    pk_url_kwarg = "id"
    success_url = reverse_lazy("dashboard")

    def test_func(self):
        return is_admin(self.request.user) or is_organizer(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to delete events.")
        return redirect("no-permission")

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
            messages.success(request,"Category Created Successfully")
            return redirect("create-category")
        else:
            messages.error(request,"Please correct the errors below")
    context = {"category_form":category_form}
    return render(request,"category_form.html",context)



class CreateCategoryEvent(UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "category_form.html"
    success_url = reverse_lazy("create-category")

    def test_func(self):
        return is_admin(self.request.user) or is_organizer(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to create categories.")
        return redirect("no-permission")

    def post(self, request, *args, **kwargs):
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request,"Category Created Successfully")
            return redirect("create-category")
        else:
            messages.error(request,"Please correct the errors below")
            return render(request, self.template_name, {"category_form": category_form})





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
def event_details(request,event_id):
    event = Event.objects.get(id = event_id)
    return render(request,"event_details.html",{"event":event})



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
        messages.success(request,"You have already RSVP'd to this event")
    else:
        event.rspv.add(request.user)
        event.save()
        
        subject = f"RSVP confirmation for {event.name}"
        message = f"You have successfully RSVP'd for {event.name}"
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