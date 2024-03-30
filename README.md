# minimalcarbon proof of concept

minimalcarbon is compressing websites by up to 95% without compromising functionality or design.

minimalcarbon has created a technique to substantially reduce the power consumption of websites. minimalcarbon not only provides a technological solution, but also promotes awareness about the link between information and energy. The rising use of digital energy is a result of the decisions we all make on a daily basis as publishers, software developers, site designers, and Internet users.

## prototype

This prototype experiment aims to establish energy as a teachable cultural practice accessible to all. Currently, the code is in its raw form, lacking comments and refinement. However, it demonstrates the potential of compressing websites by up to 95% without compromising functionality or design.

Find a description here:
https://minimalcarbon.net/

## code
minimalcarbon.site is a pipeline of programs, mostly written in python 3.10.
After trying out several other apps (httrack, wget,...) and WordPress Plugins (simply static, WP2Static, Export WP Page to Static HTML/CSS, Staatic, Static HTML Output,..) I decided to start from scratch, since none of these apps was fit for the task or easily adaptable.

### description of the pipeline:
+ intermediate results are currently stored in csv files
+ all python code: ca 9000 lines [find . -maxdepth 1 -name '*.py' | xargs wc -l]

## apps

### app_050_sitemap_crawl: 20min

	+ crawl, extract all connected internal and external links from given URL
	
### app_150_selenium: 1h
	
	+ save all files locally with headless browser
		https://en.wikipedia.org/wiki/Headless_browser
		 they are able to render and understand HTML the same way a browser would, including styling elements such as page layout, colour, font selection and execution of JavaScript and Ajax which are usually not available.
	+ extract all links
	+ change all links so they refer to root /
	+ serve the website locally via LAMP, xampp, etc
	+ find all real image sizes in webpage on standard desktop browser
	+ extract all image- and backround-image-links from html
	
	
### app_200_images: 1h30

many of these methods are site-specific to karlsruhe.digital 	

	+ copy favicon
	+ append css to style.css
	+ append special javascript
	+ remove all font tags
	+ remove fonts from stylesheets
	+ replace fonts in tag styles 
	+ perform_pdf_compression
	+ perform_image_conversion to webp or avif, resize, color grade via lut, ...
	+ replace all conversions in files
	+ create sitemap.xml
	+ minify all css, html and js files
	+ special fixes like minimal carbon banner, percentage saved, etc
	+ remove unneeded scripts
	+ remove undesired elements like twitter etc
	+ create banner
	+ calculate difference of sizes
	+ export optimized site

## next steps

partners:

	+ need partner and scientific authority for online analysis of carbon usage per websit
	+ domestic solar panel company
		# experiment on the idea of a direct worldwide solar grid without using battery banks
	+ several international solar panel companies
		# establish a solar equator on Earth

code refactoring:

	+ dividing the code and tasks into more dedicated individual apps
	+ divide apps for general and for specific use
	+ sql database per site instead of csv
	+ faster processing of blog listings, new concepts for large blogs and re-rendering
  

# deutsch

Minimalcarbon komprimiert Websites um bis zu 95%, ohne dabei Funktionalität oder Design zu beeinträchtigen.

Minimalcarbon hat eine Technik entwickelt, um den Energieverbrauch von Websites zu reduzieren. Minimalcarbon bietet nicht nur eine technologische Lösung, sondern fördert auch das Bewusstsein für den Zusammenhang zwischen Information und Energie. 

## Prototyp

Dieses Prototypexperiment zielt darauf ab, Energie als erlernbare kulturelle Technik für alle zugänglich zu machen. Derzeit befindet sich der Code in seiner Rohform, ohne Kommentare und Verfeinerung. Dennoch zeigt er das Potenzial, Websites um bis zu 95% zu komprimieren, ohne dabei Funktionalität oder Design zu beeinträchtigen.

Eine Beschreibung gibt es hier: https://minimalcarbon.net/


