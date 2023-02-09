from ..models import TextRecord
from ..forms import RecordForm
from django.test import TestCase

#forms test
class RecordFormTest(TestCase):
    def test_valid_form(self):
        t = TextRecord.objects.create(record='foo')
        data = {'record': t.record,}
        form = RecordForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        longString="############################################################################################################################################################################################################################################################################################################"
        t = TextRecord.objects.create(record=longString)
        data = {'record': t.record, }
        form = RecordForm(data=data)
        self.assertFalse(form.is_valid())