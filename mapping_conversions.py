import datetime

DATETIME_CONVERTER = {
    (str, datetime.date): lambda s: datetime.date(*map(int, s.split("-"))),
    (datetime.date, str): lambda d: d.strftime("%d-%m-%Y"),
}

def convert_keys(doc, mapping, inverse=False):
    return convert_keys_with_converter(doc, mapping, DATETIME_CONVERTER, inverse=False)

def convert_keys_with_converter(doc, mapping, converters, inverse=False):
    converted = {}
    for keys1, type1, keys2, type2 in mapping:
        
        if inverse:
            keys1, type1, keys2, type2 = keys2, type2, keys1, type1
            
        converter = converters.get((type1, type2), type2)
        keys1 = keys1.split('.')
        keys2 = keys2.split('.')
        obj1 = doc
        
        while keys1:
            k, *keys1 = keys1
            if(k in obj1):
                converted[keys2[0]] = converter(obj1[k])
                
    return converted

