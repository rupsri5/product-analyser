from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import os


class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


def excel_upload_path(instance, filename):
    """Generate upload path for excel files"""
    return os.path.join('excel_files', filename)


class ExcelFile(models.Model):
    """Model to store uploaded Excel files"""
    name = models.CharField(max_length=255, help_text="Display name for the Excel file")
    description = models.TextField(blank=True, help_text="Optional description of the file contents")
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    file = models.FileField(
        upload_to=excel_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        help_text="Upload Excel file (.xlsx or .xls)"
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Whether this file is available for analysis")

    # Store file metadata for quick access
    sheet_names = models.JSONField(default=list, blank=True, help_text="Names of sheets in the Excel file")
    column_info = models.JSONField(default=dict, blank=True, help_text="Column information for each sheet")
    
    # Store column configuration
    # Store sheet configuration
    enabled_sheets = models.JSONField(
        default=list,
        blank=True,
        help_text="List of enabled sheets in the Excel file"
    )
    sheet_config = models.JSONField(
        default=dict,
        blank=True,
        help_text="Configuration for each sheet including filter and result columns"
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Excel File'
        verbose_name_plural = 'Excel Files'

    def __str__(self):
        return self.name

    def get_file_size(self):
        """Get file size in MB"""
        try:
            return f"{self.file.size / (1024 * 1024):.2f} MB"
        except:
            return "Unknown"

    def get_sheet_count(self):
        """Get number of sheets"""
        return len(self.sheet_names) if self.sheet_names else 0

    def delete(self, *args, **kwargs):
        """Override delete to remove file from filesystem"""
        if self.file:
            try:
                os.remove(self.file.path)
            except:
                pass
        super().delete(*args, **kwargs)


class QueryLog(models.Model):
    """Log user queries for analytics"""

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    excel_file = models.ForeignKey(ExcelFile, on_delete=models.CASCADE)
    sheet_name = models.CharField(max_length=255)
    filters_applied = models.JSONField(help_text="Filters selected by user")
    result_found = models.BooleanField(default=False)
    result_data = models.JSONField(blank=True, null=True, help_text="Results returned")
    query_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-query_time']
        verbose_name = 'Query Log'
        verbose_name_plural = 'Query Logs'

    def __str__(self):
        return f"Query on {self.excel_file.name} at {self.query_time.strftime('%Y-%m-%d %H:%M')}"
