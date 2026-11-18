import sys
from pptx import Presentation
for tag in ['보고용','확정판']:
    fn=f'발표스크립트_2025기준_{tag}.txt'
    head=open(fn).read().split('\n')[:2]
    p=Presentation(f'중간보고_마약류사회적비용_2025기준_{tag}.pptx')
    out=head+['']
    for i,s in enumerate(p.slides,1):
        t=''
        for sh in s.placeholders:
            if sh.placeholder_format.type is not None and 'TITLE' in str(sh.placeholder_format.type): t=sh.text_frame.text.replace('\n',' '); break
        nt=s.notes_slide.notes_text_frame.text if s.has_notes_slide else ''
        out+= [f'[{i}] {t}', nt, '']
    open(fn,'w').write('\n'.join(out).rstrip()+'\n'); print(fn,len(p.slides))
