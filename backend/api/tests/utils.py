from django.urls import reverse

from api import models


NOTES_LIST_URL = reverse('notes-list')


def create_note(user, body='Test note', category=None):
    note = models.Note.objects.create(user=user, body=body)
    if category is not None:
        note.category = category
        note.save()
    return note


def get_note_detail_url(note_id):
    return reverse('note-detail', kwargs={'pk': note_id})
