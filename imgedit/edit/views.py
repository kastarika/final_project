from django.shortcuts import render, redirect
from .models import aks
from . import forms
from django.http import HttpResponse
from PIL import Image
import os
# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def show_all(request):
    all_img = aks.objects.all()
    return render(request, 'edit/show_all.html', {'all_img':all_img})

def first_page(request):
    if(request.method == 'POST'):
        if(request.POST['first_action'] == 'show'):
            return redirect('edit:show_all')
        else:
            return redirect('edit:upload')
    else:
        return render(request, 'edit/first_page.html')

def upload(request):
    if(request.method == 'POST'):
        form = forms.get_image(request.POST, request.FILES)
        if(form.is_valid()):
            a = form.save()
            #return redirect('/edit/' + str(aks.objects.latest('id').id) + '/')
            return redirect('/edit/' + str(a.id) + '/')
        else:
            form = forms.get_image()
            return render(request, 'edit/failed_upload.html', {'get_image': form})
    else:
        form = forms.get_image()
        return render(request, 'edit/upload.html', {"get_image":form})

def edit(request, shomare):
    if(request.method == 'POST'):
        if(request.POST.get('go_back', '') == 'go back to first page'):
            return redirect('edit:first_page')

        edit_type = request.POST['edit_type']
        last_img = aks.objects.get(id=shomare)
        cur = Image.open(last_img.img.path)

        if(edit_type == 'crop'):
            crop_left = int(request.POST['crop_left'])
            crop_up = int(request.POST['crop_up'])
            crop_right = int(request.POST['crop_right'])
            crop_down = int(request.POST['crop_down'])
            if(crop_down > last_img.img.height or crop_right > last_img.img.width or crop_up >= crop_down or crop_left >= crop_right):
               return redirect('/edit/' + str(shomare) + '/')
            cur.crop((crop_left, crop_up, crop_right, crop_down)).save(last_img.img.path)

        if(edit_type == 'resize'):
            resize_width = int(request.POST['resize_width'])
            resize_height = int(request.POST['resize_height'])
            cur.resize((resize_width, resize_height)).save(last_img.img.path)

        if(edit_type == 'convert'):
            cur.convert(mode='L').save(last_img.img.path)

        if(edit_type == 'rotate'):
            cur.rotate(int(request.POST['rotation_degree'])).save(last_img.img.path)

        if(edit_type == 'share'):
            last_img.show = True
            last_img.save()
            return redirect('edit:show_all')

        return redirect('/edit/' + str(shomare) + '/')
    else:
        last_img = aks.objects.get(id=shomare)
        return render(request, 'edit/edit.html', {'last_img':last_img})
