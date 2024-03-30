"""
check wp-content for paths or rel path etc


202210
    manual kd fixes:
.home  #section-4 {
	/* display: none; */
}

/* home twitter */
.home #section-4 {
	display: none;
}

.home  .fts-feed-type-twitter {
	/* display: none; */
}    

replace 
    <a href="/blog/index.html">Blog</a>   
    <a href="https://karlsruhe.digital/blog/">Blog</a>   
    
    
    <a href="/en/blog-2/index.html" aria-current="page">Blog</a>
    <a href="https://karlsruhe.digital/en/blog-2/" aria-current="page">Blog</a>
    
    <a href="/en/blog-2/index.html">Blog</a> 
    <a href="https://karlsruhe.digital/en/blog-2/">Blog</a>

"""



""" 
    use AI to analyse image tags


    the ratio tech vs content
        chars
        pixels
        
     
    find videos in    
        <div id="mep_0" class="mejs-container wp-video-shortcode mejs-video"
        src="https://s3.welocal.world/kadigital/media/407/videos/407.mp4?_=1"

        
        
    need find all broken links
    
    TODO
            
    https://codegolf.stackexchange.com/questions/23362/sort-characters-by-darkness



    total_size_originals: 606,034,501 bytes | 606.0 MB
    total_size_unpowered: 30,003,159 bytes | 30.0 MB
    get_project_total_size: +95.0%
    20220726 02:44:36: perc100_saved       : 95.0 %
    20220726 02:44:36: total_size_originals: 606034501 bytes
    20220726 02:44:36: total_size_unpowered: 30003159 bytes
    20220726 02:44:36: total_size_originals: 606.0 MB
    20220726 02:44:36: total_size_unpowered: 30.0 MB


    size_texts     : 19435563 bytes | 19.435563 MB | 28.7 %
    size_images_old: 0 bytes | 0.0 MB | 0.0 %
    size_images_new: 19951968 bytes | 19.951968 MB | 29.5 %
    size_pdfs      : 28267224 bytes | 28.267224 MB | 41.8 %
    --------------------------------------------
    size_total     : 67654755 bytes | 67.654755 MB




    size_texts     : 19435563 bytes | 19.435563 MB | 49.3 %
    size_images_old: 0 bytes | 0.0 MB | 0.0 %
    size_images_new: 19951968 bytes | 19.951968 MB | 50.7 %
    --------------------------------------------
    size_total     : 39387531 bytes | 39.387531 MB





    
"""


from distutils.log import debug
from selectors import BaseSelector
from tkinter import font
from urllib.parse import urlparse, urljoin
import os
import datetime
import math

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
#options.add_argument('--start-maximized')
options.add_argument("--window-size=1600,1080") # --window-size=1920,1080 # 1600,1080
options.add_argument('--lang=de')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--log-level=3')
options.add_argument("--disable-webgl")
options.add_argument("--disable-popup-blocking")
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
# 
#-----------------------------------------
#target_image_ext        = ".webp"
target_image_ext        = ".webp"
#target_image_exts       = [".avif", ".webp"] # TODO

image_exts              = ['.jpg', '.jpeg', '.png', '.gif', '.webp', ".avif"]
image_exts_no_target    = [ext for ext in image_exts if not any(exclude.strip() in ext for exclude in [target_image_ext])]
print("image_exts_no_target", image_exts_no_target)

