from django.views.decorators.cache import never_cache
from unicodedata import name
from django.shortcuts import render,redirect
from .models import Users
from django.contrib import messages

# Create your views here.
@never_cache
def index(request):
    if 'username' in request.session:
        username=request.session.get('username')
        usertype=Users.objects.get(username=username)
        if(usertype.usertype == 'admin'):
            return redirect(home)
        else:
            return redirect(user_home)
    return render(request, 'index.html')

@never_cache
def login(request):
    if 'username' in request.session:
        username=request.session.get('username')
        usertype=Users.objects.get(username=username)
        if(usertype.usertype == 'admin'):
            return redirect(home)
        else:
            return redirect(user_home)
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password'] 
        user=Users.objects.filter(username=username,password=password)
        if user:
            request.session['username']=username
            log=Users.objects.get(username=username,password=password)
            if(log.usertype == 'user'):
                return redirect(user_home)
            else:
                return redirect(home)
        else:
            messages.info(request,'invalid username or password')
            return redirect(login)
    return render(request, 'login.html')

@never_cache
def home(request):
    if 'username' in request.session:
        username=request.session.get('username')
        usertype=Users.objects.get(username=username)
        if(usertype.usertype == 'admin'):
            if request.method=='POST':
                search = request.POST['search']
                if len(search) == 0:
                    dests=Users.objects.all() 
                    return render(request, 'home.html',{'dests':dests})
                dests=Users.objects.filter(name__icontains=search)
                return render(request, 'home.html',{'dests':dests})
            dests=Users.objects.all() 
            return render(request, 'home.html',{'dests':dests})
        elif(usertype.usertype == 'user'):
            return redirect(user_home)
    else:
        return redirect(login)
    

@never_cache
def insert(request):
    if 'username' in request.session:
        username=request.session.get('username')
        usertype=Users.objects.get(username=username)
        if(usertype.usertype == 'admin'):
            return redirect(home)
        else:
            return redirect(user_home)
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        if Users.objects.filter(email=email).exists():
            messages.info(request,'Email already exist')
            return redirect(insert)
        username = request.POST['username']
        if Users.objects.filter(username=username).exists():
            messages.info(request,'Username is not available')
            return redirect(insert)
        password = request.POST['password'] 
        usertype = 'user'
        reg=Users.objects.create(name=name,email=email,username=username,password=password,usertype=usertype)
        reg.save()
        return redirect(login)
    return render(request, 'register.html')

@never_cache
def admin_insert(request):
    if 'username' in request.session:
        username=request.session.get('username')
        usertype=Users.objects.get(username=username)
        if(usertype.usertype == 'admin'):
            if request.method=='POST':
                name = request.POST['name']
                email = request.POST['email']
                if Users.objects.filter(email=email).exists():
                    messages.info(request,'Email already exist')
                    return redirect(admin_insert)
                username = request.POST['username']
                if Users.objects.filter(username=username).exists():
                    messages.info(request,'Username is not available')
                    return redirect(admin_insert)
                password = request.POST['password'] 
                usertype = 'user'
                reg=Users.objects.create(name=name,email=email,username=username,password=password,usertype=usertype)
                reg.save()
                messages.info(request,'user created')
                return redirect(admin_insert)
            return render(request, 'admin_register.html')
        elif(usertype.usertype == 'user'):
            return redirect(user_home)
    else:
        return redirect(login)
    

@never_cache
def logout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect(index)

@never_cache
def deleterow(request,id):
    data=Users.objects.get(id=id)
    data.delete()
    return redirect(home)

@never_cache
def updaterow(request,id):
    if 'username' in request.session:
        username=request.session.get('username')
        usertype=Users.objects.get(username=username)
        if(usertype.usertype == 'admin'):
            data = Users.objects.get(id=id)
            if request.method=='POST':
                name = request.POST['name']
                email = request.POST['email']
                if Users.objects.filter(email=email).exists():
                    check = Users.objects.get(email=email)
                    print("msg", check.email, check.id, type(check.id))
                    print(id, type(id))

                    if int(id) == check.id:
                        print(id, check.id)
                    else:
                        messages.info(request,'Email already exist')
                        return redirect(updaterow,id)
                username = request.POST['username']
                if Users.objects.filter(username=username).exists():
                    check = Users.objects.get(username=username)
                    print("msg", check.email, check.id, type(check.id))
                    print(id, type(id))

                    if int(id) == check.id:
                        print(id, check.id)
                    else:
                        messages.info(request,'Username already exist')
                        return redirect(updaterow,id)
                data_tb=Users.objects.get(id=id)
                data_tb.name=name
                data_tb.email=email
                data_tb.username=username
                data_tb.save()
                messages.info(request,'Updated successfully')
                return redirect(updaterow,id)
            return render(request,"update.html",{'data':data})
        elif(usertype.usertype == 'user'):
            return redirect(user_home)
    else:
        return redirect(login)

@never_cache
def user_home(request):
    if 'username' in request.session:
        username=request.session.get('username')
        usertype=Users.objects.get(username=username)
        if(usertype.usertype == 'user'):
            return render(request, 'user_home.html',{'user':usertype})
        elif(usertype.usertype == 'admin'):
            return redirect(home)
    else:
        return redirect(login)