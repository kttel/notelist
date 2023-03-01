from django.contrib.auth import login, get_user_model
from django.db.models import Q, Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.views import LoginView as KnoxLoginView

from api import models, serializers, permissions as api_permissions


@api_view()
def get_routes(request):
    routes = [
        {
            'endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Return an array of notes'
        },
        {
            'endpoint': '/notes/:id/',
            'method': 'GET',
            'body': None,
            'description': 'Return a single note object'
        },
        {
            'endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ''},
            'description': 'Creates new note based on sent data'
        },
        {
            'endpoint': '/notes/:id/update/',
            'method': 'PUT',
            'body': {'body': ''},
            'description': 'Updates an existing note with sent data'
        },
        {
            'endpoint': '/notes/:id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes an existing note'
        },
    ]
    return Response(routes)


class NotesListView(generics.ListCreateAPIView):
    queryset = models.Note.objects.all()
    serializer_class = serializers.NoteSerializer

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        user_queryset = self.queryset.filter(user=self.request.user)
        filtered_by_query = user_queryset\
            .filter(Q(body__icontains=query) |
                    Q(category__name__icontains=query))
        return filtered_by_query


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Note.objects.all()
    serializer_class = serializers.NoteSerializer
    permission_classes = (api_permissions.OwnObjectPermission,)


class CategoryListView(generics.ListCreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        user = self.request.user
        return get_user_model().objects\
                               .filter(id=user.id)\
                               .annotate(total_notes=Count('note'))[0]


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny,)


class LoginView(KnoxLoginView):
    serializer_class = serializers.AuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
