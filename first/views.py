from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . models import User, Document
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
#login
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm, AddDocumentForm
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# To run python scripts
from subprocess import run, PIPE
import sys

# Create your views here.
def home(request):
    #return HttpResponse("<h1>Rajagiri Project</h1>")
    return render(request, 'first/home.html')

def index(request):
    #documents = Document.objects.filter()
    all_users = User.objects.all()
    #return render(request, 'first/index.html', {'documents': documents})
    return render(request, 'first/index.html', {'all_users': all_users})
    #patient = get_object_or_404(User, pk=user_id)
    #return render(request, 'first/detail.html', {'patient': patient})


def view(request):
    if request.user.is_staff:
        all_users = User.objects.all()
        return render(request, 'first/view.html', {'all_users': all_users})
    else:
        return render(request,'first/home.html')

def record(request, user_id, document_id):
    patient = get_object_or_404(User, pk=user_id)
    document = Document.objects.get(pk=document_id)
    context = {
        'patient': patient,
        'document': document, }

    return render(request, 'first/record.html', context)

def detail(request, user_id):
    #return HttpResponse("<h2>Details for User ID: "+ str(user_id)+" </h2>")
    #user = User.objects.get(pk=user_id)
    patient = get_object_or_404(User, pk=user_id)

    return render(request, 'first/detail.html', {'patient': patient})

def ind_record(request, user_id, document_id):


    return render(request, 'first/record.html', context)



#login
class LoginFormView(View):
    form_class = AuthenticationForm
    template_name = 'first/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        #form = self.form_class(request.POST)
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                #return render(request, 'first/view.html', {'name': request.user.username})
                #request.user.username
                #return render(request, 'first:view')
                return redirect('first:home')
                #return HttpResponse("Signed in ")
                #return redirect('first:home', {'name': request.user.username})
                #return render(request, 'first/view.html', {'users': request.user.username})
        else:
            #return render(request, 'first/view.html', {'error': 'Email or Password is incorrect'})
            return HttpResponse("Invalid Credentials <br/> Please go back and Login again")



class UserFormView(View):
    form_class = UserForm
    template_name = 'first/registration_form.html'

    #signup , shows the page
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #sends data to database
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            # to get normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            #signin if the credentials are correct

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    # request.user.username prints username
                    return redirect('first:home')

        return render(request, self.template_name, {'form': form})

def logout_user(request):
    logout(request)
    return redirect('first:login')
    form = UserForm(request.POST or None)
    context = {
        "form": form
    }
    return render(request, 'first/login.html', context)

class DocumentCreate(CreateView):
    model = Document
    fields = ['Hospital_id','Document_type','Document_image']
    template_name = 'first/document_form.html'

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            # to get normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()


def delete_document(request, user_id, document_id):
    patient = get_object_or_404(User, pk=user_id)
    document = Document.objects.get(pk=document_id)
    document.delete()
   # return render(request, 'first/index.html')
    #return HttpResponseRedirect("first/index")
    return redirect('first:index')


class DocumentDelete(DeleteView):
    model = Document
    success_url = reverse_lazy('first:home')

class CreateDocument(View):
    template_name = 'first/document_form.html'

    def get(self, request):
        form = AddDocumentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == "POST":
            form = AddDocumentForm(request.POST,request.FILES)

            if form.is_valid():
                user = form.save(commit=False)
                # to get normalized data
                Hospital_id = form.cleaned_data['Hospital_id']
                Document_type = form.cleaned_data['Document_type']



                user.save()
                return redirect('first:index')

                #signin if the credentials are correct





        return render(request, self.template_name, {'form': form})


def create(request):
    if request.method == "POST":
        form = AddDocumentForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            # to get normalized data
            Hospital_id = form.cleaned_data['Hospital_id']
            Document_type = form.cleaned_data['Document_type']

            user.save()


        else:
            form = AddDocumentForm()

        return render(request, 'first/document_form.html',{"form":form})


def search(request):

    search_term = ''

    if 'search' in request.GET:
        search_term = request.GET['search']
        patients = User.objects.all().filter(Hospital_id__icontains=search_term)

    return render(request, 'first/search.html', {'patients': patients, 'search_term': search_term})

def hospital_user(request):
    return render(request, 'first/hospital_user.html')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            #return render(request, 'first/change_password.html')
            return render(request, 'first/hospital_user.html')
            return redirect('first:hospital_user.html')
        else:
            messages.error(request, 'Please correct the error below.')
            return HttpResponse("<h1>Something went wrong<br/> Password couldnot be Updated<br/> Please try again</h1>")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'first/change_password.html', {'form': form})


def python(request, user_id=1):
    a=[]

    if request.method == "POST":
        patientid = request.POST.get('param')
        patient = User.objects.get(pk = patientid)
        document = Document()
        document.user = patient

        for document in patient.document_set.all():
            a.append(document.Document_image.url)

        #inp = request.POST.get('param')
        b = patient.Hospital_id
        out = run([sys.executable,'C:\\python\\Python38\\code10.py',str(a),str(b)], shell=False , stdout=PIPE )
        print(out)

        return render(request,'first/python.html',{'out':out.stdout})
    else:
        patient = get_object_or_404(User, pk=user_id)

        return render(request,'first/python.html',{'patient':patient})