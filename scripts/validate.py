#!/usr/bin/env python3
"""Validate a built Jekyll site; Python standard library only. No network requests."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,unquote
import json,sys,xml.etree.ElementTree as ET,collections
class Document(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=True);self.links=[];self.ids=set();self.images=0;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='a' and 'name' in a:self.ids.add(a['name'])
  if tag=='img':self.images+=1
  for attr in ('href','src','poster'):
   if a.get(attr):self.links.append((tag,attr,a[attr]))
  if a.get('srcset'):
   for src in a['srcset'].split(','):self.links.append((tag,'srcset',src.strip().split()[0]))
def validate(root,base=''):
 root=Path(root).resolve();htmlfiles=sorted(root.rglob('*.html'));docs={};errors=[];external=set();refs=0;fragments=0
 def target(path):
  path=unquote(path)
  if base and path.startswith(base+'/'):path=path[len(base):]
  elif base and path==base:path='/'
  p=root/path.lstrip('/')
  if p.is_dir():p=p/'index.html'
  return p
 for p in htmlfiles:
  text=p.read_text()
  if '{{' in text or '{%' in text:errors.append({'file':str(p.relative_to(root)),'issue':'Unrendered Liquid'})
  docs[p]=Document(text)
 for p,d in docs.items():
  rel='/'+p.relative_to(root).as_posix();url=rel.removesuffix('index.html') if rel.endswith('/index.html') else rel
  for tag,attr,u in d.links:
   parsed=urlsplit(u)
   if parsed.scheme in ('mailto','tel','data'):continue
   if parsed.hostname and parsed.hostname not in ('www.masaomori.net','masaomori.net','masaomori.github.io'):
    external.add(u);continue
   if parsed.scheme and parsed.scheme not in ('http','https'):errors.append({'file':rel,'issue':'Unsupported scheme','url':u});continue
   dest=urlsplit(urljoin(base+url,u));t=target(dest.path);refs+=1
   if not t.is_relative_to(root) or not t.is_file():errors.append({'file':rel,'issue':'Missing local target','url':u});continue
   if dest.fragment and t in docs:
    fragments+=1
    if unquote(dest.fragment) not in docs[t].ids:errors.append({'file':rel,'issue':'Missing fragment','url':u})
 for name in ('sitemap.xml','feed/index.html'):
  try:ET.parse(root/name)
  except Exception as e:errors.append({'file':name,'issue':'Invalid XML','detail':str(e)})
 for p in root.rglob('*'):
  if p.is_file() and p.suffix.lower() in ('.php','.sql','.gz','.bak'):errors.append({'file':str(p.relative_to(root)),'issue':'Unexpected backup/server file'})
 route_map=json.loads((root/'assets/legacy-urls.json').read_text())
 for pid,url in route_map.items():
  if not target(base+url).is_file():errors.append({'issue':'Legacy ID points to missing target','id':pid})
 search=json.loads((root/'assets/search.json').read_text())
 for item in search:
  if not target(base+item['url']).is_file():errors.append({'issue':'Search entry points to missing target','url':item['url']})
 report={'html_files':len(htmlfiles),'internal_references_checked':refs,'fragment_references_checked':fragments,'image_elements':sum(d.images for d in docs.values()),'legacy_id_routes':len(route_map),'search_entries':len(search),'external_urls_not_network_checked':sorted(external),'errors':errors,'status':'PASS' if not errors else 'FAIL','baseurl':base}
 return report
if __name__=='__main__':
 report=validate(sys.argv[1] if len(sys.argv)>1 else '_site',sys.argv[2] if len(sys.argv)>2 else '')
 print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(report['errors']))
