""" 
    the ratio tech vs content
        chars
        pixels
        
     
    find videos in    
        <div id="mep_0" class="mejs-container wp-video-shortcode mejs-video"
        src="https://s3.welocal.world/kadigital/media/407/videos/407.mp4?_=1"

        
        
    need find all broken links
    
"""

from distutils.log import debug
from tkinter import font
from urllib.parse import urlparse, urljoin
import os
import datetime

#-----------------------------------------
# dq
#-----------------------------------------
import helpers_web as wh
dq  = wh.dq
sq  = wh.sq
q   = wh.sq
#ats = wh.add_trailing_slash
from helpers_web import add_trailing_slash as ats

#-----------------------------------------
# init the colorama module
#-----------------------------------------
import colorama
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED
CYAN = colorama.Fore.CYAN
MAGENTA = colorama.Fore.MAGENTA
print(MAGENTA)

#-----------------------------------------
# Options
#-----------------------------------------
# https://stackoverflow.com/questions/54446419/selenium-chrome-options-and-capabilities
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless") # options.headless = config.headless
options.add_argument('--lang=de')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--log-level=3')
options.add_argument("--disable-webgl")
options.add_argument("--disable-popup-blocking")
options.add_argument("--window-size=1000,1000")
options.add_argument("--no-sandbox")
options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
options.add_argument('--disable-gpu')
options.add_argument('--disable-setuid-sandbox')
options.add_argument('--disable-features=UsePasswordSeparatedSigninFlow')
options.add_argument("--disable-extensions")
options.add_experimental_option("prefs", { \
    'download.default_directory': 'V:/00trash/__chrom',
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
})
# "--start-maximized" '--kiosk'
#-----------------------------------------
# app-selenium
#-----------------------------------------
DEBUG                   = False
#headless               = True
suffix_compressed       = "_unpowered"
timeout                 = 30
wait_secs               = (0.0, 0.001) # (0.1, 0.2) # simulate human reload
#project_folder         = ats("page/__KD__09/") # os.path.abspath # raw has 
project_folder          = ats("V:/00shared/dev8/XAMPP/xampp-php7/htdocs") # os.path.abspath # raw has 
base                    = ats('https://karlsruhe.digital/')
target_base             = ats('http://test.particles.de/') # check protocol
base_netloc             = urlparse(base).netloc # for names
data_folder             = ats("data/" + base_netloc)
#data_folder            = ats("data/" + base_netloc)
path_src_icons          = ats(data_folder + "icons/")
path_root_icons         = ats("/data/icons/")
path_dst_icons          = ats(project_folder + path_root_icons.lstrip('/'))
pdf_res                 = 96 # dpi
pdf_compression         = '/screen'
pdf_compression_suffix  = suffix_compressed + "_" + pdf_compression.lstrip('/')
path_data_netloc        = data_folder + base_netloc + "_"
path_stylesheet         = project_folder + "wp-content/themes/karlsruhe-digital/css/style.css" # suffix_compressed
path_script             = project_folder + "wp-content/themes/karlsruhe-digital/js/script.js"
path_new_script         = data_folder + "karlsruhe.digital_script.js"

###date_time           = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
date_time_now           = datetime.datetime.now()

path_image_tuples_written = data_folder + base_netloc + "_image_tuples_written.csv"

custom_css_marker       = "#marker_appended_for_custom_css" # a word in the file to mark it was updated

svg_color               = "darkseagreen"
#-----------------------------------------
# lambdas for collecting files
#----------------------------------------- 
f_originals=lambda file : any(file.lower().endswith(ext) for ext in [
    ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".svg", 
    ".js",".css",".xml",
    ".ttf",
    "index_original.html"
])
f_originals_excludes = [
    suffix_compressed       + ".webp", 
    pdf_compression_suffix  + ".pdf",
    "sub_media"
]

