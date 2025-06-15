import ollama
import fitz

model = "llama3.3:latest"

file_route = input("Enter PDF file route: ")
file_route = fr'{file_route}'

doc = fitz.open(file_route)

pdf_text = ""
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    pdf_text += f"\n--- Page {page_num + 1} ---\n{text}"

print("\nPDF Text Extracted:\n" + "-" * 40)
print(pdf_text[:1000])  

question = input("\nWhat do you want to ask about the PDF?: ")

prompt = f"""
You are an assistant that reads PDF documents and answers questions based on the content.
Here is the content of the PDF:
{pdf_text}

Question: {question}

Answer the question using only the information in the document.
"""

try:
    response = ollama.generate(model=model, prompt=prompt)
    generated_text = response.get("response", "")
    print("\nAnswer:\n" + generated_text)
except Exception as e:
    print("An error occurred:", e)
