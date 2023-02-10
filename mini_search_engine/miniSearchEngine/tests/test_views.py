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
        self.assertContains(response, '11. New record')
        self.assertNotContains(response, '12. New record')

    def test_record_added_redirect(self):
        response= self.client.post("/newRecord/", data={'record':"New Record"})
        self.assertRedirects(response, reverse('recordAdded', kwargs={'id':11}), status_code=302, target_status_code=200)

    def test_updating_latest_record(self):
        response = self.client.get("/updateRecord/10")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="Record number 10')
        data=urlencode({
            'record':"Updated value"
        })
        self.client.post("/updateRecord/10", data, content_type="application/x-www-form-urlencoded")
        response = self.client.get("/updateRecord/10")
        self.assertNotContains(response, 'value="Record number 10')
        self.assertContains(response, 'value="Updated value')

    def test_deleting_latest_record(self):
        response = self.client.get('/textRecords/details/10')
        self.assertEqual(response.status_code, 200)
        self.client.get('/deleted/10')
        response = self.client.get('/textRecords/details/10')
        self.assertRedirects(response, reverse('doesNotExist'),status_code=302, target_status_code=404)
        response = self.client.get(reverse('textRecords'))
        self.assertNotContains(response, 'Record number 10')

    def test_searching_records(self):
        response = self.client.get("/searchResults/")
        self.assertContains(response, '10 search results')
        response = self.client.get("/searchResults/number%2010")
        self.assertContains(response, '1 search result')
        self.assertNotContains(response, '1 search results')
        TextRecord.objects.create(record='New record')
        response = self.client.get("/searchResults/New")
        self.assertContains(response, 'New')
        self.assertContains(response, '1 search result')