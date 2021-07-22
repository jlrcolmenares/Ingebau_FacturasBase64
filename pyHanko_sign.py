from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers, general, timestamps
from pyhanko.sign.fields import SigSeedSubFilter
from pyhanko_certvalidator import ValidationContext

# Load signer key material from PKCS#12 file
# This assumes that any relevant intermediate certs are also included
# in the PKCS#12 file.
signer = signers.SimpleSigner.load_pkcs12(
    pfx_file='PRUEBAS_ESPJ_ACTIVO.p12', passphrase=b'1234'
)

# Set up a timestamping client to fetch timestamps tokens
timestamper = timestamps.HTTPTimeStamper(
    url='http://timestamp.entrust.net/TSS/RFC3161sha2TS'
)

# Settings for PAdES-LTA
signature_meta = signers.PdfSignatureMetadata(
    field_name='Sig1', md_algorithm='sha256',
    # Mark the signature as a PAdES signature
    subfilter=SigSeedSubFilter.PADES,
    # We'll also need a validation context
    # to fetch & embed revocation info.
    validation_context=ValidationContext(allow_fetching=True),
    # Embed relevant OCSP responses / CRLs (PAdES-LT)
    embed_validation_info=True,
    # Tell pyHanko to put in an extra DocumentTimeStamp
    # to kick off the PAdES-LTA timestamp chain.
    use_pades_lta=True
)

with open('pdf.pdf', 'rb') as inf:
    w = IncrementalPdfFileWriter(inf)
    with open('pdf_pyhankoAPI.pdf', 'wb') as outf:
        signers.sign_pdf(
            w, signature_meta=signature_meta, signer=signer,
            timestamper=timestamper, output=outf
        )