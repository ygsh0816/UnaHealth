import csv

from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response

from .models import GlucoseLevel
from .serializers import GlucoseLevelSerializer
from rest_framework.pagination import PageNumberPagination
from datetime import datetime

class GlucoseLevelPagination(PageNumberPagination):
    """
    Custom Pagination class
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class GlucoseLevelList(generics.ListAPIView):
    """
    API to return list of Glucose levels for a user with an optional start and stop timestamps
    """
    serializer_class = GlucoseLevelSerializer
    pagination_class = GlucoseLevelPagination

    def format_timestamp(self, timestamp):
        """
        A Function to convert the datetime string to desired format
        """
        original_datetime_str = timestamp
        datetime_obj = datetime.strptime(original_datetime_str, "%d-%m-%Y %H:%M")
        formatted_datetime_str = datetime_obj.strftime("%Y-%m-%d %H:%M")
        return formatted_datetime_str

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        start = self.request.query_params.get('start', None)
        stop = self.request.query_params.get('stop', None)
        limit = self.request.query_params.get('limit', None)
        ordering = self.request.query_params.get('ordering', None)

        base_queryset = GlucoseLevel.objects.filter(user_id=user_id)

        if start:
            base_queryset.filter(timestamp__gte=self.format_timestamp(start))
        if stop:
            base_queryset.filter(timestamp__gte=self.format_timestamp(stop))
        if ordering:
            base_queryset = base_queryset.order_by(ordering)
        if limit:
            base_queryset = base_queryset[:int(limit)]

        return base_queryset

class GlucoseLevelDetail(generics.RetrieveAPIView):
    """API to return Details of a Glucose Level by ID"""
    queryset = GlucoseLevel.objects.all()
    serializer_class = GlucoseLevelSerializer


class GlucoseLevelCreate(generics.CreateAPIView):
    """
    API to record Glucose level of a User
    """
    queryset = GlucoseLevel.objects.all()
    serializer_class = GlucoseLevelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GlucoseLevelExport(generics.ListAPIView):
    """
    API to export a user's data in different file formats eg. CSV, JSON
    """
    serializer_class = GlucoseLevelSerializer

    def get(self, request, *args, **kwargs):
        format_type = request.query_params.get('format_type', 'json')
        user_id = request.query_params.get('user_id')
        queryset = GlucoseLevel.objects.filter(user_id=user_id)

        if format_type == 'csv':
            return self.export_to_csv(queryset)
        else:  # Default to JSON
            return self.export_to_json(queryset)

    def export_to_json(self, queryset):
        serializer = self.get_serializer(queryset, many=True)
        return HttpResponse(
            serializer.data,
            content_type='application/json'
        )

    def export_to_csv(self, queryset):
        serializer = self.get_serializer(queryset, many=True)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="glucose_levels.csv"'
        writer = csv.writer(response)
        headers = [field for field in serializer.data[0].keys()]
        writer.writerow(headers)

        for row in serializer.data:
            writer.writerow([row[field] for field in headers])

        return response