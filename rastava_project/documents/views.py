from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .access_token import TokenManager
from docusign_esign import EnvelopesApi, ApiClient, EnvelopesApi, EnvelopeDefinition, Document, Signer, CarbonCopy, SignHere, Tabs, \
    Recipients
from docusign_esign.client.api_exception import ApiException
from django.conf import settings
import requests
import json
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .forms import ContractForm
from .models import Contract
from .docusign_service import DocuSignService  # Handles DocuSign API interactions
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContractForm
from .models import Contract

#Token Manager Creation
token_manager = TokenManager()

base_path = settings.DOCUSIGN_BASE_URL
client_id = settings.USER_ID
integration_key = settings.INTEGRATION_KEY
client_secret = settings.DOCUSIGN_SECRET_KEY
redirect_uri = settings.DOCUSIGN_REDIRECT_URI
authorization_url = f'https://account-d.docusign.com/oauth/auth?response_type=code&scope=signature&client_id={client_id}&redirect_uri={redirect_uri}'
authorization_code = ''
token_url = 'https://account-d.docusign.com/oauth/token'


def instantiate_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            recipient_name = form.cleaned_data['recipient_name']
            recipient_email = form.cleaned_data['recipient_email']
            # signing_place = form.cleaned_data['signing_place']

            try:
                # Create Contract in DB
                contract = Contract.objects.create(
                    user=request.user,
                    recipient_email=recipient_email
                )

                # Initialize DocuSign service (handles token refresh)
                docusign = DocuSignService()
                print("\n\n", "user name, emal, recipient name" , "\n\n")
                print("\n\n", request.user.get_full_name(), request.user.email, recipient_name, recipient_email , "\n\n")
                # Send envelope to DocuSign
                envelope_id = docusign.create_envelope(
                    user=request.user,
                    recipient_email=recipient_email,
                    recipient_name=recipient_name,  # Dynamic recipient name
                    # signing_place=signing_place  # Dynamic signing place
                )

                # Update contract details in DB
                contract.contract_id = envelope_id
                print("\n\n", "envelop_id", envelope_id, "\n\n")
                contract.status = "Sent"
                contract.save()

                # Redirect to sign contract view
                return redirect('sign_contract', envelope_id=envelope_id)

            except Exception as e:
                print("Error sending envelope to DocuSign:", str(e))
                form.add_error(None, "Failed to send contract to DocuSign. Please try again.")

    else:
        form = ContractForm()

    return render(request, 'documents/instantiation.html', {'form': form})


def sign_contract(request, envelope_id):
    """
    Direct the user to the DocuSign signing URL.
    """
    docusign = DocuSignService()
    signing_url = docusign.get_recipient_view(envelope_id, request.user)

    if signing_url:
        return redirect(signing_url)
    return HttpResponse("Failed to retrieve the signing link.", status=500)


def home(request):
    # access_token = token_manager.get_access_token()
    # api_client = create_api_client(base_path=base_path, access_token=access_token)
    # context = {}
    return render(request, 'documents/index.html', context={})


def success(request):
    """
    Display a success message after signing the document.
    """
    return render(request, 'documents/success.html')

