import re
string = '<meta content="EDS-P510A-8PoE-2GTXSFP-T" itemprop="model"/>'
model = re.search("\".+?\"", string)
model = model.group()
model = re.sub("\"", "", str(model))
print(model)