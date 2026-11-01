import base64
F='/tmp/claude-0/jt/node_modules/'
faces=[('Anton',400,'normal',F+'@fontsource/anton/files/anton-latin-400-normal.woff2'),
('Montserrat','100 900','normal',F+'@fontsource-variable/montserrat/files/montserrat-latin-wght-normal.woff2'),
('Open Sans',400,'normal',F+'@fontsource/open-sans/files/open-sans-latin-400-normal.woff2'),
('Open Sans',600,'normal',F+'@fontsource/open-sans/files/open-sans-latin-600-normal.woff2'),
('Open Sans',700,'normal',F+'@fontsource/open-sans/files/open-sans-latin-700-normal.woff2'),
('IBM Plex Mono',400,'normal',F+'@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff2'),
('IBM Plex Mono',500,'normal',F+'@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2')]
css=''.join(f"@font-face{{font-family:'{n}';font-weight:{w};font-style:{st};font-display:block;src:url(data:font/woff2;base64,{base64.b64encode(open(f,'rb').read()).decode()}) format('woff2')}}\n" for n,w,st,f in faces)
s=open('/home/claude/teaser/teaser-src.html').read().replace('/*FONTS*/',css,1)
open('/home/claude/teaser/plumia-teaser.html','w').write(s); print(len(s))
