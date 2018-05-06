from .models import Note

def get_recommendations(subject):
    return Note.objects.all().filter(subject=subject).order_by('rating')[:1]
