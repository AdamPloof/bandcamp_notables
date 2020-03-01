# bandcamp_notables
A tool for tracking stats of notable albums on Bandcamp

This is a simple Python script for scraping info on the albums found under the New and Notable section of 
[Bandcamp](http://bandcamp.com). It makes use of Selenium and BeautifulSoup4 for navigating the web and parsing HTML.

The data gathered here isn't really all that interesting in and of itself, but I needed data for a separate PHP project
and figured it'd be more interesting to gather something original instead of using some dummy database.

This script gathers
  * artist name
  * album title
  * hometown of artist
  * link to album
  * album price
  * currency of that price
  * whether the artist is affiliated with a label
  * label name
  * date collected
  
  Feel free to copy and adapt to your own web scraping needs.
