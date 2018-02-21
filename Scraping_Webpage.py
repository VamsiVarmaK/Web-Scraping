#Coz my weekend has yet postponed again!

#Let's scrape a page and try scraping multiple pages from it.

from bs4 import BeautifulSoup as bs
import urllib.request
import csv

r = urllib.request.urlopen("https://ssearch.oreilly.com/?q=python").read()

soup = bs(r, "lxml")

#print(soup)

#finding all titles
Book_titles = soup.find_all("p", class_="title")
#print (Book_titles)

#Creating empty dict
books = {}
for book in Book_titles:
    books = {}

#inserting values
count=1
for book in Book_titles:
    books[count] = book.a.get_text()
    count +=1

#Stripping and cleaning the values
for k,v in books.items():
   books[k] = v.replace('\n', '').replace(' ', '')

#listing books
book_list = list(books.values())
#book_list

#dates
Book_dates = soup.find_all("p", class_="note date2")
#Book_dates

#dict
dates={}
count=0
for data in Book_dates:
    dates[count] = data.text
    count+=1

#cleaning
for k,v in dates.items():
    dates[k] = v.replace(' ', '').replace('\r', '').replace('\n', '' ).replace('ReleaseDate:','')

#listing dates
date_list = list(dates.values())

#book authors
Book_authors = soup.find_all("p", class_="note")
#Book_authors

#dict authors
authors = {}
count = 1
for author in Book_authors:
    if("By" in author.text.strip()):
        authors[count] = author.text
        count+=1
#cleaning
for k,v in authors.items():
    authors[k] = v.replace("By ", "")

#authors list
authors_list = list(authors.values())

#publishers
Book_publishers = soup.find_all("p", class_="note publisher")
#Book_publishers

#dict publishers
publishers = {}
count = 1
for publisher in Book_publishers:
    if(count==11):
        publishers[count] = "NA"
        count+=1
        continue
    publishers[count] = publisher.text
    count+=1

#cleaning
for k,v in publishers.items():
    publishers[k] = v.replace("Publisher: ", "")

#listing publishers
publishers_list = list(publishers.values())
publishers_list.append("O'Reilly Media")

#links for page info
links = {}
count=0
ram = soup.find_all("p", class_="title")
for link in ram:
    links[count]=ram[count].a["href"]
    count+=1
links

#Now to make the things even more interesting, Let's try swithching pages and scrape information
#Getting and storing page_info
page_info = []
for a in range(len(links)):
    temp = urllib.request.urlopen(links[a]).read()
    soup_temp = bs(temp, "lxml")
    page = soup_temp.find('section', id="publisher-release-length")
    if(page==None):
        page_info.append("NA")
        continue
    page_clean = str(page.find(text="Pages:").parent.parent)
    page_info.append(page_clean.replace("<p>","").replace("<strong>","").replace("Pages:","").replace("</strong>","").replace("</p>",""))


#Writing csv
with open("/Users/vamsi/Desktop/beauty.csv", "w") as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["S.No","Title", "Author", "Date","Publisher","Pages"])
    for a in range(len(book_list)):
        writer.writerow([ a+1,book_list[a], authors_list[a],date_list[a],publishers_list[a],page_info[a]])
