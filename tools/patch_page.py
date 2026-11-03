"""Turn the Claude artifact HTML into the standalone GitHub Pages index.html.
Usage: python3 patch_page.py artifact.html index.html"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
def rep(a,b):
    global s
    assert a in s, a[:60]; s=s.replace(a,b,1)
rep('if(!db){ S.mode="local"; S.ready=true; setStatus("warn","只存在這台裝置的瀏覽器"); renderAll(); return; }',
'''if(!db){ S.mode="local";
    try{ const j = await (await fetch("data/seed.json",{cache:"no-cache"})).json(); const sv=j.seedVersion||1, mine=+(localStorage.getItem("campplan.seed")||0);
      if(!Object.keys(S.gear).length){ S.gear=j.gear||{}; S.layouts=j.layouts||{}; }
      else if(sv>mine){ Object.assign(S.gear, j.gear||{}); Object.entries(j.layouts||{}).forEach(([k,v])=>{ if(!S.layouts[k]) S.layouts[k]=v; }); }
      lsSave(); localStorage.setItem("campplan.seed", String(sv)); }catch(e){}
    S.ready=true; setStatus("warn","資料存在這台裝置的瀏覽器"); renderAll(); return; }''')
rep('const assets = window.claude && await claude.use("assets"); if(!assets){ msg.textContent="這個畫面不能上傳檔案（需要編輯權限）。"; return; }',
'''const assets = window.claude && await claude.use("assets");
      if(!assets){ if(f.size>3e6){ msg.textContent="檔案太大（超過 3MB），網站版請把 .glb 放進 GitHub 的 models 資料夾。"; return; }
        const u = await new Promise((res,rej)=>{ const r=new FileReader(); r.onload=()=>res(r.result); r.onerror=rej; r.readAsDataURL(f); });
        S.gear[id].model=u; delete S.gear[id].modelId; saveGear(id); renderGearPane(); rebuildScene(); return; }''')
rep('<!doctype html><html><head><meta charset=utf8>','<!doctype html><html lang="zh-Hant"><head><meta charset=utf-8>')
rep('display:none!important}</style></head><body>\n<title>露營平配</title>','display:none!important}</style><title>露營平配</title></head><body>')
import re, os
vend=os.path.join(os.path.dirname(os.path.abspath(sys.argv[2])),'vendor')
for f in re.findall(r'https://cdn\.jsdelivr\.net/npm/three@0\.147\.0/([\w/.]+\.js)', s):
    name=f.split('/')[-1]
    assert os.path.exists(os.path.join(vend,name)), 'missing vendor/'+name+' (copy it from the three@0.147.0 npm package)'
    rep('https://cdn.jsdelivr.net/npm/three@0.147.0/'+f, 'vendor/'+name)
assert 'cdn.jsdelivr' not in s
snippet=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cloud_snippet.js'),encoding='utf8').read()
rep('async function initStore(){', snippet+'\nasync function initStore(){')
rep('try { if(window.claude && claude.use) db = await claude.use("db"); } catch(e){ db = null; }',
    'try { if(window.claude && claude.use) db = await claude.use("db"); } catch(e){ db = null; }\n  if(!db) db = await fbInit();')
rep('setStatus("ok","已同步到雲端"); renderAll(); } };', 'setStatus("ok","已同步到雲端"); if(fbSyncSeed.auth && !fbSyncSeed.auth.currentUser) setStatus("warn","未登入：可以看，但改動不會存"); renderAll(); } };')
rep('<script src="vendor/CSS3DRenderer.js"></script>', '<script src="vendor/CSS3DRenderer.js"></script>\n<script src="vendor/firebase-app-compat.js"></script>\n<script src="vendor/firebase-auth-compat.js"></script>\n<script src="vendor/firebase-firestore-compat.js"></script>\n<script src="firebase-config.js"></script>')
rep('if(f.size>3e6){ msg.textContent="檔案太大（超過 3MB）', 'if(f.size>7e5){ msg.textContent="檔案太大（超過 700KB）')

open(sys.argv[2],'w',encoding='utf8').write(s)
