from django.db import models
from django.contrib.auth.models import User

from utils.generators.stylers import optimize_json, render_json
from utils.core import http_status as sc


class ReceivedRequest(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_requests', null=True)
    path = models.CharField(max_length=2048, null=False, blank=False)
    client_ip = models.CharField(max_length=256, db_index=True, null=False, blank=False)
    method = models.CharField(max_length=10, null=False, blank=False)
    headers = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    command = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    private_data = models.TextField(blank=True, null=True)
    status_code = models.IntegerField(null=True, blank=True)
    message = models.CharField(max_length=512, blank=True, null=True)
    status = models.BooleanField(null=True, blank=True)

    create_time = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Request'
        verbose_name_plural = 'Received Requests'
        ordering = ['-create_time']

    @property
    def rendered_headers(self):
        return render_json(self.headers)

    @property
    def rendered_data(self):
        return render_json(self.data)

    @property
    def rendered_response(self):
        return render_json(self.response)

    @property
    def rendered_private_data(self):
        return render_json(self.private_data)

    def save(self, *args, **kwargs):

        self.headers = optimize_json(self.headers)
        self.data = optimize_json(self.data)
        self.response = optimize_json(self.response)
        self.private_data = optimize_json(self.private_data)

        if self.status_code:
            if sc.is_success(self.status_code) or sc.is_informational(self.status_code):
                self.status = True
            else:
                self.status = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f"ReceivedRequest [ {self.method} {self.client_ip} ]"
