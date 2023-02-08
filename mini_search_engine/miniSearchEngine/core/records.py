from ..models import TextRecord

def createNewRecord(record):
    newRecord = TextRecord(record=record)
    newRecord.save()
    return newRecord

def updateExistingRecord(updatedRecord, id):
    record = TextRecord.objects.get(id=id)
    record.record = updatedRecord
    record.save()