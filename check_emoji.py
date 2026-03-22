c = open('review.html','r',encoding='utf-8').read()
import re
matches = re.findall(r'title="(?:Female|Male|Neutral)">(.{1,4})', c)
for m in matches:
    print(repr(m))
