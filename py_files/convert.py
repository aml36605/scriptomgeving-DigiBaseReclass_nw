
def convert_bytes(bytes):

    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2f (Tb)' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2f (Gb)' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2f (Mb)' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2f (Kb)' % kilobytes
    else:
        size = '%.2f (b)' % bytes
    return size