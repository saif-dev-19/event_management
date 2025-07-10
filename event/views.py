from django.shortcuts import render,redirect
from django.http import HttpResponse
from event.forms import EventModelForm,CategoryForm,ParticipantForm
from event.models import Participant,Event
from django.contrib import messages
from django.db.models import Q,Count
from datetime import datetime,date
from django.utils.timezone import localdate
from users.views import is_organizer,is_admin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def is_users(user):
    return user.groups.filter(name = 'User').exists()

def home_page(request):
    return render(request,"home_page.html")

def participant_page(request):
    return render(request,"grids/participant_page.html")

def show_event(request):
    return HttpResponse("Events")

@user_passes_test(is_organizer,login_url="no-permission")
def organizer_dashboard(request):
    events = Event.objects.prefetch_related('participants').all()
    for e in events:
        event = e
    return render(request,"dashboard/organizer_dashboard.html",{'events':events,'event':event})


@user_passes_test(is_users,login_url="no-permission")
def user_dashboard(request):
    type = request.GET.get('type','all')

    cr_day = datetime.now().date()
    events = Event.objects.prefetch_related('participants').all()
    participant = User.objects.all()
    print(participant)

    search_name= request.GET.get('name')
    search_location =request.GET.get('location')

    if search_name:
        events = events.filter(name__icontains = search_name)
    if search_location:
        events = events.filter(name__icontains = search_location)

    
    upcoming_event = [event for event in events if event.date >= cr_day]
    past_event = [event for event in events if event.date < cr_day]


    if type =="participants":
        result = participant
    elif type == "total_events":
        result = events
    elif type == "upcoming":
        result = events.filter(date__gte=cr_day)
    elif type == "past":
        result = events.filter(date__lte=cr_day)
    else:
        result = events.filter(date__gte=cr_day)

    

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

    

@user_passes_test(is_admin,login_url="no-permission")
def create_event(request):
    event_form = EventModelForm()

    if request.method == "POST":
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
        
    context = {"event_form":event_form}
    return render(request,"event_form.html",context)


@user_passes_test(is_admin,login_url="no-permission")
@user_passes_test(is_organizer,login_url="no-permission")
def update_event(request,id):
    event = Event.objects.get(id = id)
    event_form = EventModelForm(instance = event)


    if request.method == "POST":
        event_form = EventModelForm(request.POST,instance = event)

        if event_form.is_valid():
            
            event_form.save()

            if messages.success:
                messages.success(request,"Event updated Successfully")
                return redirect("update-event")
            elif messages.error:
                messages.error(request,"something wrong")
                return redirect("update-event")
        
    context = {"event_form":event_form}
    return render(request,"event_form.html",context)


@user_passes_test(is_organizer,login_url="no-permission")
def delete_event(request,id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request,"Event Delete Successfully")
        return redirect('organizer-dashboard')
    else:
        messages.error(request,"something went wrong")
        return redirect('organizer-dashboard')




@user_passes_test(is_organizer,login_url="no-permission")
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



def create_participant(request):
    participant_form = ParticipantForm()

    if request.method == "POST":
        participant_form = ParticipantForm(request.POST)
        print("inside post")

        if participant_form.is_valid():
            participant_form.save()

            if messages.success:
                messages.success(request,"Event Created Successfully")
                return redirect("create-participant")
            elif messages.error:
                messages.error(request,"something wrong")
                return redirect("create-participant")


    context = {"participant_form":participant_form}
    return render(request,"create_participant.html",context)

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