# doc_manager/forms.py
from django import forms

class SopStepForm(forms.Form): # From previous step
    step_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}), required=False)
    step_photo = forms.ImageField(required=False)

SopStepFormSet = forms.formset_factory(SopStepForm, extra=1, can_delete=True) # From previous step

class SopForm(forms.Form): # From previous step
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'size': '40'}))

class KanbanCardForm(forms.Form):
    title = forms.CharField(max_length=255, label="Kanban Card Title/Name", widget=forms.TextInput(attrs={'size': '40'}))
    part_number = forms.CharField(max_length=100, required=False)
    item_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}), required=False)
    quantity = forms.IntegerField(required=False)
    barcode_data = forms.CharField(max_length=255, required=False, label="Product Barcode Data")
    photo = forms.ImageField(required=False, label="Item Photo")
