import os
import helpers_web as hw

#-----------------------------------------
# 
#-----------------------------------------
def save(path_conversions, conversions, mode='w'):
    
    if not conversions:
        return
    
    # make unique # remove redundancies    
    prev = load(path_conversions)
    conversions.extend(prev) 
    conversions = hw.links_make_unique(conversions)
    conversions = sorted(conversions)
    
    if conversions:    
        print("save_conversions:", hw.YELLOW + path_conversions + hw.RESET)
        with open(path_conversions, mode, encoding="utf-8") as fp:
            for conversion in conversions:
                fr, to = conversion        
                fp.write(fr.strip() +  "," + to.strip() + "\n")    
        print("save_conversions: len(conversions):", len(conversions)) 
        
#-----------------------------------------
# 
#-----------------------------------------                
def load(path_conversions):
    
    print("load_conversions:", hw.YELLOW + path_conversions + hw.RESET)
    
    conversions = []
    if os.path.isfile(path_conversions):
        with open(path_conversions, 'r', encoding="utf-8") as fp:
            for line in fp:
                subs = line.split(',')
                if len(subs) >= 2:
                    conversions.append(tuple([subs[0].strip(), subs[1].strip()])) # a tuple
        conversions = hw.links_make_unique(conversions)
        conversions = sorted(conversions)
            
    print("load_conversions: len(conversions):", len(conversions))
    return conversions

#-----------------------------------------
# 
#-----------------------------------------   