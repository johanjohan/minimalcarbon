from distutils.log import debug
from urllib.parse import urlparse, urljoin
import os

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
# app-selenium
#-----------------------------------------
DEBUG               = False
timeout             = 30
wait_secs           = (0.0, 0.001) # (0.1, 0.2) # simulate human reload
project_folder      = ats("page/__KD__09/") # os.path.abspath # raw has 
base                = ats('https://karlsruhe.digital/')
style_path          = project_folder + "wp-content/themes/karlsruhe-digital/css/style.css"
data_folder         = ats("data/")
base_netloc         = urlparse(base).netloc # for names
pdf_res             = 96 # dpi
data_base_path      = data_folder + base_netloc + "_"

#-----------------------------------------
# init the colorama module
#----------------------------------------- 
_sitemap_base               = data_base_path + "20220629_131730"
sitemap_links_internal_path = _sitemap_base + "_internal_links.csv"
sitemap_links_external_path = _sitemap_base + "_external_links.csv"
sitemap_xml_path            = _sitemap_base + "_sitemap.xml"

custom_css_path             = data_base_path + "custom.css"
image_tuples_written_path   = data_base_path + "images_written.csv"

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
print("style_path    :", style_path)
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