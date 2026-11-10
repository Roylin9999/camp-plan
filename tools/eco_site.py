import json, math, random
random.seed(11)
K=0.38  # overall scale (v38: matched to Roy's drone video, Jimny 3.55 m as ruler)
M=450   # forest margin around the drawing
T=lambda px,py: (round((px-400)*2.2*K)+M, round((py-380)*3.4*K)+M)
W,D=round(3600*K)+2*M,round(3900*K)+2*M
gravel_px=[(525,1010),(545,950),(600,890),(680,850),(760,820),(850,780),(940,740),(1030,700),(1100,660),(1170,610),(1230,560),(1280,510),(1320,478),(1360,466),(1400,472),(1398,520),(1388,570),(1405,620),(1450,680),(1520,740),(1570,790),(1620,840),(1680,890),(1740,960),(1785,1030),(1815,1110),(1840,1200),(1870,1320),(1895,1440),(1910,1530),
 (1745,1530),(1720,1430),(1680,1330),(1620,1240),(1550,1170),(1470,1120),(1380,1095),(1300,1092),(1220,1110),(1160,1160),(1110,1220),(1040,1258),(950,1272),(850,1262),(760,1240),(680,1205),(600,1165),(548,1100)]
G=[T(*p) for p in gravel_px]
def poly_center(P):
    xs=[p[0] for p in P]; ys=[p[1] for p in P]; return ((min(xs)+max(xs))/2,(min(ys)+max(ys))/2)
def inside(P,x,y):
    c=False
    for i in range(len(P)):
        (x1,y1),(x2,y2)=P[i],P[(i+1)%len(P)]
        if (y1>y)!=(y2>y) and x < x1+(y-y1)*(x2-x1)/(y2-y1): c=not c
    return c
def dist_edge(P,x,y):
    best=1e9
    for i in range(len(P)):
        (x1,y1),(x2,y2)=P[i],P[(i+1)%len(P)]
        dx,dy=x2-x1,y2-y1; t=max(0,min(1,((x-x1)*dx+(y-y1)*dy)/(dx*dx+dy*dy or 1)))
        best=min(best,math.hypot(x-x1-t*dx,y-y1-t*dy))
    return best
def offset(P,k):
    n=len(P); area=sum(P[i][0]*P[(i+1)%n][1]-P[(i+1)%n][0]*P[i][1] for i in range(n)); s=1 if area>0 else -1
    out=[]
    for i in range(n):
        a,b=P[i-1],P[(i+1)%n]; nx,ny=(b[1]-a[1])*s,-(b[0]-a[0])*s; L=math.hypot(nx,ny) or 1
        kk=k*(0.75+0.5*random.random())
        out.append((round(P[i][0]+nx/L*kk),round(P[i][1]+ny/L*kk)))
    return out
soil=offset(G,70)
def rel(P):
    cx,cy=poly_center(P); return (round(cx),round(cy)), [[p[0]-round(cx),p[1]-round(cy)] for p in P]
def bbox(pts):
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]; return max(xs)-min(xs), max(ys)-min(ys)
gear={}
items=[]; uid=[0]
def add(gid,x,y,rot=0,lock=True):
    uid[0]+=1; it={"gearId":gid,"x":round(x),"y":round(y),"rot":rot,"uid":f"e{uid[0]}"}
    if lock: it["locked"]=True
    items.append(it)
(gc,gp)=rel(G); (sc,sp)=rel(soil)
w,d=bbox(gp); gear["g_eco_gravel3"]={"name":"碎石營位地面（生態區）","cat":"環境","shape":"patch","tex":"gravel","layer":1,"feather":50,"color":"#B9B9B6","w":w,"d":d,"h":1,"pts":gp,"notes":"杉林奇蹟生態區的碎石營位＋往營本部的碎石路，形狀依插圖估計"}
w,d=bbox(sp); gear["g_eco_soil3"]={"name":"泥土邊（生態區）","cat":"環境","shape":"patch","tex":"soil","layer":0,"feather":120,"color":"#8E7052","w":w,"d":d,"h":1,"pts":sp,"notes":"碎石地外圍的泥土邊，依插圖估計"}
add("g_eco_soil3",*sc); add("g_eco_gravel3",*gc)
gear["g_cedar_l"]={"name":"高聳柳杉","cat":"環境","shape":"tree","color":"#3F6B45","w":45,"d":45,"h":2000,"notes":"生態區的高大柳杉，尺寸估計"}
gear["g_broadleaf"]={"name":"闊葉樹","cat":"環境","shape":"bush","color":"#3E6B2F","w":650,"d":650,"h":1000,"notes":"原始林的闊葉大樹，尺寸估計"}
gear["g_broadleaf_s"]={"name":"闊葉小樹","cat":"環境","shape":"bush","color":"#4D7A36","w":420,"d":420,"h":600,"notes":"林緣的小樹，尺寸估計"}
gear["g_shrub"]={"name":"灌木叢","cat":"環境","shape":"bush","color":"#4D7A36","w":260,"d":230,"h":170,"notes":"林緣灌木，尺寸估計"}
gear["g_treefern"]={"name":"筆筒樹（樹蕨）","cat":"環境","shape":"fern","color":"#4C6B2C","w":380,"d":380,"h":420,"trunk":300,"notes":"插圖中的大型樹蕨，尺寸估計"}
gear["g_fern_s"]={"cat":"環境","color":"#3E6B35","d":150,"h":90,"name":"蕨類叢（小）","notes":"林下的蕨類植物，尺寸估計","shape":"fern","w":160}
gear["g_fern_l"]={"cat":"環境","color":"#3E6B35","d":300,"h":150,"name":"大蕨類叢","notes":"山坡上的大叢蕨類，尺寸估計","shape":"fern","w":300,"fronds":13}
gear["g_trashbin"]={"name":"垃圾桶（營區）","cat":"環境","shape":"cylinder","color":"#7E868C","w":45,"d":45,"h":75,"notes":"垃圾分類區的灰色桶子，尺寸估計"}
gear["g_trash_rack"]={"name":"垃圾分類台","cat":"環境","shape":"box","color":"#9AA1A6","w":110,"d":45,"h":90,"notes":"垃圾分類區的金屬分類櫃，尺寸估計"}
gear["g_bin_blue"]={"name":"藍色垃圾桶","cat":"環境","shape":"box","color":"#2F6DB5","w":50,"d":45,"h":85,"notes":"營位後方林緣的藍色桶，尺寸估計"}
gear["g_signboard"]={"name":"營區告示牌","cat":"環境","shape":"sign","color":"#2F4A3A","w":120,"d":12,"h":190,"notes":"往營本部路口的木框告示牌，尺寸估計"}
# facilities
add("g_washbasin",*T(1585,822),rot=-50)
add("g_trash_rack",*T(1625,858),rot=-50)
add("g_trashbin",*T(1608,880)); add("g_trashbin",*T(1640,893)); add("g_trashbin",*T(1665,905))
add("g_bin_blue",*T(1100,650),rot=-30)
add("g_signboard",*T(1712,935),rot=-55)
# cedars on the gravel (from the illustration)
for px,py in [(935,905),(1020,880),(1125,915),(1225,745),(1285,830),(1245,650),(1305,565),(1200,580)]:
    add("g_cedar_l",*T(px,py))
