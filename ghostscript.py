# https://stackoverflow.com/questions/27631940/python-script-to-compress-all-pdf-files-in-a-directory-on-windows-7
#from __future__ import print_function
import os
import subprocess

import helpers_web as wh

gs_exe  = 'C:/Program Files/gs/gs9.56.1/bin/gswin64c.exe'

# https://gist.github.com/ahmed-musallam/27de7d7c5ac68ecbd1ed65b6b48416f9
# https://stackoverflow.com/questions/27631940/python-script-to-compress-all-pdf-files-in-a-directory-on-windows-7
""" 
Other options for PDFSETTINGS:

    /screen selects low-resolution output similar to the Acrobat Distiller "Screen Optimized" setting.
    /ebook selects medium-resolution output similar to the Acrobat Distiller "eBook" setting.
    /printer selects output similar to the Acrobat Distiller "Print Optimized" setting.
    /prepress selects output similar to Acrobat Distiller "Prepress Optimized" setting.
    /default selects output intended to be useful across a wide variety of uses, possibly at the expense of a larger output file.

https://www.ghostscript.com/doc/current/Use.htm

"""
def compress_pdf(in_path, out_path, compression='/screen', res=144, compat='1.4', sample_type="/Bicubic"):
    
    print("compress_pdf:", "in_path    :", wh.CYAN, os.path.basename(in_path),  wh.RESET)
    print("compress_pdf:", "out_path   :", wh.CYAN, os.path.basename(out_path), wh.RESET)
    print("compress_pdf:", "res        :", wh.YELLOW, res, wh.RESET)
    print("compress_pdf:", "compression:", compression)
    print("compress_pdf:", "compat     :", compat)
    print("compress_pdf:", gs_exe)
    
    p = subprocess.Popen([  
                            gs_exe,
                            
                            '-sDEVICE=pdfwrite', 
                            
                            f'-dCompatibilityLevel={compat}', 
                            f'-dPDFSETTINGS={compression}', 
                            
                            # '-dEmbedAllFonts=true,',
                            # '-dSubsetFonts=true',
                            
                            f'-dColorImageDownsampleType={sample_type}',
                            f'-dColorImageResolution={res}',
                            f'-dGrayImageDownsampleType={sample_type}',
                            f'-dGrayImageResolution={res}',
                            f'-dMonoImageDownsampleType={sample_type}',
                            f'-dMonoImageResolution={res}',
                            
                            '-dNOPAUSE', 
                            '-dBATCH', 
                            '-dQUIET', 
                            '-dSAFER',
                            f'-sOutputFile={out_path}', # may need to quote
                            in_path
                        ], 
                        stdout=subprocess.PIPE
                        )
    print (p.communicate())
            