crawler_valid_exts      = [".html", ".htm", ".php", ""]
#-----------------------------------------
# app
#-----------------------------------------
DEBUG                   = False
#headless               = True
#suffix_compressed       = "_unpowered"
suffix_compressed       = "_up".lower() # must be lowercase for f_originals comparison below
timeout                 = 30
wait_secs               = (0.0, 0.001) # (0.1, 0.2) # simulate human reload
#project_folder         = ats("page/__KD__09/") # os.path.abspath # raw has 
project_folder          = ats("V:/00shared/dev8/XAMPP/xampp-php7/htdocs") # os.path.abspath # raw has 
base                    = ats('https://karlsruhe.digital/')
bases                   = [base, "https://kadigital.s3-cdn.welocal.cloud/", "https://media.karlsruhe.digital/"]
###target_base             = ats('http://test.particles.de/') # check protocol # for sitemap etc
target_base             = ats('https://minimalcarbon.site/karlsruhe.digital/') # check protocol # for sitemap etc
target_root             = '/' # NEW TODO replacable pattern # root / # 'https://minimalcarbon.site/karlsruhe.digital/'
base_netloc             = urlparse(base).netloc # for names
data_folder             = ats("data/" + base_netloc)
#data_folder            = ats("data/" + base_netloc)
path_src_icons          = ats(data_folder + "icons/")
###path_root_icons         = ats("/data/icons/")
path_root_icons         = ats(target_root + "data/icons/") # NEW
path_dst_icons          = ats(project_folder + path_root_icons.lstrip('/'))
pdf_res                 = 96 # dpi
pdf_compression         = '/screen'
pdf_compression_suffix  = suffix_compressed + "_" + pdf_compression.lstrip('/')
path_data_netloc        = data_folder + base_netloc + "_"
path_stylesheet         = project_folder + "wp-content/themes/karlsruhe-digital/css/style.css" # suffix_compressed
path_script             = project_folder + "wp-content/themes/karlsruhe-digital/js/script.js"
path_new_script         = data_folder + "karlsruhe.digital_script.js"
path_stats              = ats(project_folder + "__stats/" + base_netloc) 

protocol_excludes       = ["whatsapp:", "mailto:", "javascript:", "data:"]

path_snapshots              = ats(project_folder + "../__snaps/" + base_netloc) 
path_snapshots_visited      = path_snapshots + base_netloc + "_300_image_snaps_visited.csv"

crawler_base                = path_stats + base_netloc + "_050" # crawler
path_sitemap_links_internal = crawler_base + "_internal_links.csv"
path_sitemap_links_external = crawler_base + "_external_links.csv"
path_sitemap_xml            = crawler_base + "_sitemap.xml"
path_links_errors           = crawler_base + "_error_links.csv"
path_sitemap_links_int_diff = crawler_base + "_internal_diff_links.csv"

filename_sitemap            = "sitemap.xml"
filename_sitemap_gz         = filename_sitemap + ".gz"
path_htdocs_sitemap         = project_folder + filename_sitemap
path_htdocs_sitemap_gz      = project_folder + filename_sitemap_gz

filename_robots             = "robots.txt"
path_htdocs_robots          = project_folder + filename_robots

path_custom_css             = path_data_netloc + "custom.css"
path_image_tuples_written   = path_stats + base_netloc + "_150_images_written.csv"
path_asset_tuples_written   = path_stats + base_netloc + "_150_assets_written.csv"
path_image_sizes            = path_stats + base_netloc + "_110_image_sizes.csv"
path_image_sizes_visited    = path_stats + base_netloc + "_110_image_sizes_visited.csv"

#path_conversions            = data_folder + base_netloc + "_conversions.csv"
path_conversions            = path_stats + base_netloc + "_200_conversions.csv"
path_log_params             = path_stats + base_netloc + "_params_log.txt"
folder_exported             = project_folder + "../__exported/"

dt_now                      = datetime.datetime.now()
dt_now_string               = dt_now.strftime("%Y%m%d_%H%M%S")
custom_css_marker           = "#marker_appended_for_custom_css" # a word in the file to mark it was updated
svg_color                   = "darkseagreen"

turns_for_slow_funcs        = math.inf # 4 # inf
implicit_wait               = 0.1 # can be float, will be millis

#-----------------------------------------
# 
#----------------------------------------- 
postfix_bup     = "_pofx_BUP_"
postfix_orig    = "_pofx_ORIG"
    
