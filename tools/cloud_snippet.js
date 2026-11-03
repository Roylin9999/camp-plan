/* ---- website cloud save (Firebase). Only used outside Claude, when firebase-config.js has a config.
   No sign-in: anyone with the link can view and edit (Roy's choice). ---- */
async function fbInit(){
  if(!(window.FB_CONFIG && window.FB_CONFIG.apiKey && window.firebase)) return null;
  try{
    firebase.initializeApp(window.FB_CONFIG);
    const raw = firebase.firestore();
    /* all data lives in collections named campplan_* so the Firebase project can be shared with other apps */
    const fs = { collection: c => raw.collection("campplan_" + c), batch: () => raw.batch() };
    /* fill the cloud before showing it; if the cloud can't be reached or written, stay on this browser's copy */
    await fbSyncSeed(fs);
    return fs;
  }catch(e){ console.warn("firebase", e); return null; }
}
/* first visit fills the cloud from seed.json (+ this browser's saved layouts); a newer seedVersion adds new gear */
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
