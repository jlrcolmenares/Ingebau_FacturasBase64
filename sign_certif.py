import sys
from datetime import datetime, timedelta
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

from endesive.pdf import cms


def sign_pdf():
    date = datetime.utcnow() + timedelta(hours= 2) # useful when in AWS
    date = date.strftime("Fecha: %Y.%m.%d %H:%M:%S +02'00'")
    print(date)
    dct = {
        "aligned": 0,
        "signform" : True,
        "sigbutton": True,
        #"sigflags": 3,
        #"sigflagsft": 132,
        #"sigpage": 0,
        #"sigfield": "Signature1",
        #"signaturebox": (470, 840, 570, 640),
        # "signature_img": "signature_test.png",
        "auto_sigfield": True,
        "sigandcertify": True,
        "signature": "Ingebau",
        "contact": "pruebas@example.com",
        "location": "Sevilla",
        "signingdate": date,
        "reason": "Certified Bill from Ingebau",
        "password": "1234",
    }
    with open("PRUEBAS_ESPJ_ACTIVO.p12", "rb") as fp:
        p12 = pkcs12.load_key_and_certificates(
            fp.read(), b"1234", backends.default_backend())
    fname = "pdf.pdf" # Aqui entra cada factura
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    datain = open(fname, "rb").read()
    dataout = cms.sign(datain, dct, p12[0], p12[1], p12[2], "sha256")
    fname = fname.replace(".pdf", "-signed-cms.pdf")
    with open(fname, "wb") as fp:
        fp.write(datain)
        fp.write(dataout)

if __name__ == '__main__':
    sign_pdf()