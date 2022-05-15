from django.shortcuts import render, redirect

from petstagram.main.helpers import get_profile
from petstagram.main.models import Pet, PetPhoto, Profile
from petstagram.main.templates.forms import CreateProfileForm, EditProfileForm, DeleteProfileForm


def show_profile(request):
    profile = get_profile()
    pets = Pet.objects.filter(user_profile=profile)
    pet_photos = list(PetPhoto.objects.filter(tagged_pets__in=pets).distinct())

    total_pet_photos_count = len(pet_photos)
    total_likes_count = sum(p.likes for p in pet_photos)

    context = {
        'profile': get_profile(),
        'pets': pets,
        'total_pet_photos_count': total_pet_photos_count,
        'total_likes_count': total_likes_count,
    }
    return render(request, 'profile_details.html', context)


def profile_action(request, form_class, success_url_name, instance, template_name):
    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(success_url_name)
    else:
        form = form_class(instance=instance)

    context = {
        'form': form,
    }

    return render(request, template_name, context)


def create_profile(request):
    return profile_action(request, CreateProfileForm, 'index', Profile(), 'profile_create.html')


def edit_profile(request):
    return profile_action(request, EditProfileForm, 'profile details', get_profile(), 'profile_edit.html')


def delete_profile(request):
    return profile_action(request, DeleteProfileForm, 'index', get_profile(), 'profile_delete.html')
