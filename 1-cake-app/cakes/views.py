from .models import Cake, Baker
from .forms import CakeForm
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    cakes = Cake.objects.all()
    context = {'cakes': cakes}
    return render(request, 'index.html', context)

def add(request):
    if request.method == 'POST':
        form = CakeForm(request.POST, request.FILES)
        baker = Baker.objects.filter(user=request.user).first()
        if form.is_valid():
            cake = form.save(commit=False)
            cake.baker = baker
            cake.save()
            return redirect('index')

    form = CakeForm()
    return render(request, 'add.html', {'form': form})

