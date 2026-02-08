from django.db import connection
from django.utils.timezone import now

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            db_status = "ok"
            overall_status = "ok"
            http_status = status.HTTP_200_OK
        except Exception:
            db_status = "error"
            overall_status = "degraded"
            http_status = status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(
            {
                "status": overall_status,
                "db": db_status,
                "service": "agriculture-backend",
                "timestamp": now().isoformat(),
            },
            status=http_status,
        )
