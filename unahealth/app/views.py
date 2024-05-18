from rest_framework import generics
from .models import GlucoseLevel
from .serializers import GlucoseLevelSerializer
from rest_framework.pagination import PageNumberPagination
from datetime import datetime

class GlucoseLevelPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class GlucoseLevelList(generics.ListAPIView):
    serializer_class = GlucoseLevelSerializer
    pagination_class = GlucoseLevelPagination

    def format_timestamp(self, timestamp):
        original_datetime_str = timestamp
        datetime_obj = datetime.strptime(original_datetime_str, "%d-%m-%Y %H:%M")
        formatted_datetime_str = datetime_obj.strftime("%Y-%m-%d %H:%M")
        return formatted_datetime_str

    def get_queryset(self):
        user_id = self.request.query_params['user_id']
        start = self.format_timestamp(self.request.query_params['start'])
        stop = self.format_timestamp(self.request.query_params['stop'])
        return GlucoseLevel.objects.filter(user_id=user_id, timestamp__gte=start, timestamp__lte=stop)

class GlucoseLevelDetail(generics.RetrieveAPIView):
    queryset = GlucoseLevel.objects.all()
    serializer_class = GlucoseLevelSerializer
