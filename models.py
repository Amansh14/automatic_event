from django.db import models

class EventType(models.Model):
    name = models.CharField(max_length=100)

class Event(models.Model):
    employee_id = models.CharField(max_length=50)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    date = models.DateField()

class EmailTemplate(models.Model):
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()

class Employee(models.Model):
    email = models.EmailField()