f_unpowered=lambda file : any(file.lower().endswith(ext) for ext in [
    suffix_compressed       + ".webp", 
    pdf_compression_suffix  + ".pdf", 
    ".svg", 
    ".js",".css",".xml",
    "index.html"
])
#-----------------------------------------
# font
#----------------------------------------- 
# https://www.w3schools.com/css/css_font.asp
#font_sans   =  "Verdana, Arial, Helvetica, sans-serif"
font_mono   =  "Monaco, Lucida Console, Courier New, monospace"
font_sans   =  "Verdana, Arial, Helvetica, sans-serif"
#-----------------------------------------
# html_infossil_link
#----------------------------------------- 
#html_infossil          = f"""<a href="https://infossil.org">infossil.org</a>"""
html_infossil_link      = f"""<a href="https://1001suns.com">green<sup>4</sup>matics</a>"""
html_infossil_link      = f"""<a href="https://1001suns.com">on<sup>4</sup>matics<sup>.ai</sup></a>"""
html_infossil_link      = f"""<a href="https://1001suns.com"><sup>infossil</sup></a>"""
html_infossil_link      = f"""<a href="https://1001suns.com">infossil</a>"""
html_by_infossil_link   = f"""<a href="https://1001suns.com">by infossil</a>"""
open_resource_link      = f"""Wie <a href="http://openresource.1001suns.com/" target="_blank">bitte?</a>"""
#-----------------------------------------
# init the colorama module
#----------------------------------------- 
_sitemap_base               = path_data_netloc + "20220703_204140"
path_sitemap_links_internal = _sitemap_base + "_internal_links.csv"
path_sitemap_links_external = _sitemap_base + "_external_links.csv"
path_sitemap_xml            = _sitemap_base + "_sitemap.xml"
path_links_errors           = _sitemap_base + "_error_links.xml"

path_custom_css             = path_data_netloc + "custom.css"
path_image_tuples_written   = path_data_netloc + "images_written.csv"
path_asset_tuples_written   = path_data_netloc + "assets_written.csv"
#-----------------------------------------
# footer_social_html
#----------------------------------------- 
footer_social_html_TEXT = """
<div id="unpowered-social-media-footer">
    <a href="https://twitter.com/KA_digital" rel="nofollow noopener" target="_blank" class="tgwf_grey">
    twitter
    </a>
    <a href="https://www.facebook.com/karlsruhe.digital" rel="nofollow noopener" target="_blank" class="tgwf_green" data-hasqtip="8" aria-describedby="qtip-8">
    facebook
    </a>
    <a href="https://www.instagram.com/karlsruhe.digital/" rel="nofollow noopener" target="_blank" class="tgwf_green" data-hasqtip="9">
    instagram
    </a>
    <a href="https://de.linkedin.com/company/karlsruhedigital" rel="nofollow noopener" target="_blank" class="tgwf_grey">
    linkedin
    </a>
    <a href="mailto:info@karlsruhe.digital">
    mail
    </a>
</div>
"""

# _ps = lambda s : "<img src=" + sq(path_root_icons + str(s) + suffix_compressed + ".webp") + " alt=" + sq(s) + " />"
# _ps = lambda s : "<img src=" + sq(path_root_icons + str(s) + ".png") + " alt=" + sq(s) + " />"
# _ps = lambda s : f"""<image xlink:href="{path_root_icons + str(s) + ".svg"}" height="20"></image>"""
# _ps = lambda s : f"""<object data="{path_root_icons+str(s)+'.svg'}" height="20"></object>"""
# footer_social_html_AA = f"""
# <div id="unpowered-social-media-footer">
#     <a href="https://twitter.com/KA_digital" rel="nofollow noopener" target="_blank">
#     {_ps("twitter")}
#     </a>
#     <a href="https://www.facebook.com/karlsruhe.digital" rel="nofollow noopener" target="_blank">
#     {_ps("facebook")}
#     </a>
#     <a href="https://www.instagram.com/karlsruhe.digital/" rel="nofollow noopener" target="_blank" >
#     {_ps("instagram")}
#     </a>
#     <a href="https://de.linkedin.com/company/karlsruhedigital" rel="nofollow noopener" target="_blank" >
#     {_ps("linkedin")}
#     </a>
#     <a href="mailto:info@karlsruhe.digital">
#     {_ps("envelope")}
#     </a>
# </div>
# """

# # _ps = lambda s : f"""<object data="{path_root_icons+str(s)+'.svg'}" height="20" style="padding: 0 3%;"></object>"""
# # _ps = lambda s : f"""<img  src="{path_root_icons+str(s)+'.svg'}" alt="{s}" height="20" style="padding: 0 3%;" />"""
# # footer_social_html_OBJ = f"""
# # <div id="unpowered-social-media-footer">
# #     {_ps("twitter")}{_ps("facebook")}{_ps("instagram")}{_ps("linkedin")}{_ps("envelope")}
# # </div>
# # """

# https://css-tricks.com/change-color-of-svg-on-hover/
_params = """ rel="nofollow noopener" target="_blank"   """ # style="margin: 0 10vw;"

