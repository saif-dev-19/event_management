from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegistrationForm,CustomPasswordResetConfirmForm,EditProfileForm,CustomPasswordResetForm,CustomRegistrationForm,AssignRoleForm,CreateGroupForm,CustomPasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from users.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.timezone import datetime
from event.models import Event,Participant
from django.db.models import Prefetch
from event.forms import EventModelForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.views import LoginView,PasswordChangeView
from django.views.generic import TemplateView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView
from django.contrib.auth import get_user_model
# Create your views here.


User = get_user_model()

class ProfileView(TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['number'] = user.number
        context['profile_image'] = user.profile_image
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login

        return context
    

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user
    
    def form_valid(self,form):
        form.save()
        return redirect('profile')
    


class ChangePassword(PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = CustomPasswordChangeForm


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "registration/reset_password.html"
    success_url = reverse_lazy("sign-in")
    html_email_template_name = "registration/reset_email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(self.request,'A reset email send to your mail')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = "registration/reset_password.html"
    success_url = reverse_lazy("sign-in")

    def form_valid(self, form):
        messages.success(self.request,'password reset successfully')
        return super().form_valid(form)

def is_admin(user):
    return user.groups.filter(name ='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()


def sign_up(request):
    if request.method == "GET":
        form = CustomRegistrationForm()
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(request,"A conformation email sent, please check your email")
            return redirect("sign-in")
        else:
            print("Form is not valid")
    return render(request,"registration/register.html",{'form':form})

def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("home")
    return render(request,"registration/login.html",{'form':form})


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("home")

    # def get_success_url(self):
    #     next_url = self.request.GET.get('next')
    #     print("next",next_url)
    #     return next_url if next_url else super().get_success_url()



@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign-in")


def activate_user(request,user_id,token):
    try:  
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect("sign-in")
        else:
            return HttpResponse("Invalid Id or Token")
        
    except User.DoesNotExist:
        return HttpResponse("User not found")


@user_passes_test(is_admin,login_url="no-permission")
def admin_dashboard(request):
    type = request.GET.get('type','all')

    # users = User.objects.all()
    users = User.objects.prefetch_related(Prefetch('groups',queryset=Group.objects.all(), to_attr="all_groups")).all()
    for group in users:
        if group.all_groups:
            group.group_name = group.all_groups[0].name
        else:
            group.group_name = "No Group Assigned"

    cr_day = datetime.now().date()
    events = Event.objects.prefetch_related('participants').all()
    participant = Participant.objects.all()
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
        result = events

    

    counts ={
        'upcoming' : len(upcoming_event),
        'past' : len(past_event),
        'total_participant' : User.objects.values('id').distinct().count(),
        'total_event' : events.count(),
        
    }
    
    context = {
        'counts' : counts,
        'result' : result,
        'type':type,
        'search_name' : search_name,
        'search_location' : search_location,
        'users' : users,
        'group' : group.group_name,
        'role' : 'admin'

    }
    print(result)
    
    print(counts)
    
    print(users)


    return render(request,"admin/dashboard.html",context)


@user_passes_test(is_admin,login_url="no-permission")
def delete_participant(request,id):
    if request.method == "POST":
        participant = User.objects.get(id=id)
        participant.delete()
        messages.success(request,"Participant Delete Successfully")
        return redirect('admin-dashboard')
    else:
        messages.error(request,"something went wrong")
        return redirect('admin-dashboard')


@user_passes_test(is_admin,login_url="no-permission")
def assign_role(request,user_id):
    user = User.objects.get(id = user_id)
    form = AssignRoleForm()
    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request,f"User {user.username} assigned to the {role.name} role")
            return redirect('admin-dashboard')
    return render(request,"admin/assign_role.html",{'form':form})


@user_passes_test(is_admin,login_url="no-permission")
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request,f"Group {group.name} has been created successfully")
            return redirect('create-group')
        
    return render(request,"admin/create_group.html",{'form':form})



# @user_passes_test(is_organizer,login_url="no-permission")
# @user_passes_test(is_admin,login_url="no-permission")
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

def group_list(request):
    groups = Group.objects.all()
    return render(request,"admin/group_list.html",{'groups':groups})