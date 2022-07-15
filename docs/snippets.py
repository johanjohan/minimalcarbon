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
        # # driver.implicitly_wait(config.implicit_wait)    

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
    
    
    
    

                
    # # # # #-----------------------------------------
    # # # # # b_fix_xml
    # # # # #-----------------------------------------
    # # # # if b_fix_xml_elements:
    # # # #     wh.logo("b_fix_xml_elements")
        
    # # # #     func=lambda s : True # finds all
    # # # #     func=lambda file : any(file.lower().endswith(ext) for ext in config.image_exts)
    # # # #     func=lambda file : file.lower().endswith("index.html")
    # # # #     files_index_html = wh.collect_files_func(project_folder, func=func)
    # # # #     #print(*files_index_html, sep="\n\t")
        
    # # # #     color = "darkseagreen"
    # # # #     svg_percircle = f""<div class="percircle"><svg viewBox="0 0 500 500" role="img" xmlns="http://www.w3.org/2000/svg">
    # # # #         <g id="myid">
    # # # #             <circle stroke="{color}"
    # # # #                     stroke-width="12px"
    # # # #                     fill="none"
    # # # #                     cx="250"
    # # # #                     cy="250"
    # # # #                     r="222" />
    # # # #             <text style="font: bold 12rem sans-serif;"
    # # # #                 text-anchor="middle"
    # # # #                 dominant-baseline="central"
    # # # #                 x="50%"
    # # # #                 y="50%"
    # # # #                 fill="{color}">{perc100_saved:.0f}%</text> 
    # # # #         </g>     
    # # # #     </svg></div>""


    # # # #     for file in files_index_html:
            
    # # # #         print("-"*80)
    # # # #         print("file", wh.CYAN + file + wh.RESET)
    # # # #         wp_path     = wh.to_posix('/' + os.path.relpath(file, project_folder))
    # # # #         base_path   = config.base + wh.to_posix(os.path.relpath(file, project_folder)).replace("index.html", "")
    # # # #         same_page_link = f""<a href="{base_path}">{config.base_netloc}</a>""
            
    # # # #         ""
    # # # #         Dies ist die energie-effiziente
    # # # #         energie optimierte 
    # # # #         Dies ist die Low Carbon Website
    # # # #         Dies ist die Low Carbon Website
    # # # #         This is the environmentally aware version of 
    # # # #         Dies ist die umweltbewusste Seite
    # # # #         This is the environmentally friendly twin of 
    # # # #         .<br/>The energy consumption of this website was reduced by {saved_string}.
    # # # #         .<br/>Der Energieverbrauch dieser Website wurde um {saved_string} reduziert.
    # # # #         ""
    # # # #         # https://babel.pocoo.org/en/latest/dates.html
    # # # #         from babel.dates import format_date, format_datetime, format_time
    # # # #         dt = config.date_time_now
    # # # #         format='full' # long
    # # # #         saved_string = f"<span style=''>{perc100_saved:.1f}%</span>"
    # # # #         if "/en/" in wp_path:
    # # # #             dt_string = format_date(dt, format=format, locale='en')
    # # # #             banner_header_text = f"This is the Low Carbon proxy of {same_page_link}" # <br/>{svg_percircle}
    # # # #             banner_footer_text = f"{svg_percircle}<br/>unpowered by {config.html_infossil_link}" # <br/>{dt_string}
    # # # #         else:
    # # # #             dt_string = format_date(dt, format=format, locale='de_DE')
    # # # #             banner_header_text = f"Dies ist der Low Carbon Proxy von {same_page_link}"
    # # # #             banner_footer_text = f"{svg_percircle}<br/>unpowered by {config.html_infossil_link}" # <br/>{dt_string}
                
    # # # #         #---------------------------
    # # # #         # lxml
    # # # #         #---------------------------    
    # # # #         tree = lxml.html.parse(file) # lxml.html.fromstring(content)
            
    # # # #         # start the hocus pocus in focus
    # # # #         # use section-1 from original site as frag
    # # # #         if False and False:
    # # # #             hx.replace_xpath_with_fragment_from_file(
    # # # #                 tree, 
    # # # #                 "//section[@id='section-1']", 
    # # # #                 "data/karlsruhe.digital_fragment_section1.html" # frag_file_path
    # # # #             )
            
    # # # #         #---------------------------
    # # # #         # banners
    # # # #         #---------------------------    
    # # # #         if True: # +++
    # # # #             # TODO must be /en/ and not depending on wp_path /en/
    # # # #             banner_header = hx.banner_header(banner_header_text)
    # # # #             hx.remove_by_xpath(tree, "//div[@class='banner_header']")
    # # # #             print("\t adding banner_header")    
    # # # #             try:                
    # # # #                 tree.find(".//header").insert(0, banner_header)    
    # # # #             except Exception as e:
    # # # #                 print("\t", wh.RED, e, wh.RESET)
    # # # #                 exit(1)

    # # # #             "" 
    # # # #             media
    # # # #             <footer id="colophon" class="site-footer with-footer-logo" role="contentinfo"><div class="footer-container"><div class="logo-container"><a href="https://media.karlsruhe.digital/" title="" rel="home" class="footer-logo tgwf_green" data-hasqtip="14"><img src="https://kadigital.s3-cdn.welocal.cloud/sources/5ffed45149921.svg" alt=""></a></div><div class="footer-nav"><div class="menu-footer-container"><ul id="menu-footer" class="footer-menu"><li id="menu-item-551" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-551"><a target="_blank" rel="noopener" href="/impressum/index.html">Impressum</a></li><li id="menu-item-550" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-550"><a target="_blank" rel="noopener" href="/datenschutz/index.html">Datenschutz</a></li></ul></div> </div></div><div class="footer-socials-wrapper"><ul class="footer-socials"><li><a href="https://www.facebook.com/karlsruhe.digital" target="" rel="nofollow" class="social ss-facebook tgwf_green" data-hasqtip="15"><span>Facebook</span></a></li><li><a href="https://twitter.com/KA_digital" target="" rel="nofollow" class="social ss-twitter tgwf_grey"><span>Twitter</span></a></li><li><a href="https://www.instagram.com/karlsruhe.digital/" target="" rel="nofollow" class="social ss-instagram tgwf_green" data-hasqtip="16"><span>Instagram</span></a></li><li><a href="mailto:info@karlsruhe.digital" target="" rel="nofollow" class="social ss-mail"><span>Mail</span></a></li></ul></div></footer>

    # # # #             ""                
    # # # #             banner_footer = hx.banner_footer(banner_footer_text)
    # # # #             hx.remove_by_xpath(tree, "//div[@class='banner_footer']")
    # # # #             print("\t adding banner_footer")  
    # # # #             try:
    # # # #                 footer = tree.find(".//footer") # ".//body"
    # # # #                 if not footer:
    # # # #                     footer = tree.find(".//body")
    # # # #                 footer.append(banner_footer)
    # # # #             except Exception as e:
    # # # #                 print("\t", wh.RED, e, wh.RESET)    
    # # # #                 exit(1)                

    # # # #         #---------------------------
    # # # #         # image attributes srcset
    # # # #         #---------------------------    
    # # # #         tree = hx.remove_attributes(tree, "img", ["srcset", "sizes", "xxxsrcset", "xxxsizes", "XXXsrcset", "XXXsizes"])

    # # # #         # remove logo in footer: body > footer > div.footer-top > div > div > div.col-xl-4
    # # # #         hx.remove_by_xpath(tree, "//div[@class='footer-top']//a[@class='logo']")

    # # # #         #---------------------------
    # # # #         # menu
    # # # #         #---------------------------    
    # # # #         b_hide_search = True
    # # # #         if b_hide_search:
    # # # #             hx.remove_by_xpath(tree, "//li[@id='menu-item-136']") # search in menu
    # # # #         else:
    # # # #             #hx.replace_by_xpath(tree, "//i[contains(@class, 'fa-search')]", "<span>SUCHE</span")
    # # # #             pass
            
    # # # #         if b_hide_media_subdomain:
    # # # #             hx.remove_by_xpath(tree, "//li[@id='menu-item-3988']") # media submenu --> no media.

    # # # #         # all fa font awesome TODO also gets rid of dates etc...
    # # # #         # hx.remove_by_xpath(tree, "//i[contains(@class, 'fa-')]")

    # # # #         # <span class="swiper-item-number">6</span>
    # # # #         # if True:
    # # # #         #     #hx.remove_by_xpath(tree, "//span[@class='swiper-item-number']")
    # # # #         #     hx.remove_by_xpath(tree, "//div[@id='hero-swiper']//span[@class='swiper-item-number']")
    # # # #         #     hx.remove_by_xpath(tree, "//div[@id='hero-swiper']//span[@class='color-white']")
            

    # # # #         #---------------------------
    # # # #         # scripts
    # # # #         #---------------------------                      
    # # # #         # //script[normalize-space(text())]
    # # # #         hx.remove_by_xpath(tree, "//script[contains(normalize-space(text()), '_wpemojiSettings' )]")
    # # # #         hx.remove_by_xpath(tree, "//script[contains(normalize-space(text()), 'ftsAjax' )]")
    # # # #         hx.remove_by_xpath(tree, "//script[contains(normalize-space(text()), 'checkCookie' )]")
            
    # # # #         hx.remove_by_xpath(tree, "//head//script[contains(@src, 'google-analytics' )]")
    # # # #         hx.remove_by_xpath(tree, "//head//script[contains(@src, 'wp-emoji-release' )]")
    # # # #         hx.remove_by_xpath(tree, "//head//script[contains(@src, 'feed-them-social' )]")
            
    # # # #         hx.remove_by_xpath(tree, "//head//script[contains(@src, 'jquery-migrate' )]")
    # # # #         #hx.remove_by_xpath(tree, "//head//script[contains(@src, 'jquery.js' )]") >> needed for menu !!!
            
    # # # #         hx.remove_by_xpath(tree, "//head//script[@async]")
    # # # #         hx.remove_by_xpath(tree, "//head//script[@defer]")
            
    # # # #         # hx.remove_by_xpath(tree, "//head//script[@src='https://www.google-analytics.com/analytics.js']")
    # # # #         # hx.remove_by_xpath(tree, "//head//script[@src='https://www.google-analytics.com/analytics.js']")
    # # # #         # hx.remove_by_xpath(tree, "//head//script[@src='/wp-includes/js/wp-emoji-release.min.js']")
    # # # #         # hx.remove_by_xpath(tree, "//head//script[@src='/wp-includes/js/wp-emoji-release.min.js']")
            
    # # # #         #hx.remove_by_xpath(tree, "//body//script[contains(@src, 'bootstrap' )]")
    # # # #         #hx.remove_by_xpath(tree, "//body//script[contains(@src, 'owl.carousel' )]")
    # # # #         ####hx.remove_by_xpath(tree, "//body//script[contains(@src, 'script.js' )]") NO!!
    # # # #         hx.remove_by_xpath(tree, "//body//script[contains(@src, 'wp-embed' )]")
    # # # #         hx.remove_by_xpath(tree, "//body//script[contains(@src, 'googletagmanager' )]")
    # # # #         hx.remove_by_xpath(tree, "//body//script[contains(text(), 'gtag' )]")
            
    # # # #         #---------------------------
    # # # #         # twitter feeds
    # # # #         #---------------------------   
    # # # #         hx.remove_by_xpath(tree, "//section[contains(@class,'social-media-feed')]")
            
    # # # #         #---------------------------
    # # # #         # social media footer
    # # # #         #--------------------------- 
    # # # #         hx.replace_xpath_with_fragment(tree, "//div[contains(@class, 'footer-bottom' )]//div[contains(@class, 'footer-social-links' )]", config.footer_social_html)
    # # # #         hx.replace_xpath_with_fragment(tree, "//div[@id='unpowered-social-media-footer']", config.footer_social_html)

    # # # #         #---------------------------
    # # # #         # swipers
    # # # #         #--------------------------- 
    # # # #         # //div[contains(@id, 'blog-swiper' )]//div[contains(@class, 'owl-nav' )][last()]
    # # # #         ###hx.remove_by_xpath(tree, "//div[contains(@id, 'blog-swiper' )]//div[contains(@class, 'owl-nav' )][last()]")
    # # # #         hx.remove_by_xpath(tree, "//div[contains(@id, 'blog-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
    # # # #         hx.remove_by_xpath(tree, "//div[contains(@id, 'hero-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
    # # # #         hx.remove_by_xpath(tree, "//div[contains(@id, 'testimonial-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
    # # # #         hx.remove_by_xpath(tree, "//div[contains(@id, 'theses-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
            
    # # # #         #---------------------------
    # # # #         # video/media player
    # # # #         #---------------------------          
    # # # #         hx.remove_by_xpath(tree, "//div[contains(@class, 'wp-video' )]")            
    # # # #         hx.remove_by_xpath(tree, "//div[contains(@class, 'mejs-video' )]")            

    # # # #         #---------------------------
    # # # #         # save
    # # # #         #--------------------------- 
    # # # #         out_path = file # + "__test.html"
    # # # #         print("writing:", out_path)
    # # # #         tree.write(
    # # # #             out_path, 
    # # # #             pretty_print=True, 
    # # # #             xml_declaration=False,   
    # # # #             encoding="utf-8",   # !!!!
    # # # #             method='html'       # !!!!
    # # # #         )
        
    
    # # # #     # files_index_html = wh.collect_files_endswith(project_folder, ["index.html"])
    # # # #     # for file in files_index_html:
    # # # #     #     print("-"*80)
    # # # #     #     content = wh.string_from_file(file, sanitize=False)
    # # # #     #     soup    = bs(content)
    # # # #     #     content = soup.prettify()
    # # # #     #     print(content)
           

           
