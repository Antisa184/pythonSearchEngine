from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from .core.records import createNewRecord, updateExistingRecord, deleteExistingRecord
from .models import TextRecord
from .forms import RecordForm


def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def doesNotExist(request, exception=None):
    return render(request, '404.html', status=404)
def textRecords(request):
    records = TextRecord.objects.all().values()
    template = loader.get_template('all_text_records.html')
    context = {
        'records': records,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    try:
        record = TextRecord.objects.get(id=id)
    except:
        return redirect('doesNotExist')
    template = loader.get_template('details.html')
    context = {
        'record': record,
    }
    return HttpResponse(template.render(context,request))

def newRecord(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)

        if form.is_valid():
            newRecord = createNewRecord(record=form.cleaned_data['record'])
        return redirect('recordAdded', id=newRecord.id)
    else:
        form = RecordForm()
    template = loader.get_template('new_record.html')
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))

def updateRecord(request, id):
    if request.method == 'POST':
        form = RecordForm(request.POST)

        if form.is_valid():
            updateExistingRecord(updatedRecord=form.cleaned_data['record'], id=id)
        return redirect('details', id=id)
    else:
        existingRecord = TextRecord.objects.get(id=id)
        form = RecordForm(instance=existingRecord)
    template = loader.get_template('update_record.html')
    context = {
        'record': existingRecord,
        'form': form,
    }
    return HttpResponse(template.render(context, request))

def deleteRecord(request, id):
    deleteExistingRecord(id=id)
    template = loader.get_template('record_deleted.html')
    context={
        'id':id,
    }
    return HttpResponse(template.render(context,request))
def recordAdded(request, id):
    record = TextRecord.objects.get(id=id)
    template = loader.get_template('record_added.html')
    context = {
        'record': record,
    }
    return HttpResponse(template.render(context, request))

def searchResults(request, keyword=''):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            keyword=form.cleaned_data['record']
        return redirect('searchResults', keyword=keyword)
    else:
        form = RecordForm()
    filtered = TextRecord.objects.filter(record__icontains=keyword)
    template = loader.get_template('search_results.html')
    count = len(filtered)
    res = 'result' if count==1 else 'results'
    context = {
        'recordsFiltered':filtered,
        'keyword':keyword,
        'form':form,
        'count':count,
        'res':res
    }
    return HttpResponse(template.render(context, request))

