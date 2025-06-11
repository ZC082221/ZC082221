from django.db import models
from django.contrib.auth.models import User
import uuid

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class BaseDocument(models.Model): # Renamed from Document to BaseDocument
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('IN_REVIEW', 'In Review'),
        ('APPROVED', 'Approved'),
        ('OBSOLETE', 'Obsolete'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='owned_%(class)ss', on_delete=models.SET_NULL, null=True) # Adjusted related_name
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    version = models.CharField(max_length=20, default="1.0")
    qr_code_link = models.URLField(max_length=500, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='%(class)s_documents') # Adjusted related_name

    class Meta:
        ordering = ['-updated_at']
        abstract = True

    def __str__(self):
        return f"{self.title} (v{self.version})"

class SOP(BaseDocument): # Inherits from BaseDocument
    # SOP specific fields can be added here if any
    pass

class SopStep(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sop = models.ForeignKey(SOP, related_name='steps', on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='sop_steps/photos/%Y/%m/%d/', blank=True, null=True)
    video = models.FileField(upload_to='sop_steps/videos/%Y/%m/%d/', blank=True, null=True)

    class Meta:
        ordering = ['sop', 'step_number']
        unique_together = ('sop', 'step_number')

    def __str__(self):
        return f"SOP: {self.sop.title} - Step {self.step_number}"

class KanbanCard(BaseDocument): # Inherits from BaseDocument
    part_number = models.CharField(max_length=100, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    item_description = models.TextField(blank=True)
    barcode_data = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='kanban_cards/photos/%Y/%m/%d/', blank=True, null=True)

class ChangeLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_title = models.CharField(max_length=255)
    document_version = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    change_description = models.TextField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Log for {self.document_title} v{self.document_version} at {self.timestamp}"

class FeedbackComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_identifier = models.CharField(max_length=255, help_text="Title or ID of the document being commented on")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Comment on {self.document_identifier} by {self.user.username if self.user else 'Anonymous'} at {self.timestamp}"
