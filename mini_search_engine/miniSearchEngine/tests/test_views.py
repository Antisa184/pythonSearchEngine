from urllib.parse import urlencode

from django.urls import reverse


from ..models import TextRecord
from django.test import TestCase


### test_views.py
class TextRecordListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_records = 10
        for record_id in range(number_of_records):
            TextRecord.objects.create(record=f"Record number {record_id+1}")

    def test_url_exists(self):
        response = self.client.get("/textRecords/")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('textRecords'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('textRecords'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_text_records.html')

    def test_view_details_of_existing_record(self):
        response = self.client.get("/textRecords/details/1")
        self.assertEqual(response.status_code, 200)

    def test_view_details_of_non_existing_record(self):
        response = self.client.get("/textRecords/details/00000000")
        self.assertRedirects(response, reverse('doesNotExist'),status_code=302, target_status_code=404)

    def test_adding_new_record(self):
        TextRecord.objects.create(record='New record')
        response = self.client.get("/recordAdded/11")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/textRecords/details/11")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1>11. New record</h1>')
        self.assertNotContains(response, '<h1>12. New record</h1>')

    def test_updating_latest_record(self):
        response = self.client.get("/updateRecord/10")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="Record number 10')
        data=urlencode({
            'record':"Updated value"
        })
        post = self.client.post("/updateRecord/10", data, content_type="application/x-www-form-urlencoded")
        response = self.client.get("/updateRecord/10")
        self.assertNotContains(response, 'value="Record number 10')
        self.assertContains(response, 'value="Updated value')