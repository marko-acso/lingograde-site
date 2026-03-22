c = open('review.html','r',encoding='utf-8').read()
c = c.replace("font-size:24px;\" title=\"Neutral", "font-size:20px;\" title=\"Neutral")
open('review.html','w',encoding='utf-8').write(c)
print('Neutral avatar resized to 20px')
