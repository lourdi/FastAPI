from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List
import camelot
import os

app = FastAPI()

@app.post("/pdf-to-csv/")
async def pdf_to_csv(files: List[UploadFile]):
    csv_files = []

    for uploaded_file in files:
        try:
            # Save the uploaded PDF file temporarily
            with open("temp.pdf", "wb") as pdf_file:
                pdf_file.write(uploaded_file.file.read())

            # Use Camelot-Py to extract tables from the PDF
            tables = camelot.read_pdf("temp.pdf")

            # Convert each table to CSV
            for i, table in enumerate(tables):
                csv_file_path = f"table_{i + 1}.csv"
                table.to_csv(csv_file_path)
                csv_files.append(csv_file_path)

            return JSONResponse(content={"success": "PDF to CSV conversion successful", "csv_files": csv_files})

        except Exception as e:
            return JSONResponse(content={"error": str(e)})
        finally:
            # Remove the temporary PDF file
            os.remove("temp.pdf")

