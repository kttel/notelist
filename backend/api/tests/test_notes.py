from django.contrib.auth import get_user_model

from rest_framework.test import (
    APITestCase,
    APIClient,
)
from rest_framework import status

from api import models, serializers
from api.tests.utils import (
    create_note,
    get_note_detail_url,
    NOTES_LIST_URL,
)


class PublicNotesTests(APITestCase):
    """
    Test for API requests with an unauthenticated user.
    """
    def setUp(self):
        self.client = APIClient()

    def test_get_notes_unauthorized(self):
        res = self.client.get(NOTES_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateNotesTests(APITestCase):
    """
    Tests for API requests with an authenticated user.
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword123',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_notes(self):
        """
        Test that user gets his notes.
        """
        note = create_note(user=self.user)
        res = self.client.get(NOTES_LIST_URL)

        serializer = serializers.NoteSerializer(note)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer.data, res.data)

    def test_get_only_own_notes(self):
        """
        Test that user can see only his own notes.
        """
        note = create_note(user=self.user)

        other_user = get_user_model().objects.create_user(
            username='otheruser',
            password='password12345',
        )
        other_note = create_note(user=other_user)

        res = self.client.get(NOTES_LIST_URL)
        serializer1 = serializers.NoteSerializer(note)
        serializer2 = serializers.NoteSerializer(other_note)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        self.assertEqual(len(res.data), 1)

    def test_get_filtered_notes(self):
        """
        Tests that user gets correctly filtered by body content data.
        """
        note1 = create_note(user=self.user, body='test1')
        note2 = create_note(user=self.user, body='test2')
        note3 = create_note(user=self.user, body='another')

        res = self.client.get(NOTES_LIST_URL + '?query=test')
        serializer1 = serializers.NoteSerializer(note1)
        serializer2 = serializers.NoteSerializer(note2)
        serializer3 = serializers.NoteSerializer(note3)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
        self.assertEqual(len(res.data), 2)

    def test_get_filtered_notes_by_category(self):
        """
        Tests that user gets correctly filtered by category data.
        """
        category = models.Category.objects.create(name='test')

        note1 = create_note(user=self.user, body='first', category=category)
        note2 = create_note(user=self.user, body='second', category=category)
        note3 = create_note(user=self.user, body='third')

        res = self.client.get(NOTES_LIST_URL + '?query=test')
        serializer1 = serializers.NoteSerializer(note1)
        serializer2 = serializers.NoteSerializer(note2)
        serializer3 = serializers.NoteSerializer(note3)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
        self.assertEqual(len(res.data), 2)

    def test_get_own_note_detail(self):
        """
        Test that user gets correct note details.
        """
        note = create_note(user=self.user)

        res = self.client.get(get_note_detail_url(note.id))
        serializer = serializers.NoteSerializer(note)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)
        self.assertEqual(res.data['user'], self.user.id)

    def test_get_other_user_note_error(self):
        """
        Tests that user can't get note of other user.
        """
        other_user = get_user_model().objects.create_user(
            username='otheruser',
            password='password12345',
        )
        other_note = create_note(user=other_user)

        res = self.client.get(get_note_detail_url(other_note.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_note(self):
        """
        Test that user can create new note.
        """
        payload = {
            'body': 'Test data',
        }
        res1 = self.client.post(NOTES_LIST_URL, payload, format='json')
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        res2 = self.client.get(NOTES_LIST_URL)
        notes = models.Note.objects.filter(user=self.user)
        self.assertEqual(len(notes), 1)

        note = notes[0]
        serializer1 = serializers.NoteSerializer(note)
        self.assertIn(serializer1.data, res2.data)

        res3 = self.client.get(get_note_detail_url(note.id))
        serializer2 = serializers.NoteSerializer(note)
        self.assertEqual(serializer2.data, res3.data)
        self.assertIn(payload['body'], res3.data['body'])

    def test_create_note_no_body_bad_request(self):
        """
        Test that user can't create note with an empty body.
        """
        payload = {}
        res1 = self.client.post(NOTES_LIST_URL, payload, format='json')
        self.assertEqual(res1.status_code, status.HTTP_400_BAD_REQUEST)
        notes = models.Note.objects.filter(user=self.user)
        self.assertEqual(len(notes), 0)

    def test_update_note(self):
        """
        Test that user can update his note correctly.
        """
        note_body = 'old'
        note = create_note(user=self.user, body=note_body)
        payload = {'body': 'new'}
        res = self.client.put(get_note_detail_url(note.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data['body'], note_body)
        self.assertEqual(res.data['body'], payload['body'])
        self.assertEqual(res.data['user'], self.user.id)

    def test_delete_note(self):
        """
        Test that user can delete his note.
        """
        note = create_note(user=self.user)
        res = self.client.delete(get_note_detail_url(note.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        notes = models.Note.objects.filter(user=self.user)
        self.assertEqual(len(notes), 0)
