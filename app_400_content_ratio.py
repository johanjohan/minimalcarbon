# https://www.adamsmith.haus/python/answers/how-to-extract-text-from-an-html-file-in-python

import config
import helpers_web as wh
import helpers_web as hw
import time
import urllib.parse # selenium seems to urlencode results
from urllib.request import urlopen
from bs4 import BeautifulSoup

if __name__ == "__main__":
    
    wh.logo_filename(__file__)
    wh.log("__file__:", __file__, filepath=config.path_log_params)
    
    start_secs          = time.time()
    excludes = ["media.karlsruhe.digital"]

    wh.file_make_unique(config.path_sitemap_links_internal, sort=True)
    urls = config.path_sitemap_links_internal       
      
    urls = wh.list_from_file(urls)
    urls = wh.links_remove_comments(urls, '#')
    urls = wh.links_remove_excludes(urls, excludes) # <<<
    urls = wh.links_strip_query_and_fragment(urls) # do not need for snaps
    urls = wh.links_make_absolute(urls, config.base)
    urls = wh.links_replace(urls, config.replacements_pre) # is a specific issue besides general issues
    urls = wh.links_remove_externals(urls, config.base) 
    urls = wh.links_sanitize(urls)
        
    total_bytes     = 0
    unique_strips   = []
    for count, url in enumerate(urls):
        
        print("\n"*2)
        wh.progress(count / len(urls), verbose_string="TOTAL", VT=wh.CYAN, n=66)
        print()
        print(f"{wh.CYAN}[{(time.time() - start_secs)/60.0:.1f} m] abs_url: {url} {wh.RESET}")
            
        html = wh.get_content(url)
        soup = BeautifulSoup(html, "lxml")
        
        # delete out tags
        for script in soup(["script", "style"]):
            print("\t", "script:", wh.GRAY, script, wh.RESET)
            script.decompose() # get rid of each individual element
            
        strips = list(soup.stripped_strings)
        #print("\t", strips)
        
        bytes = 0
        for strip in strips:
            #print("\t\t", wh. GRAY, wh.dq(strip), wh.RESET)
            #print(wh.GRAY + '.' + wh.RESET, end='')
            total_bytes += len(strip)
            bytes += len(strip)
            unique_strips.append(strip)
        print(wh.MAGENTA + "." * int(bytes/10) + wh.RESET)
            
    print("stripped_strings: total_bytes:", total_bytes, "|", round(total_bytes / 1e6,1), "MB")
    
    wh.logo("get_project_total_size")
    perc100_saved, total_size_originals, total_size_unpowered = wh.get_project_total_size(
        config.project_folder, 
        prefix=config.base_netloc,
        use_pdf=False
        )
    
    content_ratio_original  = (total_bytes / total_size_originals) * 100
    content_ratio_unpowered = (total_bytes / total_size_unpowered) * 100
    print("content-ratio: content_ratio_original :", round(content_ratio_original,  1), "%")
    print("content-ratio: content_ratio_unpowered:", round(content_ratio_unpowered, 1), "%")
    
    # unique ratio
    total_bytes = 0
    unique_strips = wh.links_make_unique(unique_strips)
    #print(wh.GREEN, *unique_strips, wh.RESET, sep="\n\t")
    for strip in unique_strips:
        total_bytes += len(strip)
    
    content_ratio_original  = (total_bytes / total_size_originals) * 100
    content_ratio_unpowered = (total_bytes / total_size_unpowered) * 100
    print("unique content-ratio: content_ratio_original :", round(content_ratio_original,  1), "%", f"in book-pages: 1 page in {100/content_ratio_original:.0f}" )
    print("unique content-ratio: content_ratio_unpowered:", round(content_ratio_unpowered, 1), "%", f"in book-pages: 1 page in {100/content_ratio_unpowered:.0f}" )
    
    # info
    wh.get_file_sizes(config.folder_exported, use_pdf=True)
    wh.get_file_sizes(config.folder_exported, use_pdf=False)
    
    