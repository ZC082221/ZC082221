# doc_manager/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test # user_passes_test might be used later
from django.contrib.auth.models import Group # For checking group membership
from django.http import HttpResponse # For simple messages or errors
from .forms import SopForm, SopStepFormSet, KanbanCardForm
from django.conf import settings # Keep existing imports
import os # Keep existing imports

# register, dashboard, create_sop, create_kanban_card views remain
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'doc_manager/register.html', {'form': form})

@login_required
def dashboard(request):
    search_query = request.GET.get('search', '')
    selected_tags = request.GET.getlist('tags')
    print(f"Dashboard access: Search Query='{search_query}', Selected Tags='{selected_tags}'")
    available_tags_for_ui = [{'name': 'Urgent', 'id': '1'}, {'name': 'Production', 'id': '2'}, {'name': 'QA', 'id': '3'}]
    return render(request, 'doc_manager/dashboard.html', {
        'sop_list': [], 'kanban_list': [], 'search_query': search_query,
        'selected_tags_from_query': selected_tags, 'available_tags_for_ui': available_tags_for_ui
    })

@login_required
def create_sop(request):
    if request.method == 'POST':
        sop_form = SopForm(request.POST) # Corrected: Ensure form is instantiated for POST
        step_formset = SopStepFormSet(request.POST, request.FILES, prefix='steps') # Corrected
        if sop_form.is_valid() and step_formset.is_valid():
            sop_title = sop_form.cleaned_data['title']
            print(f"SOP Title (from form): {sop_title}")
            # Simulating step processing
            for i, step_form in enumerate(step_formset):
                if step_form.cleaned_data:
                    step_description = step_form.cleaned_data.get('step_description')
                    step_photo = step_form.cleaned_data.get('step_photo')
                    print(f"Step {i+1} Description: {step_description}")
                    if step_photo:
                        print(f"Step {i+1} Photo Filename: {step_photo.name}")
            return render(request, 'doc_manager/sop_creation_result.html', {
                'item_name': sop_title,
                'item_type': "SOP",
                'details': "Processed (Not Saved). Step details printed to console.",
                'qr_code_url': None,
                'qr_data': "No QR Data (feature skipped due to library installation issue)"
            })
    else:
        sop_form = SopForm()
        step_formset = SopStepFormSet(prefix='steps')
    return render(request, 'doc_manager/sop_form.html', {
        'sop_form': sop_form, 'step_formset': step_formset, 'form_title': 'Create New SOP'})


@login_required
def create_kanban_card(request):
    if request.method == 'POST':
        form = KanbanCardForm(request.POST, request.FILES) # Corrected
        if form.is_valid():
            title = form.cleaned_data['title']
            part_number = form.cleaned_data.get('part_number', '') # Example of capturing other fields
            item_description = form.cleaned_data.get('item_description', '')
            quantity = form.cleaned_data.get('quantity', None)
            barcode_data = form.cleaned_data.get('barcode_data', '')
            photo = form.cleaned_data.get('photo')
            print(f"Kanban Card Title: {title}")
            print(f"Part Number: {part_number}")
            print(f"Item Description: {item_description}")
            print(f"Quantity: {quantity}")
            print(f"Barcode Data: {barcode_data}")
            if photo: print(f"Photo Filename: {photo.name}")
            return render(request, 'doc_manager/sop_creation_result.html', {
                'item_name': title,
                'item_type': "Kanban Card",
                'details': "Processed (Not Saved). Details printed to console.",
                'qr_code_url': None,
                'qr_data': "No QR Data (feature skipped)"
            })
    else:
        form = KanbanCardForm()
    return render(request, 'doc_manager/kanban_card_form.html', {
        'form': form, 'form_title': 'Create New Kanban Card'})

# Helper function to check if user is in 'Approver' group
def is_approver(user):
    # This check might fail if the 'Approver' group was not created due to previous timeouts
    # when running `python manage.py setup_groups`
    if not user.is_authenticated: # Anonymous users can't be approvers
        return False
    try:
        return user.groups.filter(name='Approver').exists()
    except Exception as e:
        # This is a broad exception, but useful if DB connectivity is an issue,
        # which has been a theme with `manage.py` commands.
        print(f"Error checking group 'Approver' for user {user.username}: {e}. Assuming not approver.")
        return False

@login_required
# @user_passes_test(is_approver, login_url='/app/not_authorized/') # Alternative, redirects to login if test fails (or specified URL)
def approve_document_test_view(request, simulated_doc_id):
    user_is_approver = is_approver(request.user)

    # If using @user_passes_test, this explicit check might be redundant
    # but useful if we want to show a custom message on the same page
    # or if the decorator is not used.
    if not user_is_approver and request.resolver_match.url_name == 'approve_document_test':
        # If we want to enforce the restriction strictly and redirect
        # return redirect('doc_manager:not_authorized')
        # For this test, we'll allow rendering the page but show the status.
        pass


    message = f"Attempting to interact with simulated document ID: {simulated_doc_id}." # Removed extra newline

    if user_is_approver:
        action_message = f"User {request.user.username} IS in the 'Approver' group. Approval action would be recorded here."
        print(f"Simulated approval: User {request.user.username} for doc {simulated_doc_id}")
    else:
        action_message = f"User {request.user.username} IS NOT in the 'Approver' group. Approval denied."
        print(f"Simulated approval attempt DENIED: User {request.user.username} for doc {simulated_doc_id} (not an approver)")

    return render(request, 'doc_manager/approval_test_result.html', {
        'simulated_doc_id': simulated_doc_id,
        'user_is_approver': user_is_approver,
        'action_message': action_message,
        'message': message
    })

@login_required # Or remove if it should be accessible to anonymous users trying to access restricted areas
def not_authorized_view(request):
    return render(request, 'doc_manager/not_authorized.html')
