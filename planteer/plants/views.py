from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Plant, Comment
from .forms import PlantForm, CommentForm

# Create your views here.

def plant_list(request):
    plants = Plant.objects.all()

    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')

    if category and category != 'all':
        plants = plants.filter(category=category)
    if is_edible == 'true':
        plants = plants.filter(is_edible=True)

    context = {
        'plants': plants,
        'selected_category': category,
        'selected_is_edible': is_edible,
    }
    return render(request, 'plants/plant_list.html', context)
    pass


def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.plant = plant
            new_comment.save()
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        comment_form = CommentForm()

    comments = plant.comments.all()

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:4]

    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'related_plants': related_plants,
        'comments': comments,
        'comment_form': comment_form,
    })


def plant_create(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('plants:plant_list')
    else:
        form = PlantForm()
    return render(request, 'plants/plant_form.html', {
        'form': form,
        'title': 'Add New Plant',
    })


def plant_update(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)
    return render(request, 'plants/plant_form.html', {
        'form': form,
        'title': 'Update Plant',
    })


def plant_delete(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        plant.delete()
        return redirect('plants:plant_list')
    return render(request, 'plants/plant_confirm_delete.html', {
        'plant': plant
    })



def plant_search_view(request):
    # كل النباتات افتراضياً
    plants_qs = Plant.objects.all()

    # قيم الفلاتر من الـ GET
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    edible = request.GET.get("edible", "").strip()  # "yes" / "no" / ""

    # فلتر النص (اسم / وصف ...)
    if query:
        plants_qs = plants_qs.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
            # لو عندك حقول ثانية (scientific_name مثلاً) ضفها هنا
        )

    # فلتر الكاتيقوري
    if category:
        plants_qs = plants_qs.filter(category=category)

    # فلتر هل هي صالحة للأكل
    if edible == "yes":
        plants_qs = plants_qs.filter(is_edible=True)
    elif edible == "no":
        plants_qs = plants_qs.filter(is_edible=False)

    # لو عندك CATEGORY_CHOICES في المودل:
    try:
        categories = Plant.CATEGORY_CHOICES
    except AttributeError:
        # fallback لو ما عندك choices ثابتة
        categories = (
            plants_qs.values_list("category", "category")
            .distinct()
        )

    context = {
        "results": plants_qs,
        "query": query,
        "selected_category": category,
        "selected_edible": edible,
        "categories": categories,
    }
    return render(request, "plants/plant_search.html", context)
