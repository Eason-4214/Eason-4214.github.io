#!/usr/bin/env python3
"""Render a dependency-free, crawlable academic homepage from profile.json."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
import json
from hashlib import sha256
import struct

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://eason-4214.github.io/'
p = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))

def e(value):
    return escape(str(value), quote=True)

def link(text, url, cls=''):
    assert urlsplit(url).scheme in ('', 'http', 'https', 'mailto'), url
    return f'<a href="{e(url)}"' + (f' class="{e(cls)}"' if cls else '') + f'>{e(text)}</a>'

def section(id, title, body, extra=''):
    return f'<section id="{id}" class="section" aria-labelledby="{id}-heading"><div class="section-heading"><h2 id="{id}-heading">{title}</h2>{extra}</div>{body}</section>'

profile = f'<img class="portrait" src="{e(p["portrait"])}" alt="{e(p["name"])}" width="190" height="244" fetchpriority="high">'
profile += f'<h1 class="name">{e(p["name"])}</h1><p class="native-name">{e(p["nativeName"])}</p><p class="role">{e(p["role"])}</p>'
profile += link(p['affiliation'], p['affiliationUrl'], 'affiliation')
profile += '<hr class="profile-rule"><div class="profile-links">' + link('Email', 'mailto:' + p['email'])
profile += ''.join(link(item['label'], item['url']) for item in p['links']) + '</div>'
profile += f'<p class="location">{e(p["location"])}</p>'

about = '<div class="intro">' + ''.join(f'<p>{e(x)}</p>' for x in p['about']) + '</div>'
about += '<div class="research-list" aria-label="Research interests">' + ''.join(f'<span class="research-tag">{e(x)}</span>' for x in p['interests']) + '</div>'
content = section('about', 'About', about)

news = '<ul class="news-list">'
for item in sorted(p.get('news', []), key=lambda x:x['date'], reverse=True):
    year, month = item['date'].split('-')
    news += f'<li><time class="news-date" datetime="{e(item["date"])}">[{month}/{year}]</time> {e(item["text"])}'
    if item.get('linkText'):
        news += link(item['linkText'], item['url'])
    news += e(item.get('suffix', '')) + '</li>'
news += '</ul>'
if p.get('news'):
    content += section('news', 'News', news)

papers = ''
for paper in p['publications']:
    figure = ''
    if paper.get('image'):
        src = e(paper['image'])
        alt = e(paper['imageAlt'])
        image_path = ROOT / urlsplit(paper['image']).path
        image_width, image_height = struct.unpack('>II', image_path.read_bytes()[16:24])
        figure = f'<a class="paper-figure" href="{src}" target="_blank" rel="noopener" title="Open full-size figure" aria-label="Open full-size figure: {alt} (new tab)"><img src="{src}" alt="{alt}" loading="lazy" decoding="async" width="{image_width}" height="{image_height}"><span class="figure-label">{e(paper["imageLabel"])}</span></a>'
    body = f'<div class="paper-top"><span class="venue">{e(paper["venue"])}</span><span class="year">{e(paper["year"])}</span></div>'
    body += '<h3 class="paper-title">' + link(paper['title'], paper['url']) + '</h3>'
    authors = ', '.join(f'<strong>{e(a)}</strong>' if a == p['name'] else e(a) for a in paper['authors'])
    body += f'<p class="authors">{authors}</p><p class="publication">{e(paper["publication"])}</p>'
    body += '<div class="paper-links">' + ''.join(link(x['label'], x['url']) for x in paper.get('links', [])) + '</div>'
    papers += '<article class="paper' + (' has-figure' if figure else '') + '">' + figure + '<div class="paper-content">' + body + '</div></article>'
scholar = next(x['url'] for x in p['links'] if x['label'] == 'Google Scholar')
content += section('publications', 'Selected publications', papers, link('All publications ↗', scholar, 'aside-link'))

education = ''.join(f'<div class="entry"><span class="year">{e(x["period"])}</span><div><h3>{e(x["institution"])}</h3><p>{e(x["degree"])}</p></div></div>' for x in p['education'])
content += section('education', 'Education', education)
content += section('contact', 'Contact', f'<p class="contact-copy">{e(p["affiliation"])}</p>' + link(p['email'], 'mailto:' + p['email'], 'contact-email'))

person = {
    '@type':'Person', '@id':BASE+'#person', 'name':p['name'], 'givenName':'Yiteng', 'familyName':'Sun',
    'alternateName':['Eason Sun', 'Eason'], 'url':BASE, 'image':BASE+'assets/yiteng-sun.jpg',
    'jobTitle':p['role'], 'affiliation':{'@type':'CollegeOrUniversity','name':p['affiliation'],'url':p['affiliationUrl']},
    'alumniOf':[{'@type':'CollegeOrUniversity','name':x['institution']} for x in p['education'][1:]],
    'knowsAbout':p['interests'], 'sameAs':[x['url'] for x in p['links']]+['https://github.com/Eason-4214']
}
schema = {'@context':'https://schema.org','@type':'ProfilePage','@id':BASE+'#profile','url':BASE,'name':'Yiteng Sun — Academic Homepage','mainEntity':person}
schema_json = json.dumps(schema,ensure_ascii=False,indent=2).replace('<','\\u003c')
title = 'Yiteng Sun (Eason) | Human–Computer Interaction | PolyU'
description = 'Yiteng Sun (Eason), Ph.D. student at The Hong Kong Polytechnic University. Research in human–computer interaction, human factors, and autonomous driving.'
verification = p.get('googleSiteVerification','')
verification_meta = f'<meta name="google-site-verification" content="{e(verification)}">' if verification else ''
style_version = sha256((ROOT / 'style.css').read_bytes()).hexdigest()[:10]
cv_link = f'<a href="{e(p["cv"])}" target="_blank" rel="noopener" aria-label="CV (PDF, opens in a new tab)">CV</a>' if p.get('cv') else ''
html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <meta name="author" content="Yiteng Sun">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <link rel="canonical" href="{BASE}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:type" content="profile">
  <meta property="og:url" content="{BASE}">
  <meta property="profile:first_name" content="Yiteng">
  <meta property="profile:last_name" content="Sun">
  {verification_meta}
  <link rel="icon" type="image/svg+xml" href="./favicon.svg">
  <link rel="stylesheet" href="./style.css?v={style_version}">
  <script type="application/ld+json">{schema_json}</script>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <div class="shell">
    <header class="topbar">
      <a class="wordmark" href="./" aria-label="Home"><span class="mark" aria-hidden="true">Y</span><span>Yiteng Sun</span></a>
      <nav aria-label="Main navigation"><a href="#about">About</a><a href="#news">News</a><a href="#publications">Publications</a><a href="#contact">Contact</a>{cv_link}</nav>
    </header>
    <div class="layout">
      <aside class="profile" aria-label="Profile">{profile}</aside>
      <main id="main" tabindex="-1">{content}</main>
    </div>
    <footer class="footer"><span>© 2026 Yiteng Sun</span><a href="#">Back to top ↑</a></footer>
  </div>
</body>
</html>
'''
(ROOT/'index.html').write_text(html,encoding='utf-8')
(ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n',encoding='utf-8')
(ROOT/'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{BASE}</loc></url></urlset>\n',encoding='utf-8')
(ROOT/'.nojekyll').touch()
print('Built static HTML, Person/ProfilePage metadata, robots.txt, and sitemap.xml.')
