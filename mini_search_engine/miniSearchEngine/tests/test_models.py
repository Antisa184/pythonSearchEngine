from ..models import TextRecord
from django.test import TestCase

# models test
class TextRecordTest(TestCase):
    def create_text_record(self, record="New text record"):
        return TextRecord.objects.create(record=record)

    def test_text_record_creation(self):
        t = self.create_text_record()
        self.assertTrue(isinstance(t, TextRecord))
        self.assertEqual(t.record, "New text record")