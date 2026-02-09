# Temporary fix for removed 'cgi' module in Python 3.13
def parse_header(line):
    parts = line.split(";")
    key = parts[0].strip().lower()
    pdict = {}
    for item in parts[1:]:
        if "=" in item:
            k, v = item.split("=", 1)
            pdict[k.strip().lower()] = v.strip().strip('"')
    return key, pdict