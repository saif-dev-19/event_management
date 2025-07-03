from django.shortcuts import render,redirect
from django.http import HttpResponse
from event.forms import EventModelForm,CategoryForm,ParticipantForm
from event.models import Participant,Event
from django.contrib import messages
from django.db.models import Q,Count
from datetime import datetime,date
from django.utils.timezone import localdate

# Create your views here.
def home_page(request):
    return render(request,"dashboard/home_page.html")

def participant_page(request):
    return render(request,"grids/participant_page.html")

def show_event(request):
    return HttpResponse("Events")

def event_dashboard(request):
    type = request.GET.get('type','all')

    cr_day = datetime.now().date()
    events = Event.objects.prefetch_related('participants').all()
    participant = Participant.objects.all()

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
        result = events

    

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
        'search_location' : search_location

    }

    return render(request,"dashboard/event_dashboard.html",context)



def create_event(request):
    event_form = EventModelForm()

    if request.method == "POST":
        event_form = EventModelForm(request.POST)
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


def update_event(request,id):
    event = Event.objects.get(id = id)
    event_form = EventModelForm(instance = event)

    if event.category:
        category_form = CategoryForm(instance = event.category)

    if request.method == "POST":
        event_form = EventModelForm(request.POST,instance = event)
        category_form = CategoryForm(request.POST,instance = event.category)

        if event_form.is_valid() and category_form.is_valid():
            
            
            event = event_form.save()
            category = category_form.save(commit=False)
            event.category = category
            category.save()

            if messages.success:
                messages.success(request,"Event updated Successfully")
                return redirect("update-event")
            elif messages.error:
                messages.error(request,"something wrong")
                return redirect("update-event")
        
    context = {"event_form":event_form,"category_form":category_form}
    return render(request,"event_form.html",context)

def delete_event(request,id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request,"Event Delete Successfully")
        return redirect('event-dashboard')
    else:
        messages.error(request,"something went wrong")
        return redirect('event-dashboard')



def create_category(request):
    category_form = CategoryForm()

    if request.method =="POST":
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()

            if messages.success:
                messages.success(request,"Event Created Successfully")
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