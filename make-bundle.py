#!/usr/bin/env python

# make-bundle.py: fetch the latest MS codesigning bundle from CCADB,
# munge it into a new bundle with some pretty-printed metadata

import sys

import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization

CCADB_LINK = "https://ccadb.my.salesforce-sites.com/microsoft/IncludedRootsPEMTxtForMSFT?MicrosoftEKUs=Code%20Signing"

CERT_RENDER_TEMPLATE = """
Subject: {subject}
Issuer: {issuer}
Subject Key Identifier: {ski}
Authority Key Identifier: {aki}
Not Before: {not_before}
Not After: {not_after}
{cert_pem}
"""


def get_ski(cert: x509.Certificate) -> str:
    try:
        ski = cert.extensions.get_extension_for_class(x509.SubjectKeyIdentifier)
        return ski.value.digest.hex()
    except x509.ExtensionNotFound:
        return "(none)"
    except ValueError:
        return "(invalid DER while parsing extensions)"


def get_aki(cert: x509.Certificate) -> str:
    try:
        aki = cert.extensions.get_extension_for_class(x509.AuthorityKeyIdentifier)
        if ident := aki.value.key_identifier:
            return ident.hex()
        else:
            return "(no key identifier)"
    except x509.ExtensionNotFound:
        return "(none)"
    except ValueError:
        return "(invalid DER while parsing extensions)"


def render_with_metadata(cert: x509.Certificate) -> str:
    cert_pem = cert.public_bytes(serialization.Encoding.PEM).decode()
    return CERT_RENDER_TEMPLATE.format(
        subject=cert.subject.rfc4514_string(),
        issuer=cert.issuer.rfc4514_string(),
        ski=get_ski(cert),
        aki=get_aki(cert),
        not_before=cert.not_valid_before.isoformat(),
        not_after=cert.not_valid_after.isoformat(),
        cert_pem=cert_pem,
    )


resp = requests.get(CCADB_LINK)
resp.raise_for_status()

certs = x509.load_pem_x509_certificates(resp.content)

for cert in certs:
    print(render_with_metadata(cert))