excludes_postfix=[postfix_bup, postfix_orig]
excludes_compressed_postfix=[suffix_compressed, postfix_bup, postfix_orig]
#-----------------------------------------
# lambdas for collecting files
#----------------------------------------- 
f_originals=lambda file : any(file.lower().endswith(ext) for ext in [
    ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".svg", 
    ".js",".css",".xml",
    "robots.txt", 
    "sitemap.xml.gz",
    ".ttf",
    "index_original.html"
])
f_originals_excludes = [
    "sub_media",
    suffix_compressed       + target_image_ext, 
    pdf_compression_suffix  + ".pdf",
    ".mp4",
    
    postfix_bup, 
    postfix_orig,
]

f_unpowered=lambda file : any(file.lower().endswith(ext) for ext in [
    suffix_compressed       + target_image_ext, 
    pdf_compression_suffix  + ".pdf", 
    ".svg", 
    ".js",".css",".xml",
    "robots.txt", 
    "sitemap.xml.gz",
    "index.html"
])
f_unpowered_excludes = [
    "sub_media",
    "font", 
    "real3d-flipbook",
    ".mp4",
    
    postfix_bup, 
    postfix_orig,
]
#-----------------------------------------
# font
#----------------------------------------- 
# https://www.w3schools.com/css/css_font.asp
#font_sans   =  "Verdana, Arial, Helvetica, sans-serif"
#font_mono   =  "Monaco, Lucida Console, Courier New, monospace"
font_mono   =  "monospace"
#font_sans   =  "Verdana, Arial, Helvetica, sans-serif"
font_sans   =  "sans-serif"
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
_html_icon_img  = lambda s, c, sty : f""" <img  src="{path_root_icons+str(s)+'.svg'}" alt="{s} icon" class="{c}" style="{sty}" /> """
_icon           = lambda s : _html_icon_img(s, f"icon icon-{s}", "")
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

svg_leaf_img = _html_icon_img("leaf", "svg-leaf", "")


#-----------------------------------------
# 
#-----------------------------------------
# sitemap_links_ignore = [
#     base + 'wp-json/', # is a file not a dir
#     base + 'sitemap/', # is a file not a dir
# ]
sitemap_links_ignore = [
    '/wp-json/', 
    '/sitemap/', 
]
print("sitemap_links_ignore", sitemap_links_ignore)
# replace later with both qotes so we dont replace substrings

# use all possible quotes
# these are inspired from internal and external links files
replacements_pre = []
for q in ['\"', '\'']:
    print("\t", "using", q)
    

    # replacements_pre.append(
    #     (
    #         'http:// ', # has a trailing space
    #         ''
    #     )
    # )
    # replacements_pre.append(
    #     (
    #         'https:// ', # has a trailing space
    #         ''
    #     )
    # )

    replacements_pre.append(
        (
            q + 'http:// ', # has a trailing space
            q + 'https://'
        )
    )
    replacements_pre.append(
        (
            q + 'https:// ', # has a trailing space
            q + 'https://'
        )
    )

    
    replacements_pre.append(
        (
            'http://karlsruhe.digital/ https', 
            'https://karlsruhe.digital/'        # <<< s
        )
    )
    # # replacements_pre.append(
    # #     (
    # #         ' https', 
    # #         ''
    # #     )
    # # )
    # # replacements_pre.append(
    # #     (
    # #         ' http', 
    # #         ''
    # #     )
    # # )
        
    replacements_pre.append(
        (
            'http:// https://',
            'https://'
        )
    )

    # # no OLD protocols no more
    # replacements_pre.append(
    #     (
    #         q + 'http://', # <<<<<<<<<<<<<
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
    # # # replacements_pre.append(
    # # #     (
    # # #         q + 'wp-content/',  # no root
    # # #         q + '/wp-content/'
    # # #     )
    # # # )
    replacements_pre.append(
        (
            q + 'wp-content',  # no root
            q + '/wp-content'
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