"""


"""
    # wget -E -H -k -K -p -e robots=off https://karlsruhe.digital
    # wget -E --span-hosts -k -K -p -e robots=off https://karlsruhe.digital
    # wget --mirror -nH -np -p -k -E -e robots=off https://karlsruhe.digital
    # wget --mirror -nH -np -p -k -E -e robots=off -i "../data/karlsruhe.digital_internal_links.csv" 
    
    # https://stackoverflow.com/questions/31205497/how-to-download-a-full-webpage-with-a-python-script
    
https://www.elegantthemes.com/blog/editorial/the-wordpress-json-rest-api-wp-api-what-it-is-how-it-works-what-it-means-for-the-future-of-wordpress
https://developer.wordpress.org/rest-api/


https://karlsruhe.digital/wp-json/
https://karlsruhe.digital/wp-json/wp/v2
https://karlsruhe.digital/wp-json/wp/v2/routes
routes
_links self

TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
-> link "https://karlsruhe.digital/2022/06/events-termine-in-karlsruhe-kw-25-2022/"
-> guid rendered "https://karlsruhe.digital/?p=5522" ## media makes more sense
https://karlsruhe.digital/wp-json/wp/v2/posts
https://karlsruhe.digital/wp-json/wp/v2/pages
https://karlsruhe.digital/wp-json/wp/v2/media
https://karlsruhe.digital/wp-json/wp/v2/blocks
https://karlsruhe.digital/wp-json/wp/v2/categories