placed=[(i["x"],i["y"],120) for i in items if i["gearId"].startswith("g_cedar")]
def free(x,y,r):
    under=r<=130
    return all(math.hypot(x-a,y-b)>=r+(rr if (rr<=130 or not under) else 50) for a,b,rr in placed)
def scatter(gid,n,region,r,keep_out=150,tries=20000):
    region=[(0 if v==0 else W if v==3600 else v*K+M) if i%2==0 else (0 if v==0 else D if v==3900 else v*K+M) for i,v in enumerate(region)]; c=0
    for _ in range(tries):
        if c>=n: break
        x=random.uniform(region[0],region[2]); y=random.uniform(region[1],region[3])
        if not (0<=x<=W and 0<=y<=D): continue
        if inside(soil,x,y) or dist_edge(soil,x,y)<keep_out: continue
        if not free(x,y,r): continue
        placed.append((x,y,r)); add(gid,x,y,random.choice([0,45,90,135])); c+=1
# cedar grove behind (upper-left) - px region left/top
grove=(0,0,2000,1500)
scatter("g_cedar_l",22,grove,150,keep_out=60)
scatter("g_cedar",6,grove,150,keep_out=60)
# right side forest (east of road): px x>1450 above y 1100 → cm x>2300
scatter("g_broadleaf",7,(2400,0,3600,2600),250,keep_out=250)
scatter("g_cedar_l",5,(2300,0,3600,1300),150,keep_out=120)
scatter("g_broadleaf_s",5,(2300,0,3600,2600),180,keep_out=150)
# lower-left slope & front: smaller trees, tree ferns, ferns (keeps the view open like the illustration)
scatter("g_broadleaf",3,(0,1500,600,3000),250,keep_out=350)
scatter("g_broadleaf_s",3,(0,1500,800,2800),180,keep_out=250)
scatter("g_shrub",10,(0,2600,3600,3900),130,keep_out=80)
scatter("g_treefern",9,(0,1100,3600,3900),150,keep_out=90)
scatter("g_treefern",2,(2000,2400,2900,3900),150,keep_out=90)
# fringe of ferns and shrubs right along the soil edge
ring=offset(soil,110)
for i in range(0,len(ring)):
    a,b=ring[i],ring[(i+1)%len(ring)]
    L=math.hypot(b[0]-a[0],b[1]-a[1])
    for k in range(int(L//150)+1):
        t=k*150/L if L else 0; x=a[0]+(b[0]-a[0])*t+random.uniform(-40,40); y=a[1]+(b[1]-a[1])*t+random.uniform(-40,40)
        if not (0<=x<=W and 0<=y<=D) or inside(soil,x,y): continue
        gid=random.choice(["g_fern_s","g_fern_s","g_fern_l","g_fern_l","g_shrub"]); r={"g_fern_s":70,"g_fern_l":110,"g_shrub":110}[gid]
        if free(x,y,r): placed.append((x,y,r)); add(gid,x,y,random.choice([0,60,120]))
scatter("g_shrub",14,(0,0,3600,3900),130,keep_out=60)
scatter("g_fern_l",30,(0,0,3600,3900),130,keep_out=40)
scatter("g_fern_s",40,(0,0,3600,3900),80,keep_out=20)
layout={"kind":"site","name":"杉林奇蹟 生態區（照影片）","siteW":W,"siteD":D,"ground":"forest","sky":"day","items":items,"updatedAt":"2026-11-10T06:50:00.000Z"}
print(len(items), {g:sum(1 for i in items if i["gearId"]==g) for g in set(i["gearId"] for i in items)})
json.dump({"gear":gear,"layout":layout},open("eco.json","w"),ensure_ascii=False)
