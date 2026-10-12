import subprocess
HF='../hf/';V3='../v3/'
N="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"
PUNCH="scale=w='trunc(1080*(1+0.08*max(0,1-t/0.3))/2)*2':h='trunc(1920*(1+0.08*max(0,1-t/0.3))/2)*2':eval=frame,crop=1080:1920"
def run(a): subprocess.run(['ffmpeg','-y','-loglevel','error']+a,check=True)
def clip(src,ss,dur,out,pre='',punch=True):
    vf=(pre+',' if pre else '')+f"tpad=stop_mode=clone:stop_duration=2,{N},trim=duration={dur},setpts=PTS-STARTPTS"+(','+PUNCH if punch else '')+",format=yuv420p"
    run(['-ss',str(ss),'-i',src,'-vf',vf,'-an','-c:v','libx264','-crf','14','-preset','fast','-r','30',out])
def frames(pat,out):
    run(['-framerate','30','-i',pat,'-vf','format=yuv420p,setsar=1','-c:v','libx264','-crf','14','-preset','fast','-r','30',out])
clip(HF+'v2.mp4',0.5,1.5,'A1.mp4')
clip(HF+'v0.mp4',1.5,1.5,'A2.mp4')
clip(HF+'v3.mp4',0.5,1.0,'B1.mp4')
clip(V3+'dn.mp4',1.5,1.0,'B2.mp4')
clip(V3+'ex.mp4',0,1.4,'B3.mp4',pre='reverse,setpts=PTS/3.6')
clip(HF+'v1.mp4',4.0,0.8,'B4.mp4')
frames('car/f%04d.jpg','C.mp4')
frames('pri/f%04d.jpg','D.mp4')
clip(V3+'ex.mp4',0,3.6,'E.mp4',pre='setpts=PTS/1.4',punch=False)
frames('pk/p%04d.jpg','F.mp4')
segs=['A1','A2','B1','B2','B3','B4','C','D','E','F']
open('l3.txt','w').write(''.join(f"file '{s}.mp4'\n" for s in segs))
run(['-f','concat','-safe','0','-i','l3.txt','-c','copy','base3.mp4'])
T=30.0
caps=[('h_h1',0.15,1.45),('h_h2',1.55,2.92),('h_in',19.35,22.6)]
ins=['-i','base3.mp4'];fc=[];prev='0:v';n=1
for name,a,b in caps:
    ins+=['-loop','1','-t',str(T),'-i',name+'.png']
    fc.append(f"[{n}:v]format=rgba,fade=t=in:st={a}:d=0.18:alpha=1,fade=t=out:st={b-0.15}:d=0.15:alpha=1[o{n}]")
    fc.append(f"[{prev}][o{n}]overlay=0:'if(lt(t,{a}),40,40*max(0,1-(t-{a})/0.35))':eval=frame:enable='between(t,{a},{b})'[v{n}]");prev=f'v{n}';n+=1
fc.append(f"[{prev}]eq=contrast=1.03:saturation=1.04,noise=alls=3:allf=t,fade=t=in:st=0:d=0.25,fade=t=out:st={T-0.5}:d=0.5,format=yuv420p[vf]")
ins+=['-i','score3.wav']
fc.append(f"[{n}:a]loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={T-0.6}:d=0.6[af]")
run(ins+['-filter_complex',';'.join(fc),'-map','[vf]','-map','[af]','-t',str(T),'-c:v','libx264','-preset','slow','-crf','19','-profile:v','high','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','takween-table01-30s.mp4'])
print('done')
