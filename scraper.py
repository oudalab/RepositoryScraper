from bs4 import BeautifulSoup
import urllib
import time
import os

#for i in range(20):
	#newSoup = BeautifulSoup(urllib.urlopen('https://repository.ou.edu/islandora/object/oku%253Ahos?page=' + str(i)))
	#print newSoup.prettify()
	#time.sleep(2)

def scrapePage(url, pageNum):
	soup = BeautifulSoup(urllib.urlopen(url + str(pageNum)), "lxml")

	for thumb in soup.select(".islandora-basic-collection-thumb > a"):
		escapedName = thumb["title"].replace(" ", "-")
		newimagepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", escapedName)
		if not os.path.exists(newimagepath):
			os.makedirs(newimagepath)		

		scrapeBook("https://repository.ou.edu" + thumb["href"] + "/pages?page=", 0, escapedName)
		print "Scraping page of books"

	if soup.find("a", text="next"):
		time.sleep(3)
		print "Found next page of books"
		pageNum += 1
		scrapePage(url, pageNum)

def scrapeBook(url, pageNum, bookName):
	soup = BeautifulSoup(urllib.urlopen(url + str(pageNum)), "lxml")

	for thumb in soup.select(".islandora-object-thumb > a"):
		title = thumb["title"].replace(" ", "-")
		child = thumb.findChildren()[0]
		thumbUrl = child["src"]
		print "Scraping /images/" + bookName + "/" + title + ".jpg"
		urllib.urlretrieve(thumbUrl, os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", bookName, title + ".jpg"))
		#print thumbUrl

	if soup.find("a", text="next"):
		time.sleep(1)
		print "Found next page"
		pageNum += 1
		scrapeBook(url, pageNum, bookName)
		

imagepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

if not os.path.exists(imagepath):
    os.makedirs(imagepath)

scrapePage("https://repository.ou.edu/islandora/object/oku%253Ahos?page=", 0)
#scrapeBook("https://repository.ou.edu/uuid/641949b1-d13d-5821-b238-ae774c4e078f/pages?page=", 0, "An-Astronomical-Catechism")
