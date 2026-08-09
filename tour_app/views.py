from django.shortcuts import get_object_or_404, render

from .models import TourPackage


def package_data():
    return [
        {
            'title': 'Bali Island Escape',
            'slug': 'bali-island-escape',
            'image': 'https://images.unsplash.com/photo-1537996194471-e657df8fabcc?auto=format&fit=crop&q=80',
            'country': 'Indonesia',
            'duration': '5 Days / 4 Nights',
            'price': '$649',
            'summary': 'Chase islands, temples, beaches, and a slower rhythm of island life.',
        },
        {
            'title': 'Swiss Alpine Journey',
            'slug': 'swiss-alpine-journey',
            'image': 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&q=80',
            'country': 'Switzerland',
            'duration': '7 Days / 6 Nights',
            'price': '$1,299',
            'summary': 'Glacier trails, lake towns, and alpine villages across classic Switzerland.',
        },
        {
            'title': 'Moroccan Heritage Tour',
            'slug': 'moroccan-heritage-tour',
            'image': 'https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&q=80',
            'country': 'Morocco',
            'duration': '6 Days / 5 Nights',
            'price': '$899',
            'summary': 'Wander medinas, architecture, desert light, and vibrant local culture.',
        },
    ]


def home(request):
    packages = list(TourPackage.objects.all()[:3])
    if not packages:
        packages = package_data()

    stats = [
        {'label': 'Happy Travelers', 'value': '24K+'},
        {'label': 'Destinations', 'value': '48+'},
        {'label': 'Expert Guides', 'value': '120'},
        {'label': 'Travel Awards', 'value': '16'},
    ]

    context = {
        'packages': packages,
        'stats': stats,
    }
    return render(request, 'tour_app/index.html', context)


def packages(request):
    package_list = list(TourPackage.objects.all())
    if not package_list:
        package_list = package_data()

    context = {
        'packages': package_list,
    }
    return render(request, 'tour_app/packages.html', context)


def package_detail(request, slug):
    package = get_object_or_404(TourPackage, slug=slug)
    return render(request, 'tour_app/package_detail.html', {'package': package})
