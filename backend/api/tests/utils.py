from django.urls import reverse

from api import models


NOTES_LIST_URL = reverse('notes-list')
PROFILE_URL = reverse('profile')
REGISTER_URL = reverse('register-user')


def create_note(user, body='Test note', category=None):
    note = models.Note.objects.create(user=user, body=body)
    if category is not None:
        note.category = category
        note.save()
    return note


def get_note_detail_url(note_id):
    return reverse('note-detail', kwargs={'pk': note_id})
