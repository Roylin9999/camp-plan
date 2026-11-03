"""Export artifact db + model assets to the site.
Usage: python3 export_models.py <export_dir with gear/ layouts/ models/> <site_dir> <seedVersion>
Bump seedVersion each update so existing visitors receive new/changed gear (their own layouts are kept)."""
import json,base64,struct,os,sys,glob
ex=sys.argv[1]; out=sys.argv[2]
gear={}; lay={}
for f in glob.glob(ex+'/gear/*.json'):
    gear[os.path.basename(f)[:-5]]=json.load(open(f))
for f in glob.glob(ex+'/layouts/*.json'):
    lay[os.path.basename(f)[:-5]]=json.load(open(f))
def to_glb(j):
    if '__glb_base64' in j: return base64.b64decode(j['__glb_base64'])
    bufs=j.get('buffers',[]); parts=[base64.b64decode(b['uri'].split(',',1)[1]) for b in bufs]
    starts=[];data=b''
    for p in parts:
        starts.append(len(data)); data+=p; data+=b'\0'*((4-len(data)%4)%4)
    for v in j.get('bufferViews',[]):
        v['byteOffset']=v.get('byteOffset',0)+starts[v.get('buffer',0)]; v['buffer']=0
    j['buffers']=[{'byteLength':len(data)}]
    js=json.dumps(j,separators=(',',':')).encode(); js+=b' '*((4-len(js)%4)%4)
    total=12+8+len(js)+8+len(data)
    return struct.pack('<III',0x46546C67,2,total)+struct.pack('<II',len(js),0x4E4F534A)+js+struct.pack('<II',len(data),0x004E4942)+data
for gid,g in gear.items():
    if 'modelId' in g:
        j=json.load(open(f"{ex}/models/{g['modelId']}.json"))
        open(f"{out}/models/{gid}.glb",'wb').write(to_glb(j))
        g['model']=f"models/{gid}.glb"; del g['modelId']
seedv=int(sys.argv[3]) if len(sys.argv)>3 else 1
json.dump({'seedVersion':seedv,'gear':gear,'layouts':lay},open(f'{out}/data/seed.json','w'),ensure_ascii=False,indent=1)
print(len(gear),len(lay))
