import subprocess, os
H='../hf/'
T=42.0
N="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,format=yuv420p"
def vid(src,ss,dur,out):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(ss),'-i',src,'-t',str(dur),'-vf',f"tpad=stop_mode=clone:stop_duration=2,{N},trim=duration={dur}",'-an','-c:v','libx264','-crf','14','-preset','fast',out],check=True)
def still(src,dur,out,z0=1.0,z1=1.07,dy=0):
    zexp=f"({z0}+({z1}-{z0})*t/{dur})"
    vf=(f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,scale=2160:3840,fps=30,"
        f"scale=w='trunc(2160*{zexp}/2)*2':h='trunc(3840*{zexp}/2)*2':eval=frame,"
        f"crop=2160:3840:'(iw-2160)/2':'(ih-3840)/2+{dy}*t/{dur}',scale=1080:1920,setsar=1,format=yuv420p")
    subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-t',str(dur),'-i',src,'-vf',vf,'-c:v','libx264','-crf','14','-preset','fast',out],check=True)
segs=[]
def S(name,fn,*a,**k):
    out=f'seg_{name}.mp4'
    if not os.path.exists(out): fn(*a,out,**k) if fn is vid else fn(*a,out,**k)
    segs.append(out)
S('a',vid,H+'v0.mp4',0.3,2.4)
S('b',vid,H+'v1.mp4',2.6,2.4)
S('c0',still,'n0.png',2.4,z0=1.0,z1=1.08)
S('c1',still,'n1.png',2.4,z0=1.09,z1=1.0)
S('c2',vid,'dn.mp4',0.4,2.4)
S('c3',still,'n3.png',2.4,z0=1.0,z1=1.08)
S('c4',still,'n4.png',2.4,z0=1.02,z1=1.09,dy=-60)
S('c5',still,'n7.png',2.4,z0=1.09,z1=1.0)
for i,src in enumerate(['n0.png','n1.png','n2.png','n3.png','n4.png','n7.png']):
    S(f'f{i}',still,src,0.2,z0=1.12,z1=1.18)
S('blk',still,'blk.png',1.6,z0=1.0,z1=1.0)
S('ex',vid,'ex.mp4',0.0,4.8)
S('exs',still,'n6.png',5.2,z0=1.0,z1=1.0)
S('s1',vid,H+'v4.mp4',0.4,2.4)
S('s2',vid,H+'v5.mp4',0.6,2.4)
S('end',still,'k_end.png',5.2,z0=1.0,z1=1.04)
with open('list.txt','w') as f:
    for s in segs: f.write(f"file '{s}'\n")
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','list.txt','-c','copy','base.mp4'],check=True)
# overlays
caps=[('hook',0.3,2.25),('t01',2.6,4.7),
 ('col0',4.95,7.1),('col1',7.35,9.5),('col2',9.75,11.9),('col3',12.15,14.3),('col4',14.55,16.7),('col5',16.95,19.1),
 ('inq',20.55,21.95),('ins',27.1,31.9)]
caps+=[(f'call{k}',27.2+0.68*k,(27.2+0.68*(k+1)) if k<6 else 31.9) for k in range(7)]
caps+=[('svc1',32.2,34.3),('svc2',34.6,36.7),('e1',37.0,99),('e2',37.6,99),('e3',38.3,99),('e4',39.0,99)]
ins=['-i','base.mp4'];fc=[];prev='0:v';n=1
for name,a,b in caps:
    ins+=['-loop','1','-t',str(T),'-i',f'k_{name}.png']
    call=name.startswith('call')
    fi=0.12 if call else 0.3
    fo='' if (b>=99 or call) else f"fade=t=out:st={b-0.2}:d=0.2:alpha=1,"
    fc.append(f"[{n}:v]format=rgba,fade=t=in:st={a}:d={fi}:alpha=1,{fo}setpts=PTS-STARTPTS[o{n}]")
    rise=0 if call else 30
    fc.append(f"[{prev}][o{n}]overlay=x=0:y='if(lt(t,{a}),{rise},{rise}*max(0,1-(t-{a})/0.5))':eval=frame:enable='between(t,{a-0.02},{min(b,T)+0.02})'[v{n}]")
    prev=f'v{n}';n+=1
# beat flashes
fc.append(f"[{prev}]eq=contrast=1.04:saturation=1.04,vignette=PI/5,noise=alls=3:allf=t,"
          "fade=t=in:st=0:d=0.4,"
                    f"fade=t=out:st={T-0.7}:d=0.7,format=yuv420p[vf]")
ins+=['-i','score2.wav']
fc.append(f"[{n}:a]loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={T-1.0}:d=1.0[af]")
subprocess.run(['ffmpeg','-y','-loglevel','error']+ins+['-filter_complex',';'.join(fc),'-map','[vf]','-map','[af]','-t',str(T),
 '-c:v','libx264','-preset','slow','-crf','20','-profile:v','high','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','takween-tables-collection.mp4'],check=True)
print('done')
