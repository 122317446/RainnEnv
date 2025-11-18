import csv 
from PyPDF2 import PdfReader

class FileReader:

    @staticmethod
    def read_file(file_path):
        if file_path.endswith(".pdf"):
            return FileReader.read_pdf(file_path)
        elif file_path.endswith(".txt"):
            return FileReader.read_txt(file_path)
        elif file_path.endswith(".csv"):
            return FileReader.read_csv(file_path)
        else:
            return "[Unsupported file type]"

    @staticmethod
    #This is how using PyPDF2 can enable Rainn to read pdf files
    #Basically a text extractor which is added into a var (or array) combined with breaks using \n
    def read_pdf(path):
        reader = PdfReader(path)
        return "".join(page.extract_text() or "" for page in reader.pages)

    #This is a simple command for reading txt files (within your project directory)
    @staticmethod
    def read_txt(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    #Utilising csv in order to read excel spreadsheets, in later iterations need to have a function to convert them automatically
    @staticmethod
    def read_csv(path):
        rows = []
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(", ".join(row))
        return "\n".join(rows)

