import base64
import os

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

    for file in os.listdir(input_folder):
        try:
            with open(f"{input_folder}/{file}", "rb") as bytes_string:
                text_content = base64.b64decode(bytes_string.read(), validate=True)
            # Perform a validation
            if text_content[0:4] != b'%PDF':
                raise ValueError("Missing the PDF file signature")
            # Write PDF
            with open(f"{output_folder}/{file}.pdf", 'wb') as pdf_file:
                pdf_file.write(text_content)
                pdf_file.close()
        except ValueError as ex:
            print(ex)
        

if __name__ == "__main__":

    initial_folder = "./tests/"
    output_folder = "./Facturas_PDF/"
    PDF_to_b64( initial_folder, output_folder)
    
    #input_folder = "./de_PDF_a_Base64/"
    #output_folder = "./de_Base64_a_PDF/"
    #b64_to_PDF( input_folder, output_folder)