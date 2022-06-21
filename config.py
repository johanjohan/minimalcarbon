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
print(YELLOW)

#-----------------------------------------
# dq
#-----------------------------------------
import web_helpers as wh
dq  = wh.dq
sq  = wh.sq
q   = wh.sq
#ats = wh.add_trailing_slash
from web_helpers import add_trailing_slash as ats

#-----------------------------------------
# 
#-----------------------------------------
wait_secs           = (0.1, 1.2345)
project_folder      = ats("page/__KD__/")
base                = ats('https://karlsruhe.digital/')
style_path          = project_folder + "wp-content/themes/karlsruhe-digital/css/style.css"

sitemap_links_path  = "data/karlsruhe.digital_20220616_222903_internal_links.csv"
sitemap_links_ignore = [
    base + 'wp-json/', # is a file not a dir
    base + 'sitemap/', # is a file not a dir
]
print("sitemap_links_ignore", sitemap_links_ignore)
# replace later with both qotes so we dont replace substrings
replacements_pre = [
    (
        'https://karlsruhe.digital'     , 
        'https://karlsruhe.digital/'
    ),
 
    (
        'https://karlsruhe.digital/en/home'     , 
        'https://karlsruhe.digital/en/home/'
    ),
    
   
    ]
print("replacements_pre", replacements_pre)

# prebuild some dirs, en/home would otherwise be built as a file...
dirs = [
    ats(project_folder + 'en/home/'),
    ats(project_folder + 'wp-json/'),
    ats(project_folder + 'sitemap/')
]
print("make_dirs:")
for d in dirs:
    print("\t", d)
    wh.make_dirs(d)
print()

#-----------------------------------------
# verbose
#-----------------------------------------
print("base          :", q(base))
print("project_folder:", q(project_folder))
print("style_path    :", q(style_path))
print()

print("replacements_pre:")
for fr, to in replacements_pre:
    print("\t", fr, "-->", to)
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