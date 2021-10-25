import re
string = "<meta content=\"EDS-P510A-8PoE-2GTXSFP-T\" itemprop=\"model\"/>"
model = re.search("\w", string)
print(model)