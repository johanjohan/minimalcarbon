import helpers_web as wh    
import config
import time
    
#-----------------------------------------
# 
#-----------------------------------------        

if __name__ == "__main__":
        
    files = wh.collect_files_endswith(config.project_folder, ["index.html", ".css", ".js", ".xml"])
    print("files", *files, sep="\n\t")
    time.sleep(5)
    
    files = wh.files_backup_or_restore_and_exclude(
        files, 
        postfix_orig=config.postfix_orig, 
        postfix_bup=None # config.postfix_bup
    ) 
    
    
    