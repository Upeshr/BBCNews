from flask import Flask, render_template, request, send_file, make_response, session
import requests
from bs4 import BeautifulSoup
import openpyxl
import io

app = Flask(__name__)
app.secret_key = "mysecretkey123"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scrape", methods=["POST"])
def scrape():
    url = request.form["url"]
    
    if not url.startswith("http"):
        url = "http://" + url  # Append http if not present
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("title").text if soup.find("title") else "No Title"
        headings = [h.text.strip() for h in soup.find_all("h1")]

        paragraphs = []
        for p in soup.find_all("p"):  # Limit to first 10 paragraphs
            text = p.text.strip()
            if len(text) > 5:
                paragraphs.append(text)
        paragraphs = paragraphs[:10]  # Limit to first 10 paragraphs

        books = []
        for book in soup.find_all("article", class_="product_pod"):
            book_title = book.h3.a["title"]
            book_price = book.find("p", class_="price_color").text.strip()
            books.append(f"{book_title} - {book_price}")
        books = books[:20]  # Limit to first 20 books

        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href and href != "#" and href != "/":
                if href.startswith("http"):
                    links.append(href)
                else:  # Relative links
                    links.append(url +"/" + href)

        links = links[:20]  # Limit to first 20 links

        session["url"] = url
        session["title"] = title
        session["headings"] = headings
        session["paragraphs"] = paragraphs
        session["books"] = books
        session["links"] = links

        return render_template("results.html", url=url, title=title, headings=headings, paragraphs=paragraphs, books=books, links=links)

    except Exception as e:
        return render_template("index.html", error=f"Error {str(e)}")
    except Exception as e:
        return render_template("index.html", error=f"An error occurred: {str(e)}")

@app.route("/download", methods=["POST"])
def download():
    url = session.get("url", "")
    title = session.get("title", "")
    headings = session.get("headings", [])
    paragraphs = session.get("paragraphs", [])
    links = session.get("links", [])

    print("URL:", url)
    print("Title:", title)
    print("Headings:", headings)
    print("Paragraphs:", paragraphs)
    print("Links:", links)

    try:# Create Excel workbook and populate with data
        wb = openpyxl.Workbook()
    
        sheet1 = wb.active
        sheet1.title = "Summary"
        sheet1.cell(row=1, column=1).value = "URL"
        sheet1.cell(row=1, column=2).value = url
        sheet1.cell(row=2, column=1).value = "Title"
        sheet1.cell(row=2, column=2).value = title

        sheet2 = wb.create_sheet("Headings")
        sheet2.cell(row=1, column=1).value = "Headings"
        for i, heading in enumerate(headings, start=2):
            sheet2.cell(row=i, column=1).value = str(heading)
            print(f"Writing heading row {i}:", heading)

        sheet3 = wb.create_sheet("Paragraphs")
        sheet3.cell(row=1, column=1).value = "Paragraphs"
        for i, paragraph in enumerate(paragraphs, start=2):
            sheet3.cell(row=i, column=1).value = str(paragraph)
            print(f"Writing paragraph row {i}:", paragraph)

        sheet4 = wb.create_sheet("Links")
        sheet4.cell(row=1, column=1).value = "Links"
        for i, link in enumerate(links, start=2):
            sheet4.cell(row=i, column=1).value = link
            print(f"Writing link row {i}:", link)
        print("Excel workbook created successfully.")

        sheet5 = wb.create_sheet("Books")
        sheet5.cell(row=1, column=1).value = "Books Title"
        sheet5.cell(row=1, column=2).value = "Price"
        books = session.get("books", [])
        for i, book in enumerate(books, start=2):
            parts = book.split(" - ")
            sheet5.cell(row=i, column=1).value = parts[0] 
            if len(parts) > 1:
                sheet5.cell(row=i, column=2).value = parts[0]
                if len(parts) > 1:
                    sheet5.cell(row=i, column=2).value = parts[1]   

        # Create in-memory binary stream for the Excel file
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        response = make_response(output.getvalue())
        response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        response.headers["Content-Disposition"] = "attachment; filename=scraped_data.xlsx"
        return response

    except Exception as e:
        print("EXCEL ERROR:", str(e))
        return "Error creating Excel: " + str(e)

if __name__ == "__main__":
    app.run(debug=True)  