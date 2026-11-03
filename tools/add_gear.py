"""Add or replace one gear item on the website: converts its model, updates seed.json and writes the cloud doc.
Usage: python3 add_gear.py <gear_id> <gear.json> [model_asset.json] [model_file_name]"""
import json, sys, os, struct, base64, urllib.request
here = os.path.dirname(os.path.abspath(__file__)); site = os.path.dirname(here)
gid, gfile = sys.argv[1], sys.argv[2]
g = json.load(open(gfile)); g.pop('modelId', None)
if len(sys.argv) > 3:
    j = json.load(open(sys.argv[3]))
    if '__glb_base64' in j: glb = base64.b64decode(j['__glb_base64'])
    else:
        parts = [base64.b64decode(b['uri'].split(',',1)[1]) for b in j.get('buffers',[])]; starts=[]; data=b''
        for p in parts: starts.append(len(data)); data += p; data += b'\0'*((4-len(data)%4)%4)
        for v in j.get('bufferViews',[]): v['byteOffset']=v.get('byteOffset',0)+starts[v.get('buffer',0)]; v['buffer']=0
        j['buffers']=[{'byteLength':len(data)}]
        js=json.dumps(j,separators=(',',':')).encode(); js+=b' '*((4-len(js)%4)%4)
        glb=struct.pack('<III',0x46546C67,2,12+8+len(js)+8+len(data))+struct.pack('<II',len(js),0x4E4F534A)+js+struct.pack('<II',len(data),0x004E4942)+data
    name = sys.argv[4] if len(sys.argv) > 4 else gid + '.glb'
    open(os.path.join(site,'models',name),'wb').write(glb); g['model'] = 'models/' + name
sp = os.path.join(site,'data','seed.json'); sd = json.load(open(sp)); sd['gear'][gid] = g
json.dump(sd, open(sp,'w'), ensure_ascii=False, indent=1)
cfg = open(os.path.join(site,'firebase-config.js')).read()
key = cfg.split('apiKey: "')[1].split('"')[0]; proj = cfg.split('projectId: "')[1].split('"')[0]
body = json.dumps({"fields":{"_json":{"stringValue":json.dumps(g,ensure_ascii=False,separators=(',',':'))}}}).encode()
url = f"https://firestore.googleapis.com/v1/projects/{proj}/databases/(default)/documents/campplan_gear/{gid}?key={key}"
print(gid, urllib.request.urlopen(urllib.request.Request(url, data=body, method='PATCH', headers={'Content-Type':'application/json'})).status)
