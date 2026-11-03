/* ---- website cloud save (Firebase). Only used outside Claude, when firebase-config.js has a config. ---- */
async function fbInit(){
  if(!(window.FB_CONFIG && window.FB_CONFIG.apiKey && window.firebase)) return null;
  try{
    firebase.initializeApp(window.FB_CONFIG);
    const raw = firebase.firestore(), auth = firebase.auth();
    /* all data lives in collections named campplan_* so the Firebase project can be shared with other apps */
    const fs = { collection: c => raw.collection("campplan_" + c), batch: () => raw.batch() };
    await new Promise(r => { const off = auth.onAuthStateChanged(() => { off(); r(); }); });
    auth.getRedirectResult().catch(()=>{});
    const ui = () => {
      let b = document.getElementById("fbLogin");
      if(!b){ b = document.createElement("button"); b.id="fbLogin"; b.className="btn"; b.style.marginLeft="8px"; document.querySelector("header").appendChild(b);
        b.onclick = () => { if(auth.currentUser) return auth.signOut(); const p = new firebase.auth.GoogleAuthProvider();
          auth.signInWithPopup(p).catch(e => { if(/popup|operation-not-supported|web-storage/i.test(e.code||"")) auth.signInWithRedirect(p); else alert("登入失敗：" + (e.code||e.message)); }); }; }
      b.textContent = auth.currentUser ? "登出" : "登入（才能存檔）";
      b.className = auth.currentUser ? "btn" : "btn primary";
    };
    ui();
    auth.onAuthStateChanged(u => { ui(); if(u) fbSyncSeed(fs).catch(e => console.warn("seed", e)); if(S.ready) setStatus(u?"ok":"warn", u?"已同步到雲端":"未登入：可以看，但改動不會存"); });
    fbSyncSeed.auth = auth;
    return fs;
  }catch(e){ console.warn("firebase", e); return null; }
}
/* first sign-in fills the cloud from seed.json (+ this browser's saved layouts); a newer seedVersion adds new gear */
async function fbSyncSeed(fs){
  const j = await (await fetch("data/seed.json",{cache:"no-cache"})).json(); const sv = j.seedVersion||1;
  const meta = await fs.collection("meta").doc("seed").get(); const cur = meta.exists ? (meta.data().v||0) : 0;
  if(cur >= sv) return;
  const gearSnap = await fs.collection("gear").get(), laySnap = await fs.collection("layouts").get();
  let loc = {}; try{ loc = JSON.parse(localStorage.getItem("campplan.v1")||"{}"); }catch(e){}
  const writes = [];
  Object.entries(j.gear||{}).forEach(([k,v]) => writes.push(["gear",k,v]));
  if(gearSnap.empty) Object.entries(loc.gear||{}).forEach(([k,v]) => { if(!(j.gear||{})[k]) writes.push(["gear",k,v]); });
  const have = new Set(laySnap.docs.map(d=>d.id));
  const lays = laySnap.empty ? {...(j.layouts||{}), ...(loc.layouts||{})} : (j.layouts||{});
  Object.entries(lays).forEach(([k,v]) => { if(!have.has(k)) writes.push(["layouts",k,v]); });
  for(let i=0;i<writes.length;i+=400){ const b = fs.batch(); writes.slice(i,i+400).forEach(([c,k,v]) => b.set(fs.collection(c).doc(k), JSON.parse(JSON.stringify(v)))); await b.commit(); }
  await fs.collection("meta").doc("seed").set({v:sv});
}
