"""
Utility file used to convert a dictionary into a JSON string
"""

def extractJSONvalue(v):
    """
    Convert the given value into a proper JSON value
    """
    if type(v) is str:
        return "\""+v+"\""
    else:
        return str(v)
        
def convertJSON(dicObj,keys_sorted,nulledKeys):
    """
    Convert the given keys contained in the dictionary into JSON string. 
    It conserves the order of 'key_sorted'. If a key is missing, its value will be "".
    dicObj : the source dictionary
    keys_sorted : a list of keys, which must be present in the final JSON string
    nulledKeys: a list of keys that should be set to "" if present in 'keys_sorted'
    """
    first = True
    finalStr = "{"
    for j in keys_sorted:
        if not first:
            finalStr += ", "
        else:
            first = False
        finalStr += "\"" + j + "\": " + extractJSONvalue("" if ((not (j in dicObj)) or (j in nulledKeys)) else dicObj[j])
    finalStr += "}"
    return finalStr