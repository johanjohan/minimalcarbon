import web_helpers as wh
#-----------------------------------------
# dq
#-----------------------------------------
dq = wh.dq
sq = wh.sq
q =  wh.sq
ats = wh.add_trailing_slash

#-----------------------------------------
# 
#-----------------------------------------
project_folder  = "page/__KD__"
base            = 'https://karlsruhe.digital'
style_path      = project_folder + "wp-content/themes/karlsruhe-digital/css/style.css"

base            = ats(base)
project_folder  = ats(project_folder)

# replace later with both qotes so we dont replace substrings
replacements_pre = [
    ("https://karlsruhe.digital/en/home", "https://karlsruhe.digital/en/home/"),
]


#-----------------------------------------
# verbose
#-----------------------------------------
print("base          :", q(base))
print("project_folder:", q(project_folder))
print("style_path    :", q(style_path))

print("replacements_pre:")
for fr, to in replacements_pre:
    print("\t", fr, to)


if __name__ == "__main__":
    
    for fr, to in replacements_pre:
        print(fr, to)

    # for r in replacements_pre:
    #     print(r[0], r[1])
    #     f, t = r
    #     print(f, t)