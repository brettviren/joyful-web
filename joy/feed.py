# http://lkiesow.github.io/python-feedgen/
import os
from feedgen.feed import FeedGenerator

from joy.util import seconds2datetime

def atom(dat, **cfg):
    "Return XML text of an Atom feed file"
    fg = FeedGenerator()

    siteroot = cfg['siteroot']
    feed_base_id = cfg['feed_base_id']
    feed_path = cfg['feed_path']
    if feed_path.startswith('/'): # remove any
        feed_path = feed_path[1:] # leading slash
    feedurl = os.path.join(siteroot, feed_path)

    fg.id(feed_base_id + '/' + feed_path)
    fg.title(cfg['title'])
    fg.author(name = cfg['author'], email = cfg['email'])
    fg.link( href=cfg['siteroot'], rel='alternate')
    fg.link( href=feedurl, rel='self' )
    fg.language('en')

    logo = cfg.get('feed_logo_url',None)
    if logo:
        fg.logo(logo)

    subtitle = cfg.get('feed_subtitle',None) or cfg.get('subtitle',None)
    if subtitle:
        fg.subtitle(subtitle)

    content_type = cfg.get('feed_content_type', 'link')

    for org,meta in zip(dat['org'], dat['meta']):
        fe = fg.add_entry()
        fe.id(feed_base_id + '/' + org['path'])
        title = meta.get('title')
        if not title:
            raise RuntimeError,'Org file with no title "%s"' % (os.path.join(org['path'],org['name']))
        fe.title(title)

        description = meta.get('description',None)
        if description:
            fe.summary(description)
        
        category = meta.get('category',None)
        if category:
            fe.category(term=category)

        created = meta.get('timestamp',None)
        if created:
            #print 'CREATED TIMESTAMP:',created
            fe.pubdate(created)
        else:
            #print 'COMMITTED TIMESTAMP:',created
            created = meta['created']
            fe.pubdate(created.isoformat()+'-00:00')
        revised = meta['revised']
        fe.updated(revised.isoformat()+'-00:00')

        kwds = dict(cfg)
        kwds.update(org)
        kwds.update(meta)
        link = cfg['feed_content_link'].format(**kwds)
        fe.link(href= link, rel="alternate")

        if content_type == 'link':
            fe.content(src = link)
        if content_type in ['text','org']:
            fe.content(type = "text", content = org['text'])
        if content_type in ['plain','ascii']:
            fe.content(type = "text", content = org['plain'])
        if content_type in ['html','body']:
            fe.content(type = "html", content = org['body'])

    xml = fg.atom_str(pretty=True)

    return xml
