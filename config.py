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
wait_secs           = (0.1, 0.2)
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

# use all possible quotes
replacements_pre = []
for q in ['\"', '\'']:
    print("\t", "using", q)
    replacements_pre.append(
        (
            q + 'https://karlsruhe.digital'  + q   ,
            q + 'https://karlsruhe.digital/' + q
        )
    )
    replacements_pre.append(
        (
            q + 'https://karlsruhe.digital/en/home'  + q   ,
            q + 'https://karlsruhe.digital/en/home/' + q
        )
    )
    replacements_pre.append(
        (
            q + '//'         ,
            q + 'https://'
        )
    )

print("replacements_pre", *replacements_pre, sep="\n\t")

# prebuild some dirs, en/home would otherwise be built as a file...
print("make_dirs:")
dirs = [
    ats(project_folder + 'en/home/'),
    ats(project_folder + 'wp-json/'),
    ats(project_folder + 'sitemap/')
]
for d in dirs:
    print("\t", d)
    wh.make_dirs(d)
print()

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