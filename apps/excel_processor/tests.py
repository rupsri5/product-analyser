from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
import json
import os
import tempfile
import pandas as pd

from .models import ExcelFile, QueryLog

User = get_user_model()


class ExcelFileModelTest(TestCase):
    """Test ExcelFile model"""

    def setUp(self):
        # Create a temporary Excel file for testing
        self.temp_excel_data = pd.DataFrame({
            'category': ['A', 'B', 'A', 'B'],
            'product': ['Product1', 'Product2', 'Product3', 'Product4'],
            'total': [100, 200, 150, 250],
            'product_code': ['P1', 'P2', 'P3', 'P4']
        })

    def test_excel_file_creation(self):
        """Test creating an ExcelFile instance"""
        excel_file = ExcelFile.objects.create(
            name="Test Excel",
            description="Test description",
            sheet_names=['Sheet1'],
            column_info={'Sheet1': {'columns': ['col1', 'col2']}}
        )

        self.assertEqual(excel_file.name, "Test Excel")
        self.assertTrue(excel_file.is_active)
        self.assertEqual(excel_file.get_sheet_count(), 1)

    def test_str_method(self):
        """Test string representation"""
        excel_file = ExcelFile.objects.create(name="Test File")
        self.assertEqual(str(excel_file), "Test File")


class ViewsTest(TestCase):
    """Test views"""

    def setUp(self):
        self.client = Client()
        self.excel_file = ExcelFile.objects.create(
            name="Test Excel",
            sheet_names=['Sheet1'],
            column_info={
                'Sheet1': {
                    'all_columns': ['category', 'product', 'total'],
                    'filterable_columns': ['category', 'product'],
                    'result_columns': ['total']
                }
            }
        )

    def test_index_view(self):
        """Test main index view"""
        response = self.client.get(reverse('excel_processor:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Excel Analyzer')

    def test_get_sheets_ajax(self):
        """Test get sheets AJAX endpoint"""
        response = self.client.get(
            reverse('excel_processor:get_sheets'), 
            {'file_id': self.excel_file.id}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('sheets', data)
        self.assertEqual(data['sheets'], ['Sheet1'])

    def test_get_sheets_without_file_id(self):
        """Test get sheets without file ID"""
        response = self.client.get(reverse('excel_processor:get_sheets'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_analytics_view(self):
        """Test analytics view"""
        response = self.client.get(reverse('excel_processor:analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Analytics')


class QueryLogTest(TestCase):
    """Test QueryLog model"""

    def setUp(self):
        self.excel_file = ExcelFile.objects.create(name="Test File")

    def test_query_log_creation(self):
        """Test creating a QueryLog"""
        query_log = QueryLog.objects.create(
            excel_file=self.excel_file,
            sheet_name='Sheet1',
            filters_applied={'category': 'A'},
            result_found=True,
            result_data={'total': 100}
        )

        self.assertEqual(query_log.excel_file, self.excel_file)
        self.assertTrue(query_log.result_found)
        self.assertEqual(query_log.result_data['total'], 100)
