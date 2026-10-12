const {chromium}=require('/opt/node-tools/node_modules/playwright');const path=require('path');
(async()=>{const [out,stills]=process.argv.slice(2);const d=__dirname;
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+path.join(d,'ov.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1500);
const ts=stills?stills.split(',').map(Number):Array.from({length:900},(_,i)=>i/30);let i=0;
for(const t of ts){await p.evaluate(t=>window.__seek(t),t);await p.screenshot({path:path.join(out,stills?`o_${t}.png`:`o${String(i).padStart(4,'0')}.png`),omitBackground:true});i++}
await b.close()})();
