import lxml
import lxml.html
from lxml import etree
import helpers_web as hw

def remove_attributes(tree, tag, attributes):
    
    print(f"remove_attributes: <{tag}> {attributes} | {tree}")
    
    cnt = 0
    for attribute in list(attributes):
        attribute = attribute.replace('@', '')
        _xpath = f"//{tag}[@{attribute}]"
        items = tree.xpath(_xpath) 
        #print("\t items", items)
        for item in items:
            #print("\t", hw.GRAY, item.get(attribute), hw.RESET) 
            item.attrib.pop(attribute, None)  # None is to not raise an exception
            cnt += 1
        assert tree.xpath(_xpath) == [] # make sure all popped
        
    #print(lxml.etree.tostring(tree, pretty_print=True))
    print(f"\t removed: {cnt} attributes from <{tag}> ")
    
    return tree

""" 

<div id="simple-banner" class="simple-banner">
    <div class="simple-banner-text">
        <span>This site is run on sustainable energy and reduces image quality &amp; quantity for a low carbon footprint. <br>Videos load after clicking to avoid tracking. <a href="http://openresource.1001suns.com/pyramis-niger.php">Why?</a><!--br/>Access the low carbon version of this site <a href="http://static.1001suns.com/">here</a--></span>
    </div>
</div>

CSS will be applied directly to the simple-banner class, 
the simple-banner-scrolling class for scrolling styles, 
the simple-banner-text class for text specific styles, 
and the simple-banner-button class for close button specific styles. 
Be very careful, bad CSS can break the banner.


"""
def __get_content(text, id, class_banner, class_text):
    return f'''
    <div id="{id}" class="{class_banner}">
        <div class="{class_text}">
            <span>{text}</span>
        </div>
    </div>    
    '''    
    
def banner_header(text, id="banner_header", class_banner="banner_header", class_text="banner_header_text"):
    banner = lxml.html.fragment_fromstring(__get_content(text, id, class_banner, class_text))
    #print(lxml.html.etree.tostring(banner, pretty_print=True).decode())
    return banner
     
def banner_footer(text, id="banner_footer", class_banner="banner_footer", class_text="banner_footer_text"):
    banner = lxml.html.fragment_fromstring(__get_content(text, id, class_banner, class_text))
    #print(lxml.html.etree.tostring(banner, pretty_print=True).decode())
    return banner

def remove_by_xpath(tree, sxpath):
    #print("remove_by_xpath", sxpath)
    for item in tree.xpath(sxpath):
        print("\t removing:", hw.CYAN + sxpath + hw.RESET)
        item.getparent().remove(item)     

def replace_xpath_with_fragment(tree, sxpath, html_string):
    #print("replace_by_xpath", sxpath)
    for item in tree.xpath(sxpath):
        print("\t replacing:", hw.CYAN + sxpath + hw.RESET)
        item.getparent().replace(item, lxml.html.fragment_fromstring(html_string)) 
        
def replace_xpath_with_fragment_from_file(tree, sxpath, frag_file_path):
    html_string =  hw.string_from_file(frag_file_path, sanitize=False)
    for item in tree.xpath(sxpath):
        print("\t replacing:", hw.YELLOW + sxpath + hw.RESET)
        item.getparent().replace(item, lxml.html.fragment_fromstring(html_string)) 
 
                    
if __name__ == "__main__":
    banner_header("text with html<br> end.")