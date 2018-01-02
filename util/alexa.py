import base64
import json
import os
import pytz
import requests
from datetime import datetime
from datetime import timedelta
from exceptions import CertificateValidationException
from exceptions import NotConfiguredError
from exceptions import NotForMeError
from OpenSSL import crypto
from settings import ALEXA_SKILL_APPLICATION_IDS
from urllib.parse import urlparse

"""
Borrowed and modified from django-alexa - why rewrite what is open source?
https://github.com/pycontribs/django-alexa/blob/master/django_alexa/internal/validation.py
"""


def _validate_current_timestamp(value):
    """
    value - a timestamp formatted in ISO 8601 (for example, 2015-05-13T12:34:56Z).
    """
    timestamp = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    utc_timestamp = pytz.utc.localize(timestamp)
    utc_timestamp_now = pytz.utc.localize(datetime.utcnow())
    delta = utc_timestamp - utc_timestamp_now
    if abs(delta) > timedelta(minutes=2, seconds=30):
        return False
    else:
        return True


def _verify_cert_url(cert_url):
    """
    Verify the URL location of the certificate
    """
    if cert_url is None:
        return False
    parsed_url = urlparse(cert_url)
    if parsed_url.scheme == 'https':
        if parsed_url.hostname == "s3.amazonaws.com":
            if os.path.normpath(parsed_url.path).startswith("/echo.api/"):
                if parsed_url.port is None:
                    return True
                elif parsed_url.port == 443:
                    return True
    return False


def _verify_signature(request_body, signature, cert_url):
    """
    Verify the request signature is valid.
    """
    if signature is None or cert_url is None:
        return False
    if len(signature) == 0:
        return False
    cert_str = requests.get(cert_url)
    certificate = crypto.load_certificate(crypto.FILETYPE_PEM, str(cert_str.text))
    if certificate.has_expired() is True:
        return False
    if certificate.get_subject().CN != "echo-api.amazon.com":
        return False
    decoded_signature = base64.b64decode(signature)
    try:
        if crypto.verify(certificate, decoded_signature, request_body, 'sha1') is None:
            return True
    except:
        raise CertificateValidationException("Error occured during signature validation", {"error": 400})
    return False


def validate_alexa_request(request_headers, request_body):
    """
    Validates this is a valid alexa request, we raise if we find an issue,
    otherwise, we return True
    """

    # first things first, is alexa skill app id set up?
    if not ALEXA_SKILL_APPLICATION_IDS:
        raise NotConfiguredError("Alexa Skills application id not set up")

    json_body = json.loads(request_body)
    timestamp = json_body['request']['timestamp']
    # For each of the following errors, the alexa service expects an HTTP error code. This isn't well documented.
    # I'm going to return 403 forbidden just to be safe (but need to pass a message to the custom error handler,
    # hence why I'm adding an argument when raising the error)
    if _verify_cert_url(request_headers.get('Signaturecertchainurl')) is False:
        raise CertificateValidationException("Invalid Certificate Chain URL")
    if _verify_signature(request_body, request_headers.get('Signature'), request_headers.get('Signaturecertchainurl')) is False:
        raise CertificateValidationException("Invalid Request Signature")
    if _validate_current_timestamp(timestamp) is False:
        raise CertificateValidationException("Invalid Request Timestamp")

    # ok, the scariest things are over, let's look in to whether this was
    # actually for our application:
    try:
        application_id = json_body['context']['System']['application']['applicationId']
    except KeyError:
        raise CertificateValidationException("Could not find applicationId in "
                                             "request body")

    if application_id not in ALEXA_SKILL_APPLICATION_IDS:
        raise NotForMeError(
            "{0} is not one of the valid alexa skills application ids for "
            "this service".format(application_id)
        )

    return True
