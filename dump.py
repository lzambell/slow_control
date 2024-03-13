import json
#from json import JSONEncoder



def dump_offline(out, infos):
    extension = out[out.rfind(".")+1:]
    print(extension)
    if((extension == "dat") or (extension == "txt")):
        dump_offline_txt(out, infos)
    elif(extension == "json"):
        dump_offline_json(out, infos)
    elif(extension == "root"):
        dump_offline_root(out, infos)
    else:
        print(" I don't know this type of file :", extension)
    
        
def dump_offline_txt(out, infos):
    print(" text output")
    with open(out, "w") as file:
        for (key, value) in infos.items():
            file.write('{0}\t {1}\n'.format(key, value))

def dump_offline_json(out, infos):
    print('dumping in ', out)
    
    with open(out, 'w') as file:        
        file.write("values=")
        #for (key, value) in infos.items():
        file.write(json.dumps(infos, indent=2))
        
def dump_offline_root(out, infos):
    print(" root output requested ... to be done")
