
# %%
import base64
import os

# %%
# FROM PDF TO BASE64
for bill in os.listdir("./Facturas_PDF/"):
    name = bill[:-4]
    #print(name)
    with open(f"./Facturas_PDF/{bill}", "rb") as pdf_file: 
        # Tranform to base64
        b64_string = base64.b64encode(pdf_file.read())
        # Write Base64 
        with open(f"./de_PDF_a_Base64/{name}", "wb") as bytes_string:
            bytes_string.write(b64_string) # imprimimos en base64
            #bytes_string.write(base64.decodebytes(b64_string))
            bytes_string.close()


# %%
# FROM BASE64 TO PDF
for file in os.listdir("./de_PDF_a_Base64/"):
    name = file[:-4]
    with open(f"./de_PDF_a_Base64/{file}", "rb") as bytes_string:
        #text_content = bytes_string.read()
        text_content = base64.b64decode(bytes_string.read(), validate=True)
        # Perform a validation
        #if b64_string[0:4] != b'%PDF':
        #    raise ValueError("Missing the PDF file signature")
        # Write PDF
        with open(f"./de_Base64_a_PDF/{file}.pdf", 'wb') as pdf_file:
            pdf_file.write(text_content)
            pdf_file.close()
    

# %%
