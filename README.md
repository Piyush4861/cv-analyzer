STEP-1

- download VS code for mac
- install python extention 
- if you try to install any packages using "pip/brew install python" it will show error that pip/brew command not found
- need to setup and activate virtual environment
- setup the virtual environment to install the packages using pip
    python3 -m venv venv
    source venv/bin/activate
- now you can install using "pip install python"
- but you will not be able to installpip install tesseract-ocr
- need to upgrade the pip
    pip install -upgrade pip
- it will install/upgrade the latest version of pip
- now you can install "pip install tesseract"
- all set with the requirements

STEP-2

- assume we have pdfs/docxs stored somewhere and now the first step is to extract the information of every document
- we will create parser.py file
- start with importing the required libraries
- create function to extract text from pdf
- give pdf_path where all the pdfs are stored
- run the function and we get the extracted data in json format
- now we have completed the extraction of information from bulk cvs, now we want some frontend so that we can get cvs from the UI.
