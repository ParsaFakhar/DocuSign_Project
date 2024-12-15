import requests
from .access_token import TokenManager
from django.conf import settings
from .Contract_Generator import generate_contract_pdf, convert_pdf_to_base64
import os
from docusign_esign import EnvelopesApi

base64file = "JVBERi0xLjMKJZOMi54gUmVwb3J0TGFiIEdlbmVyYXRlZCBQREYgZG9jdW1lbnQgaHR0cDovL3d3dy5yZXBvcnRsYWIuY29tCjEgMCBvYmoKPDwKL0YxIDIgMCBSIC9GMiAzIDAgUiAvRjMgNCAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL0Jhc2VGb250IC9IZWx2ZXRpY2EgL0VuY29kaW5nIC9XaW5BbnNpRW5jb2RpbmcgL05hbWUgL0YxIC9TdWJ0eXBlIC9UeXBlMSAvVHlwZSAvRm9udAo+PgplbmRvYmoKMyAwIG9iago8PAovQmFzZUZvbnQgL0hlbHZldGljYS1Cb2xkIC9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nIC9OYW1lIC9GMiAvU3VidHlwZSAvVHlwZTEgL1R5cGUgL0ZvbnQKPj4KZW5kb2JqCjQgMCBvYmoKPDwKL0Jhc2VGb250IC9IZWx2ZXRpY2EtT2JsaXF1ZSAvRW5jb2RpbmcgL1dpbkFuc2lFbmNvZGluZyAvTmFtZSAvRjMgL1N1YnR5cGUgL1R5cGUxIC9UeXBlIC9Gb250Cj4+CmVuZG9iago1IDAgb2JqCjw8Ci9Db250ZW50cyA5IDAgUiAvTWVkaWFCb3ggWyAwIDAgNDAwIDYwMCBdIC9QYXJlbnQgOCAwIFIgL1Jlc291cmNlcyA8PAovRm9udCAxIDAgUiAvUHJvY1NldCBbIC9QREYgL1RleHQgL0ltYWdlQiAvSW1hZ2VDIC9JbWFnZUkgXQo+PiAvUm90YXRlIDAgL1RyYW5zIDw8Cgo+PiAKICAvVHlwZSAvUGFnZQo+PgplbmRvYmoKNiAwIG9iago8PAovUGFnZU1vZGUgL1VzZU5vbmUgL1BhZ2VzIDggMCBSIC9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iago3IDAgb2JqCjw8Ci9BdXRob3IgKGFub255bW91cykgL0NyZWF0aW9uRGF0ZSAoRDoyMDI0MTIxNjAwMTAyOCswMycwMCcpIC9DcmVhdG9yIChSZXBvcnRMYWIgUERGIExpYnJhcnkgLSB3d3cucmVwb3J0bGFiLmNvbSkgL0tleXdvcmRzICgpIC9Nb2REYXRlIChEOjIwMjQxMjE2MDAxMDI4KzAzJzAwJykgL1Byb2R1Y2VyIChSZXBvcnRMYWIgUERGIExpYnJhcnkgLSB3d3cucmVwb3J0bGFiLmNvbSkgCiAgL1N1YmplY3QgKHVuc3BlY2lmaWVkKSAvVGl0bGUgKHVudGl0bGVkKSAvVHJhcHBlZCAvRmFsc2UKPj4KZW5kb2JqCjggMCBvYmoKPDwKL0NvdW50IDEgL0tpZHMgWyA1IDAgUiBdIC9UeXBlIC9QYWdlcwo+PgplbmRvYmoKOSAwIG9iago8PAovRmlsdGVyIFsgL0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlIF0gL0xlbmd0aCA2NTIKPj4Kc3RyZWFtCkdhdCVgOWknTS8mO0taT01Xa1IiUGg3PE4uQ1UpQHAoL0Y0MyZkWEo9XG07OHJAbiwicVhaZGE0IV8xaSJnSl1aVVI+Y09HczEiKDE7PD5RPSkqOCgtJmZWJU87Q2FtTDN0YkY1ZTJEakguJ1w/TmpTP0BCXCg1MVthTlxUK24mUiMpLWxhQWU4VF9OOWxORSdwZl1hSU5AKC9dcSNvZ0I9IW1bYT4lWSYqWmsoOz87IypYJ2AiaUVba0MrPl9qbT8mQ0FtT044M24tRVNOdUJMS1g5MjYhS1o3dSYwSE9mQCYwNlJhKVkwJWIlQihaYEo+WEU0Tj4yTnIuPSxoXSNjSlxzUEVBZ0EnajUmVVRZcHJBIzdPbVIiPitANTVVXnI9QFxDXTlDVSIxckwsPFpKOiRLdDNoWzRjQWNdUlRLZWQhIUFeZCUkLiJWSmZvTGU3dCpEOmIzUjVgX1oqWXA8KzpDOSoxMFY/JSRJN2U5SGJGLDc0NnE5X0YkUyJyV29KM1lhWFcxRFVQXmdaOW0mUFt0PlNgZGVIPE8jdUdhUmNYZEpETU1BO0NedFojUFs4UUdBPjUxb11pWyE0UFFdbDJzXSNiRyduQ3RNciddLyg4UVwwYEp1bWw+bXBeW0Y0TzxbWnMlWkdhSjIpcm8jSWBmLVReJS1GTjxwakNraWZNXFVLJHMuZGtXY2k3SHI2RUU7VF4vJTk2UWViKjRZKjA/SyJjY1UqMmI4XigvVDcrcixEMTpnNCQ3M0lFSSEscWZWdU43Xj4nQVFHSiUsKFBBbmJEX04yQio/WmFSW1wyIUIyXy51NkB1RXE6UE1EKmFOcjxsZyVlPUdWX3ExN1w3RzhmaU9gfj5lbmRzdHJlYW0KZW5kb2JqCnhyZWYKMCAxMAowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwNzMgMDAwMDAgbiAKMDAwMDAwMDEyNCAwMDAwMCBuIAowMDAwMDAwMjMxIDAwMDAwIG4gCjAwMDAwMDAzNDMgMDAwMDAgbiAKMDAwMDAwMDQ1OCAwMDAwMCBuIAowMDAwMDAwNjUxIDAwMDAwIG4gCjAwMDAwMDA3MTkgMDAwMDAgbiAKMDAwMDAwMTAxNSAwMDAwMCBuIAowMDAwMDAxMDc0IDAwMDAwIG4gCnRyYWlsZXIKPDwKL0lEIApbPDQ3OGIyODRmYzdiNzFlYTVhMTQ2M2ExZWFlMTEyZWU3Pjw0NzhiMjg0ZmM3YjcxZWE1YTE0NjNhMWVhZTExMmVlNz5dCiUgUmVwb3J0TGFiIGdlbmVyYXRlZCBQREYgZG9jdW1lbnQgLS0gZGlnZXN0IChodHRwOi8vd3d3LnJlcG9ydGxhYi5jb20pCgovSW5mbyA3IDAgUgovUm9vdCA2IDAgUgovU2l6ZSAxMAo+PgpzdGFydHhyZWYKMTgxNgolJUVPRgo="