#-----------------------------------------
# testing...
#-----------------------------------------
# # requests TFFTF vs urllib TFFTF
# print(wh.get_mime_type("http://karlsruhe.digital"))
# print(wh.get_mime_type("https://karlsruhe.digital"))
# print(wh.get_mime_type("https://karlsruhe.digital/"))
# print(wh.get_mime_type("https://karlsruhe.digital//"))
# print(wh.get_mime_type("https://karlsruhe.digital/wp-content/uploads/2022/06/2021.Sesemann_7422.Foto-im-Intranet.jpg"))
# #print(wh.get_mime_type("https://123ddd.cccXXXX"))
# exit(0)

# https://searchfacts.com/url-trailing-slash/
# Should You Have a Trailing Slash at the End of URLs
# The short answer is that the trailing slash does not matter for your root domain or subdomain. 
# Google sees the two as equivalent.
# But trailing slashes do matter for everything else because Google sees the two versions 
# (one with a trailing slash and one without) as being different URLs.





"""


if __name__ == "__main__":


    import re
    s = "©@my string with öäüßÖÄÜ éè bla bla 世丕且且世两 !\":.<>?"

    #delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
    #res = ''.join(ch for ch in s if ch.isalnum())
    res = bytes(s, 'utf-8').decode('utf-8', 'ignore')

    import string
    res = ''.join(x for x in s if x in string.printable) # OK

    # https://stackoverflow.com/questions/33504953/is-there-a-way-to-convert-unicode-to-the-nearest-ascii-equivalent
    #transliteration.
    # pip install Unidecode
    from unidecode import unidecode

    res = unidecode(s).replace(' ', '_')

    import unicodedata
    import re

    def slugify(value, allow_unicode=False):
        
        value = unidecode(value) # 3j
        
        """
        Taken from https://github.com/django/django/blob/master/django/utils/text.py
        Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
        dashes to single dashes. Remove characters that aren't alphanumerics,
        underscores, or hyphens. Convert to lowercase. Also strip leading and
        trailing whitespace, dashes, and underscores.
        """
        value = str(value)
        if allow_unicode:
            value = unicodedata.normalize('NFKC', value)
        else:
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value.lower())
        return re.sub(r'[-\s]+', '-', value).strip('-_')

    res = slugify(unidecode(s), allow_unicode=False)

    print(s)
    print(res)

        