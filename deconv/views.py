from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponseRedirect
from .psf import create_gaussian
from .deconvolution import create_filtered
from django.core.files.storage import FileSystemStorage
import cv2


# Create your views here.
filename="garden.png"
image_height=400
image_width=600

class IndexView(View):
    def get(self,request):
        global filename
        filename="garden.png"
        return render(request,"deconv/index.html",{"before_image":filename, "after_image":"new"+filename, "sigma":"", "epsilon":"", "t":"", "select":1})
    def post(self,request):
        global filename
        try:
            image=request.FILES['image']
            if(image.name.rfind('.png')!=-1 or image.name.rfind('.jpg')!=-1 or image.name.rfind('.jpeg')!=-1):
                fs = FileSystemStorage()
                extension=image.name.split('.')[1]
                filename = str(hash(image.name))+"."+extension
                fs.save(filename, image)
                im = cv2.imread("static/deconv/image/"+filename)
                global image_height
                global image_width
                image_height, image_width, _ = im.shape
                print(str(image_height))
        except:
            print("ファイルは存在しません")
        sigma=request.POST['sigma']
        try:
            epsilon=request.POST['epsilon']
            t=1
        except:
            t=request.POST['t']
            epsilon=1
        if request.POST['algorithm']=="standard":
            select=0
        else:
            select=1
        create_gaussian(image_width,image_height,float(sigma),"static/deconv/image/gaussian.png")
        create_filtered("static/deconv/image/"+filename,
                        "static/deconv/image/new"+filename,
                        "static/deconv/image/gaussian.png",
                        select=select,input_t=float(t),epsilon=float(epsilon))
        return render(request,"deconv/index.html",{"before_image":filename, "after_image":"new"+filename, "sigma":sigma, "epsilon":epsilon, "t":t, "select":select})

index=IndexView.as_view()