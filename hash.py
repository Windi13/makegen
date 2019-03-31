
import hashlib

# This module provides the functionality to generate a hash over a number of given files
# This can be used to establish if the structure or number of files has changed
def calc_hash(sources):
    m = hashlib.md5()
    k = ""
    for s in sources:
        m.update(s.encode('utf-8'))
        k += s
        
    return m.hexdigest()