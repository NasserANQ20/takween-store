import subprocess
HF='../hf/';V3='../v3/'
GR="eq=contrast=1.06:saturation=0.95:gamma=0.98,colorbalance=bs=0.03:bm=0.02:rh=-0.02"
N="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"
PUNCH="scale=w='trunc(1080*(1+0.07*max(0,1-t/0.25))/2)*2':h='trunc(1920*(1+0.07*max(0,1-t/0.25))/2)*2':eval=frame,crop=1080:1920"
def run(a): subprocess.run(['ffmpeg','-y','-loglevel','error']+a,check=True)
def clip(src,ss,dur,out,pre='',punch=True):
    vf=(pre+',' if pre else '')+f"tpad=stop_mode=clone:stop_duration=2,{N},trim=duration={dur},setpts=PTS-STARTPTS"+(','+PUNCH if punch else '')+f",{GR},format=yuv420p"
    run(['-ss',str(ss),'-i',src,'-vf',vf,'-an','-c:v','libx264','-crf','14','-preset','fast','-r','30',out])
def still(src,dur,out,z0=1.0,z1=1.06):
    zexp=f"({z0}+({z1}-{z0})*t/{dur})"
    vf=(f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,scale=2160:3840,fps=30,"
        f"scale=w='trunc(2160*{zexp}/2)*2':h='trunc(3840*{zexp}/2)*2':eval=frame,crop=2160:3840,scale=1080:1920,{PUNCH},{GR},setsar=1,format=yuv420p")
    run(['-loop','1','-t',str(dur),'-i',src,'-vf',vf,'-c:v','libx264','-crf','14','-preset','fast','-r','30',out])
def black(dur,out):
    run(['-f','lavfi','-i',f'color=c=black:s=1080x1920:r=30:d={dur}','-vf','format=yuv420p','-c:v','libx264','-crf','14',out])
black(1.5,'s01.mp4')
clip(HF+'v2.mp4',1.0,1.5,'s02.mp4')
clip(HF+'v3.mp4',1.0,1.5,'s03.mp4')
clip(HF+'v0.mp4',2.0,1.5,'s04.mp4')
clip(HF+'v1.mp4',1.0,3.0,'s05.mp4')
clip(V3+'ex.mp4',0,3.0,'s06.mp4',pre='setpts=PTS/1.68')
still(V3+'n0.png',1.0,'s07.mp4'); still(V3+'n1.png',1.0,'s08.mp4',1.06,1.0)
clip(V3+'dn.mp4',1.0,1.0,'s09.mp4'); still(V3+'n3.png',1.0,'s10.mp4')
still(V3+'n4.png',1.0,'s11.mp4',1.06,1.0); still(V3+'n7.png',1.0,'s12.mp4')
clip(HF+'v4.mp4',0.5,3.0,'s13.mp4')
clip(HF+'v5.mp4',0.5,2.5,'s14.mp4')
clip(HF+'v7.mp4',1.5,2.5,'s15.mp4')
black(4.0,'s16.mp4')
open('list.txt','w').write(''.join(f"file 's{i:02d}.mp4'\n" for i in range(1,17)))
run(['-f','concat','-safe','0','-i','list.txt','-c','copy','base.mp4'])
print('ok')
