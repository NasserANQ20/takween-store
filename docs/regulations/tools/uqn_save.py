# حفظ صفحة نظام/قرار من جريدة أم القرى كملف Markdown.
# الاستخدام: python3 docs/regulations/tools/uqn_save.py "<رابط uqn.gov.sa>" "<المسار/الملف_uqn.md>"
import re,html,subprocess,sys,datetime
url,out=sys.argv[1],sys.argv[2]
s=subprocess.run(['curl','-sSL','--max-time','60',url],capture_output=True,text=True).stdout
title=html.unescape(re.search(r'<meta property="og:title" content="([^"]*)"',s).group(1))
pub=re.search(r'"datePublished": "([^"]+)"',s); pub=pub.group(1)[:10] if pub else ''
m=re.search(r'<article id="article-content"[^>]*>(.*?)</article>',s,re.S)
b=m.group(1)
b=re.sub(r'<(br|/div|/p|/tr|/h\d|/li)[^>]*>','\n',b)
b=re.sub(r'</t[dh]>',' | ',b)
b=html.unescape(re.sub(r'<[^>]+>','',b))
b=re.sub(r'[ \t ‏‎]+',' ',b)
lines=[l.strip() for l in b.split('\n')]
o=[]
for l in lines:
    if not l: continue
    if re.match(r'^(المادة|الفصل|الباب)\s',l) and len(l)<60: o.append('\n### '+l)
    else: o.append(l)
txt='\n'.join(o)
open(out,'w',encoding='utf8').write(f"# {title}\n\n> المصدر الرسمي: جريدة أم القرى — {url}\n> تاريخ النشر على الموقع: {pub}\n> نُسخ آلياً بتاريخ {datetime.date.today()} للاستخدام المرجعي؛ عند الاستناد الرسمي ارجع للمصدر.\n\n{txt}\n")
print(out, title, pub, len(txt))
