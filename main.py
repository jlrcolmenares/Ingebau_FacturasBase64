import base64
import time
import os

from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers, general, timestamps
from pyhanko.sign.fields import SigSeedSubFilter
from pyhanko_certvalidator import ValidationContext

# SIGN PDF
def sign_pdf( input_folder, output_folder):
    """ This funtion takes all the PDF files,
    Ttransform it, and copy them in outfolder in Base64

    Args:
        input_folder ([type]): [description]
        output_path ([type]): [description]
    """
    # Some validations
    assert os.path.exists(input_folder), "INPUT folder doesn't exist"
    assert os.path.exists(output_folder), "OUTPUT folder doesn't exist"

    for file_path in os.listdir(input_folder):
        basename = os.path.basename(file_path)
        file_name = os.path.splitext(basename)[0]
        
        signer = signers.SimpleSigner.load_pkcs12(pfx_file='PRUEBAS_ESPJ_ACTIVO.p12', passphrase=b'1234')
        timestamper = timestamps.HTTPTimeStamper(url='http://timestamp.entrust.net/TSS/RFC3161sha2TS')

        # Settings for PAdES-LTA
        signature_meta = signers.PdfSignatureMetadata(
            field_name='Sig1', md_algorithm='sha256',
            subfilter=SigSeedSubFilter.PADES,
            validation_context=ValidationContext(allow_fetching=True),
            embed_validation_info=True,
            use_pades_lta=True
        )

        with open(f"{input_folder}/{file_path}", 'rb') as inf:
            w = IncrementalPdfFileWriter(inf)
            with open(f"{output_folder}{file_path}", 'wb') as outf:
                signers.sign_pdf(
                    w, signature_meta=signature_meta, signer=signer,
                    timestamper=timestamper, output=outf
                )
                outf.close()
            inf.close()


# FROM PDF TO BASE64
def PDF_to_b64( input_folder, output_folder):
    """ This funtion takes all the PDF files,
    Ttransform it, and copy them in outfolder in Base64

    Args:
        input_folder ([type]): [description]
        output_path ([type]): [description]
    """
    # Some validations
    assert os.path.exists(input_folder), "INPUT folder doesn't exist"
    assert os.path.exists(output_folder), "OUTPUT folder doesn't exist"

    for file_path in os.listdir(input_folder):
        try:
            basename = os.path.basename(file_path)
            file_name = os.path.splitext(basename)[0]
            with open(f"{input_folder}/{file_path}", "rb") as pdf_file: 
                # Tranform to base64
                b64_string = base64.b64encode(pdf_file.read())
                # Write Base64 
                with open(f"{output_folder}/{file_name}", "wb") as bytes_string:
                    bytes_string.write(b64_string)
                    bytes_string.close() 
        except ValueError as ex:
            print(ex)


# FROM BASE64 TO PDF
def b64_to_PDF( input_folder, output_folder):
    """ This funtion takes all base64 files in a folder,
    transforme it and copy them in outfolder in PDF

    Args:
        input_folder ([type]): [description]
        output_path ([type]): [description]
    """
    # Some validations
    assert os.path.isdir(input_folder), "INPUT folder doesn't exist"
    assert os.path.isdir(output_folder), "OUTPUT folder doesn't exist"

    for file_path in os.listdir(input_folder):
        try:
            basename = os.path.basename(file_path)
            file_name = os.path.splitext(basename)[0]
            
            signer = signers.SimpleSigner.load_pkcs12(
                pfx_file='PRUEBAS_ESPJ_ACTIVO.p12', passphrase=b'1234'
            )
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

            # Sign document
            with open(f"{input_folder}/{basename}", 'rb') as inf:
                w = IncrementalPdfFileWriter(inf)
            with open(f"{input_folder}/signed-{basename}", 'wb') as outf:
                signers.sign_pdf(
                    w, signature_meta=signature_meta, signer=signer,
                    timestamper=timestamper, output=outf
                )

            # Transform signed to Base64
            with open(f"{input_folder}/signed-{basename}", "rb") as bytes_string:
                text_content = base64.b64decode(bytes_string.read(), validate=True)
            
            # Perform a validation
            if text_content[0:4] != b'%PDF':
                raise ValueError("Missing the PDF file signature")
            # Write PDF
            with open(f"{output_folder}/{file_name}.pdf", 'wb') as pdf_file:
                pdf_file.write(text_content)
                pdf_file.close()
        except ValueError as ex:
            print(ex)
        

if __name__ == "__main__":

    unsigned = "./1_Facturas_PDF/"
    signed = "./2_de_PDF_a_Firmados/"
    sign_pdf( unsigned,signed )

    
    # initial_folder = "./1_Facturas_PDF/"
    # output_folder = "./3_de_PDF_a_Base64/"
    # PDF_to_b64( initial_folder, output_folder)
    
    #input_folder = "./de_PDF_a_Base64/"
    #output_folder = "./de_Base64_a_PDF/"
    #b64_to_PDF( input_folder, output_folder)