from django.contrib import messages
from django.shortcuts import render ,redirect
import bcrypt
from .models import *
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from .forms import *


def index(request):
    return render(request,"index.html")


def signin(request):
    return render(request,"login.html")

def register(request):
    return render(request,'register.html')

def signup(request):
    if request.method =='POST':
        errors=Users.objects.validator(request.POST)
        if len(errors) > 0:
            for key , value in errors.items():
                messages.error(request,value)
            
            return redirect('/register')
        else:
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            email=request.POST['email']
            password=request.POST['password']
            pwhash=bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
            new_user=Users.objects.create(first_name=first_name,last_name=last_name,email=email,password=pwhash)
            new_user.save()
            request.session['loggedIn'] = new_user.id
            return redirect('/dashboard')

def login(request):
    if request.method=='POST':
        users_all = Users.objects.filter(email=request.POST['email'])
        if len(users_all)==1:
            if not bcrypt.checkpw(request.POST['password'].encode(),users_all[0].password.encode()):
                messages.error(request, "Email or Password is incorrect!")
                return redirect('/signin')
            else:
                request.session['loggedIn'] = users_all[0].id   
                return redirect('/dashboard')
        else:
            messages.error(request, "Email does not exist!")
            return redirect('/signin')

def dashboard(request):
    context={
        'todos': Todo.objects.all(),
        'user_posts':Users.objects.get(id=request.session['loggedIn']).user_post.order_by('-created_at')[0:3],
        'posts' :Posts.objects.all().order_by('-created_at')[0:3],
        'users':Users.objects.get(id=request.session['loggedIn']),
        'post':Posts.objects.all(),
        'note_count':Note.objects.all().count()-1,
        'file_count':File.objects.all().count(),
        'Image_count':Image.objects.all().count(),
        'Algorithm_count':Algorithm.objects.all().count(),
    }
    return render(request,'dashboard.html',context)

####note
def note(request):
    context={
        'users':Users.objects.get(id=request.session['loggedIn']),
    }
    return render(request,'note.html',context)


def add_note(request):
    if request.method=='POST':
        new_create=Note.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            user=Users.objects.get(id=request.session['loggedIn']),
        )
        new_create.save()
    return redirect('/note')


def edit_note(request,note_id):

    context={
        'user':Users.objects.get(id= request.session['loggedIn']),
        'note':Note.objects.get(id=note_id),
    }
    return render(request,'note_edit.html',context)


def update_note(request,note_id):
    note=Note.objects.get(id=note_id)
    if request.method=='POST':
        note.title=request.POST['title']
        note.content=request.POST['content']
        note.save()
        return redirect('/note')
##post

def posts(request):
    context={
        'posts' :Posts.objects.all(),
    }

    return render (request,'posts.html',context)

def add_post(request):
    if request.method=='POST':
        new_create=Posts.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            user=Users.objects.get(id=request.session['loggedIn']),
        )
        new_create.save()
    return redirect('/posts')


def edit_information(request,post_id):

    context={
        'user':Users.objects.get(id= request.session['loggedIn']),
        'posts_id':Posts.objects.get(id=post_id),
    }

    return render(request,'edit_post.html',context)

def update_post(request,post_id):
    posts_id=Posts.objects.get(id=post_id)
    if request.method=='POST':
        posts_id.title=request.POST['title']
        posts_id.content=request.POST['content']
        posts_id.save()
        return redirect('/posts')

## comment

def comment(request,id):
    context={
        
        'post':Posts.objects.get(id=id),
        'comments': Posts.objects.get(id=id).comments.order_by('-created_at'),
    }
    return render(request,"comment.html",context)


def add_Comments(request,id):
    if request.method=='POST':
        new_create=Comments.objects.create(
            comment=request.POST['comment'],
            post=Posts.objects.get(id=id),
            user=Users.objects.get(id=request.session['loggedIn']),
    
        )
        new_create.save()
    return redirect(f'/comment/{id}')

def add_todo(request):
    if request.method=='POST':
        new_create=Todo.objects.create(
            todo=request.POST['todo'],
            uploaded_by=Users.objects.get(id=request.session['loggedIn']),
        )
        new_create.save()
    return redirect('/dashboard')

def delete_todo(request,id):
    todo=Todo.objects.get(id=id)
    todo.delete()
    return redirect('/dashboard')

def algo(request):
    context={
        'algos' :Algorithm.objects.all(),
    }
    return render(request,'algo.html',context)

def profile(request):
    context={
        'user_posts':Users.objects.get(id=request.session['loggedIn']).user_post.order_by('-created_at'),
        'user_comments':Users.objects.get(id=request.session['loggedIn']).user_comment.order_by('-created_at'),
    }
    return render(request,'profile.html',context)

def add_algorithm(request):
    if request.method=='POST':
        new_create=Algorithm.objects.create(
            created_by=Users.objects.get(id=request.session['loggedIn']),
            desc=request.POST['desc'],
            title=request.POST['title']
        )
        new_create.save()
    return redirect('/algo')

def image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    form = ImageForm()
    img = Image.objects.all()
    return render(request, 'image.html', {'img':img ,'form': form})


def files_list(request):
    files = File.objects.all()
    return render(request, 'file_list.html', {
        'files': files
    })


def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = FileForm()
    return render(request, 'upload.html', {
        'form': form
    })

def delete_image(request, id):
    if request.method == 'POST':
        image = Image.objects.get(id=id)
        image.delete()
    return redirect('/image')


def delete_file(request, id):
    if request.method == 'POST':
        book = File.objects.get(id=id)
        book.delete()
    return redirect('file_list')



def delete_Note(request,note_id):

    note_delete=Note.objects.get(id=note_id)

    note_delete.delete()

    return redirect('/note')




def logout(request):
    request.session.clear()
    return redirect('/')



