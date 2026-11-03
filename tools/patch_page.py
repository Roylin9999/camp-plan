"""Turn the Claude artifact HTML into the standalone GitHub Pages index.html.
Usage: python3 patch_page.py artifact.html index.html"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
def rep(a,b):
    global s
    assert a in s, a[:60]; s=s.replace(a,b,1)
rep('if(!db){ S.mode="local"; S.ready=true; setStatus("warn","只存在這台裝置的瀏覽器"); renderAll(); return; }',
'''if(!db){ S.mode="local";
    if(!Object.keys(S.gear).length){ try{ const j = await (await fetch("data/seed.json",{cache:"no-cache"})).json(); S.gear=j.gear||{}; S.layouts=j.layouts||{}; lsSave(); }catch(e){} }
    S.ready=true; setStatus("warn","資料存在這台裝置的瀏覽器"); renderAll(); return; }''')
rep('const assets = window.claude && await claude.use("assets"); if(!assets){ msg.textContent="這個畫面不能上傳檔案（需要編輯權限）。"; return; }',
'''const assets = window.claude && await claude.use("assets");
      if(!assets){ if(f.size>3e6){ msg.textContent="檔案太大（超過 3MB），網站版請把 .glb 放進 GitHub 的 models 資料夾。"; return; }
        const u = await new Promise((res,rej)=>{ const r=new FileReader(); r.onload=()=>res(r.result); r.onerror=rej; r.readAsDataURL(f); });
        S.gear[id].model=u; delete S.gear[id].modelId; saveGear(id); renderGearPane(); rebuildScene(); return; }''')
rep('<!doctype html><html><head><meta charset=utf8>','<!doctype html><html lang="zh-Hant"><head><meta charset=utf-8>')
rep('display:none!important}</style></head><body>\n<title>露營平配</title>','display:none!important}</style><title>露營平配</title></head><body>')
for f in ['build/three.min.js','examples/js/controls/OrbitControls.js','examples/js/loaders/GLTFLoader.js']:
    rep('https://cdn.jsdelivr.net/npm/three@0.147.0/'+f, 'vendor/'+f.split('/')[-1])
open(sys.argv[2],'w',encoding='utf8').write(s)
