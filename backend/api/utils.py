
# def create_note(request):
#     data = request.data

#     if data is not None:
#         body = data.get('body')
#         note = models.Note.objects.create(
#             body=body
#         )
#         data = serializers.NoteSerializer(note, many=False).data
#         return Response(data)
#     return Response()