#_ps    = lambda s : f"""<object type="image/svg+xml" data="{path_root_icons+str(s)+'.svg'}" alt="{s}" class="icon icon-{s}"> </object> """
#_ps    = lambda s : f"""<img  src="{path_root_icons+str(s)+'.svg'}" alt="{s}" height="20" class="icon icon-{s}" />"""
###_ps  = lambda s : f""" <img  src="{path_root_icons+str(s)+'.svg'}" alt="{s} icon" class="icon icon-{s}" /> """
_ps_scs = lambda s, c, sty : f""" <img  src="{path_root_icons+str(s)+'.svg'}" alt="{s} icon" class="{c}" style="{sty}" /> """
_icon   = lambda s : _ps_scs(s, f"icon icon-{s}", "")
footer_social_html = f"""
<div id="unpowered-social-media-footer">
    <a href="https://twitter.com/KA_digital" {_params} >
        {_icon("twitter")}
    </a>
    <a href="https://www.facebook.com/karlsruhe.digital" {_params} >
        {_icon("facebook")}
    </a>
    <a href="https://www.instagram.com/karlsruhe.digital/" {_params} >
        {_icon("instagram")}
    </a>
    <a href="https://de.linkedin.com/company/karlsruhedigital" {_params} >
        {_icon("linkedin")}
    </a>
    <a href="mailto:info@karlsruhe.digital">
        {_icon("mailto")}
    </a>
</div>
"""

svg_leaf_img = _ps_scs("leaf", "svg-leaf", "")

#-----------------------------------------
# 
#-----------------------------------------
image_exts_no_webp  = ['.jpg', '.jpeg', '.png', '.gif']
image_exts          = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
#-----------------------------------------
# 
#-----------------------------------------
sitemap_links_ignore = [
    base + 'wp-json/', # is a file not a dir
    base + 'sitemap/', # is a file not a dir
]
print("sitemap_links_ignore", sitemap_links_ignore)
# replace later with both qotes so we dont replace substrings

# use all possible quotes
# these are inspired from internal and external links files
replacements_pre = []
for q in ['\"', '\'']:
    print("\t", "using", q)
    

    replacements_pre.append(
        (
            'http:// ', # has a trailing space
            ''
        )
    )
    replacements_pre.append(
        (
            'https:// ', # has a trailing space
            ''
        )
    )
    
    
    replacements_pre.append(
        (
            'http:// https://',
            'https://'
        )
    )
    replacements_pre.append(
        (
            q + 'http:// ', # has a trailing space
            q + 'http://'
        )
    )
    replacements_pre.append(
        (
            q + 'https:// ', # has a trailing space
            q + 'https://'
        )
    )

    
    # replacements_pre.append(
    #     (
    #         q + 'http://',
    #         q + 'https://'
    #     )
    # )
    replacements_pre.append(
        (
            q + 'https://karlsruhe.digital'  + q,
            q + 'https://karlsruhe.digital/' + q
        )
    )
    replacements_pre.append(
        (
            q + 'https://www.karlsruhe.digital',
            q + 'https://karlsruhe.digital'
        )
    )
    replacements_pre.append(
        (
            q + 'https://karlsruhe.digital/en/home'  + q,
            q + 'https://karlsruhe.digital/en/home/' + q
        )
    )
    replacements_pre.append(
        (
            q + '//',
            q + 'https://'
        )
    )
    replacements_pre.append(
        (
            q + 'wp-content/',  # no root
            q + '/wp-content/'
        )
    )
    replacements_pre.append(        # script escape "https:\/\/s.w.org\/images\/core\/emoji\/12.0.0-1\/72x72\/"
        (
            '\/',
            '/'
        )
    )
    replacements_pre.append(        
        (
            '//arlsruhe.digital',   # typo in external links searching for "ruhe.digi"
            '//karlsruhe.digital'
        )
    )
print("replacements_pre", *replacements_pre, sep="\n\t")

# # # # # prebuild some dirs, en/home would otherwise be built as a file...
# # # # print("make_dirs:")
# # # # dirs = [
# # # #     ats(project_folder + 'en/home/'),
# # # #     ats(project_folder + 'wp-json/'),
# # # #     ats(project_folder + 'sitemap/')
# # # # ]
# # # # for d in dirs:
# # # #     print("\t", d)
# # # #     wh.make_dirs(d)
# # # # print()

#-----------------------------------------
# verbose
#-----------------------------------------
print("base          :", base)
print("project_folder:", project_folder)
print("style_path    :", path_stylesheet)
print()

print("replacements_pre:")
for fr, to in replacements_pre:
    print("\t", fr, "\t", "-->", to)
print(RESET)

#-----------------------------------------
# main
#-----------------------------------------
if __name__ == "__main__":
    
    for fr, to in replacements_pre:
        print(fr, to)

    # for r in replacements_pre:
    #     print(r[0], r[1])
    #     f, t = r
    #     print(f, t)