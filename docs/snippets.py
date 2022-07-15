"""  



does not load all fonts , get rid of them


"https:\/\/karlsruhe.digital\/wp-includes\/js\/wp-emoji-release.min.js?ver=5.2.15"
https://stackoverflow.com/questions/6076229/escaping-a-forward-slash-in-a-regular-expression


https:\/\/karlsruhe.digital\/

https://github.com/beautify-web/js-beautify
pip install jsbeautifier
pip install cssbeautifier


Python script to extract URLs from HTML documents. 
https://gist.github.com/zmwangx/49049218bd89c21ddabd647896af995a

Note: The new features discussed in this article — srcset/sizes/<picture> — are all supported in modern desktop and mobile browsers (including Microsoft's Edge browser, although not Internet Explorer.)


<img srcset="elva-fairy-480w.jpg 480w,
             elva-fairy-800w.jpg 800w"
     sizes="(max-width: 600px) 480px,
            800px"
     src="elva-fairy-800w.jpg"
     alt="Elva dressed as a fairy">


Note: The new features discussed in this article — srcset/sizes/<picture> — are all supported in modern desktop and mobile browsers (including Microsoft's Edge browser, although not Internet Explorer.)


<img srcset="elva-fairy-480w.jpg 480w,
             elva-fairy-800w.jpg 800w"
     sizes="(max-width: 600px) 480px,
            800px"
     src="elva-fairy-800w.jpg"
     alt="Elva dressed as a fairy">



http:// https://is_a_real_url.yes

TODO

now python replace tags via bs4 or selenium
https://stackoverflow.com/questions/55915856/change-element-in-python-using-selenium

var = 100
js = f"arguments[0].setAttribute('value', '{var}')"
browser.execute_script(js, get_draws)


EDIT SOLVED:

Figured out how to change the value of an element. I had to change the search method of that element to this:

get_draws = browser.find_element_by_tag_name('option')

Then my next line was pretty simple:

browser.execute_script(arguments[0].setAttribute('value', '100'), get_draws)

python replace tag with selenium
https://stackoverflow.com/questions/69732483/python-selenium-find-all-css-element-and-replace-all
https://www.geeksforgeeks.org/change-the-tags-contents-and-replace-with-the-given-string-using-beautifulsoup/
https://python.tutorialink.com/i-want-to-replace-the-html-code-with-my-own/


r=requests.get('https://neculaifantanaru.com/en/qualities-of-a-leader-inner-integrity.html')
soup=BeautifulSoup(r.text, 'html.parser')

try:
    articles = soup.find_all('p', {'class':"text_obisnuit"})
    for item in articles:  

        original_text=item.text
        #print(original_text)
        translated_output=ts.google(original_text, from_language='en', to_language='ro')
        print(item)

        item.string = translated_output
            
except Exception as e:
    print(e)

# To see that it was changed
for item in articles:   
    print(item)


translated_html = str(soup)

####################

    element =driver.find_element_by_id("some-random-number")
    driver.execute_script("arguments[0].innerText = '200'", element)
    
    element =  driver.find_element_by_class_name("something");
    driver.execute_script("arguments[0].setAttribute('style', 'transition: transform 2500ms bla bla bla')", element);       


#######################


37

I do not know of a Selenium method that is designed specifically to remove elements. However, you can do it with:

element = driver.find_element_by_class_name('classname')
driver.execute_script(""
var element = arguments[0];
element.parentNode.removeChild(element);
"", element)

############################
https://stackoverflow.com/questions/22515012/python-selenium-how-can-i-delete-an-element

def excludeTagFromWebDriver(driver : WebDriver, selector : str):
    i = 0
    soup = BeautifulSoup(driver.page_source, 'html.parser') # Parsing content using beautifulsoup
    while soup.find(selector):
        # print(soup.find(selector))
        js = ""
            var element = document.querySelector("" + "'" + selector + "'" + "");
            if (element)
                element.parentNode.removeChild(element);
            ""
        driver.execute_script(js)
        soup = BeautifulSoup(driver.page_source, 'html.parser') # Parsing content using beautifulsoup
        i += 1
        # print('Removed tag with selector ' + "'" + selector + "'" + ' with nr: ', i)
    print('Removed ' + str(i) + ' tags with the selector ' + "'" + selector + "'" + " and all it's children tags.")
    return driver

driver = excludeTagFromWebDriver(driver,"sup")

###################################
        try:
            element = driver.find_element_by_xpath("//div[@class='chatContainer oldStyle']")
        driver.execute_script(""var element = arguments[0]; 
            element.parentNode.removeChild(element);"", element)
        except Exception:
            pass
##################################
chatBox = driver.find_element(By.XPATH, "//div[@class='chatContainer oldStyle']")
driver.execute_script("arguments[0].remove();", chatBox)

###################################
driver.find_element_by_id('foo').clear()

###################################

def removeOneTag(text, tag):
    return text[:text.find("<"+tag+">")] + text[text.find("</"+tag+">") + len(tag)+3:]
    
####################################
tree=et.fromstring(xml)

for bad in tree.xpath("//fruit[@state=\'rotten\']"):
  bad.getparent().remove(bad)     # here I grab the parent of the element to call the remove directly on it

print et.tostring(tree, pretty_print=True, xml_declaration=True)

###################################
import lxml.etree as et

xml=""
<groceries>
  <fruit state="rotten">apple</fruit>
  <fruit state="fresh">pear</fruit>
  <punnet>
    <fruit state="rotten">strawberry</fruit>
    <fruit state="fresh">blueberry</fruit>
  </punnet>
  <fruit state="fresh">starfruit</fruit>
  <fruit state="rotten">mango</fruit>
  <fruit state="fresh">peach</fruit>
</groceries>
""

tree=et.fromstring(xml)

for bad in tree.xpath("//fruit[@state='rotten']"):
    bad.getparent().remove(bad)

print et.tostring(tree, pretty_print=True)

###################################
for bad in tree.xpath("//fruit[@state=\'rotten\']"):
  bad.getparent().remove(bad)
  
###################################
https://stackoverflow.com/questions/7981840/how-to-remove-an-element-in-lxml
###################################
e.getparent().remove(e)

###################################
https://www.geeksforgeeks.org/remove-all-style-scripts-and-html-tags-using-beautifulsoup/

# Import Module
from bs4 import BeautifulSoup

# HTML Document
HTML_DOC = ""
			<html>
				<head>
					<title> Geeksforgeeks </title>
					<style>.call {background-color:black;} </style>
					<script>getit</script>
				</head>
				<body>
					is a
					<div>Computer Science portal.</div>
				</body>
			</html>
			""

# Function to remove tags
def remove_tags(html):

	# parse html content
	soup = BeautifulSoup(html, "html.parser")

	for data in soup(['style', 'script']):
		# Remove tags
		data.decompose()

	# return data by retrieving the tag content
	return ' '.join(soup.stripped_strings)


# Print the extracted data
print(remove_tags(HTML_DOC))

###################################
# Import Module
from bs4 import BeautifulSoup

# HTML Documen
HTML_DOC = ""
			<html>
				<head>
					<title> Geeksforgeeks </title>
					<style>.call {background-color:black;} </style>
					<script>getit</script>
				</head>
				<body>
					is a
					<div>Computer Science portal.</div>
				</body>
			</html>
			""

# Function to remove tags
def remove_tags(html):

	# parse html content
	soup = BeautifulSoup(html, "html.parser")

	for data in soup(['style', 'script']):
		# Remove tags
		data.decompose()

	# return data by retrieving the tag content
	return ' '.join(soup.stripped_strings)


# Print the extracted data
print(remove_tags(HTML_DOC))


###################################
document.getElementById("FirstDiv").remove();

###################################
###################################
###################################
###################################
###################################
###################################
###################################
###################################
###################################

###################################



    import tempfile
    with tempfile.NamedTemporaryFile(dir=dir, delete=False, suffix='.html') as tmp:
        tmp.close() # already open
        print("tmp.name:", tmp.name)
        save_html(content, tmp.name)
        driver.get(tmp.name)
        #wait_for_page_has_loaded(driver)
        return tmp.name
    
    

"""




               
""" 
        # # options=config.options
        # # options.headless = False
        # # driver = webdriver.Chrome(options=options)
        # # driver.implicitly_wait(30)    

        for file in files_index_html:
            
            print("-"*80)
            
            tree = lxml.html.parse(file)
            #tree = lxml.html.fromstring(content)

            tree = hx.remove_attributes(tree, "img", ["srcset", "xxxsrcset", "sizes", "xxxsizes"])
        
            out_path = file + "_srcset.html"
            print("writing:", out_path)
            tree.write(out_path, pretty_print=True)
            
            # img_sizes = h.xpath('//img[@sizes or @xxxsizes]') 
            # print(img_sizes)

            # # # # # # # # # driver.get("file:///" + file)
            # # # # # # # # # wh.wait_for_page_has_loaded(driver)
            # # # # # # # # # content = driver.page_source
            
            # # # # # # # # # time.sleep(3)
            
            # # # # # # # # # #elements = driver.find_elements(By.TAG_NAME, "img")
            
            # # # # # # # # # #elements = driver.find_elements(By.XPATH, "//img[@srcset]")
            # # # # # # # # # elements = driver.find_elements(By.XPATH, "//img")
            # # # # # # # # # for element in elements:
            # # # # # # # # #     print("\t", element.tag_name, element.text)
            # # # # # # # # #     driver.execute_script("arguments[0].remove();", element)
                
            # # # # # # # # # driver.execute_script(
            # # # # # # # # #     ""
            # # # # # # # # #     var element = document.getElementById("Ebene_1");
            # # # # # # # # #     element.parentNode.removeChild(element);
            # # # # # # # # #     ""
            # # # # # # # # # )

                
            # # # # # # # # # #driver.refresh()
            # # # # # # # # # for i in range(7):
            # # # # # # # # #     time.sleep(1)
            # # # # # # # # #     print('.', end='', flush=True)
                
            # # # # content = wh.string_from_file(file, sanitize=False)
            # # # soup    = bs(content, "html.parser")
            # # # #content = soup.prettify()
            # # # for data in soup(['style', 'script']):
            # # #     # Remove tags
            # # #     print("\t", data)
            # # #     data.decompose()

            # # # # return data by retrieving the tag content
            # # # #content = ' '.join(soup.stripped_strings)        
            
            # # # #print(content)    
        
            # # # driver.get("data:text/html;charset=utf-8," + content)
            # # # wh.wait_for_page_has_loaded(driver)
            
            # # # for i in range(30):
            # # #     time.sleep(1)
            # # #     print('.', end='', flush=True)
                    
                    
        #print(*files_index_html, sep="\n\t")
        # 
        # 
        
        # driver.close()
        # driver.quit()
        
 
 
 
 
 
 
    # list_script_text = h.xpath("//script/text()")
    # import re
    # import json
    # for text in list_script_text:
    #     text = jsbeautifier.beautify(text)
    #     print("script", GRAY + text + RESET)
    #     # j = json.loads(text)
    #     # print(MAGENTA, json.dumps(j, indent=4), RESET)

    #     # # # s = re.findall("'([^']*)'", text)
    #     #s = re.findall("(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", text)
    #     s = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    #     #s = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
    #     regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    #     s = re.findall(regex, text)
    #     print("s", YELLOW, *s, RESET, sep="\n\t")
    
    
    
    
           
"""



    
    