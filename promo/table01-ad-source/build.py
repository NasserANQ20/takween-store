import subprocess
T=37.5; d=0.5
B=[0,4,8.5,12,15.5,19.5,23.5,27.2,31.8]
SS=[0.15,0.0,0.2,0.2,0.1,0.2,0.2,0.1]      # in-points in source clips
ins=[];fc=[]
grade="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,eq=contrast=1.05:saturation=1.03:gamma=0.98,format=yuv420p"
for i in range(8):
    ln=(B[i+1]-B[i])+(d/2 if i==0 else d)
    ins+=['-i',f'v{i}.mp4']
    fc.append(f"[{i}:v]trim=start={SS[i]},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=1,trim=duration={ln:.3f},setpts=PTS-STARTPTS,{grade},settb=1/30[s{i}]")
# end card background
ins+=['-loop','1','-t',f'{T-B[8]+d:.3f}','-i','card_end.png']
fc.append(f"[8:v]scale=1080:1920,fps=30,zoompan=z='1+0.0006*on':d=1:s=1080x1920:fps=30,format=yuv420p,settb=1/30[s8]")
prev='s0'
for k in range(8):
    tr='fadeblack' if k==0 else ('fade' if k==7 else 'smoothleft' if k in (2,5) else 'fade')
    dur=0.35 if k==0 else (0.7 if k==7 else d)
    off=B[k+1]-dur/2
    fc.append(f"[{prev}][s{k+1}]xfade=transition={tr}:duration={dur}:offset={off:.3f}[x{k}]"); prev=f'x{k}'
fc.append(f"[{prev}]vignette=PI/5,noise=alls=3:allf=t,format=yuv420p[base]")
caps=[('c0',0.5,3.6),('c1',4.5,8.0),('c2',8.9,11.7),('c3',12.4,15.2),('c4',15.9,19.2),('c5',19.9,23.2),('c6',23.9,26.9),('c7',27.6,31.3),
      ('e1',32.25,37.0),('e2',32.85,37.0),('e3',33.6,37.0),('e4',34.3,37.0)]
prev='base';n=9
for name,a,b in caps:
    ins+=['-loop','1','-t',str(T),'-i',f'card_{name}.png']
    fo=f"fade=t=out:st={b}:d=0.4:alpha=1," if b<37 else ""
    fc.append(f"[{n}:v]format=rgba,fade=t=in:st={a}:d=0.5:alpha=1,{fo}setpts=PTS-STARTPTS[o{n}]")
    fc.append(f"[{prev}][o{n}]overlay=x=0:y='if(lt(t,{a}),36,36*max(0,1-(t-{a})/0.7))':eval=frame:enable='between(t,{a-0.05},{b+0.5})'[v{n}]")
    prev=f'v{n}';n+=1
fc.append(f"[{prev}]fade=t=out:st={T-0.7}:d=0.7,format=yuv420p[vout]")
ins+=['-i','score.wav']
fc.append(f"[{n}:a]loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=out:st={T-1.0}:d=1.0[aout]")
cmd=['ffmpeg','-y','-loglevel','error']+ins+['-filter_complex',';'.join(fc),'-map','[vout]','-map','[aout]','-t',str(T),
 '-c:v','libx264','-preset','slow','-crf','19','-profile:v','high','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','takween-table01-ad.mp4']
subprocess.run(cmd,check=True);print('done')
