# In some app's views.py (e.g. backend/app/views.py)

from django.http import JsonResponse
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from pathlib import Path
import base64

def jwks_view(request):
    public_key_pem = (Path(__file__).resolve().parent.parent / 'public_key.pem').read_bytes()
    
    public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
    public_numbers = public_key.public_numbers()

    e_val = public_numbers.e
    n_val = public_numbers.n

    # Convert int -> bytes -> base64url
    def to_base64url(num: int) -> str:
        b = num.to_bytes((num.bit_length() + 7)//8, byteorder='big')
        return base64.urlsafe_b64encode(b).rstrip(b'=').decode('ascii')

    jwk = {
        "kty": "RSA",
        "alg": "RS256",
        "use": "sig",
        "n": to_base64url(n_val),
        "e": to_base64url(e_val),
    }

    return JsonResponse({"keys": [jwk]})