class DocuSignService:
    def __init__(self):
        self.token_manager = TokenManager()
        self.base_url = 'https://demo.docusign.net/restapi'
        self.account_id = settings.API_ACCOUNT_ID  # Replace with your DocuSign Account ID

    def create_envelope(self, user, recipient_email, recipient_name):
        access_token = self.token_manager.get_access_token()

        url = f"{self.base_url}/v2.1/accounts/{self.account_id}/envelopes"
        # url2 = "https://demo.docusign.net/restapi/v2.1/accounts/b39ea592-fa62-4402-a609-49e56c5abcd5/envelopes"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        envelope_definition = {
            "emailSubject": "Please sign this document",
            "documents": [{
                "documentBase64": base64file,
                "name": "Sample Contract",
                "fileExtension": "pdf",
                "documentId": "1"
            }],
            "recipients": {
                "signers": [
                    {
                        "email": user.email,
                        "name": user.username,
                        "recipientId": "1",
                        "routingOrder": "1",
                        "tabs": {
                            "textTabs": [
                                {"anchorString": "/USRNM/", "value": user.username, "required": "true"},
                                {"anchorString": "/USREML/", "value": user.email, "required": "true"},
                                # {"anchorString": "/SignHereUser/", "value": , "required": "true"}
                            ],
                            "signHereTabs": [
                                {
                                    "anchorString": "/SignHereUser/",
                                    "anchorUnits": "pixels",
                                    "anchorXOffset": "20",
                                    "anchorYOffset": "10",
                                    "documentId": "1",
                                    "pageNumber": "1"
                                }
                            ]
                        }
                    },
                    {
                        "email": recipient_email,
                        "name": recipient_name,
                        "recipientId": "2",
                        "routingOrder": "2",
                        "tabs": {
                            "textTabs": [
                                {"anchorString": "/RCPTN/", "value": recipient_name, "required": "true"},
                                {"anchorString": "/RCPTEML/", "value": recipient_email, "required": "true"},
                                # {"anchorString": "/SignRecipient/", "value": "", "required": "true"}
                            ],
                            "signHereTabs": [
                                {"anchorString": "/SignRecipient/", "documentId": "1", "pageNumber": "1"}
                            ]
                        }
                    }
                ]
            },
            "status": "sent"
        }

        response = requests.post(url, json=envelope_definition, headers=headers)

        print("\n\n", "response: ", response, "\n\n")
        # print("\n\n", "response2: ", response2, "\n\n")
        response.raise_for_status()

        return response.json()["envelopeId"]

    def get_recipient_view(self, envelope_id, user):
        print("\n\n", "get_recipient_view" , "\n\n")
        url = f"https://demo.docusign.net/restapi/v2.1/accounts/{settings.API_ACCOUNT_ID}/envelopes/{envelope_id}/views/recipient"
        print("\n\n", url , "\n\n")
        headers = {
            "Authorization": f"Bearer {self.token_manager.get_access_token()}",
            "Content-Type": "application/json"
        }
        body = {
            "userName": user.username,
            "email": user.email,
            "recipientId": "1",
            "returnUrl": "http://127.0.0.1:8000/success",
            "authenticationMethod": "none"
        }

        response = requests.post(url, json=body, headers=headers)
        print("\n\n", "response in get recipient view", response , "\n\n")
        if response.status_code == 201:
            return response.json().get("url")
        return None
