c = open('review.html','r',encoding='utf-8').read()
c = c.replace(
    "pickAvatar(this,'neutral')\" style=\"width:56px;height:56px;border-radius:50%;border:2px solid #E0E0E0;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:28px;",
    "pickAvatar(this,'neutral')\" style=\"width:56px;height:56px;border-radius:50%;border:2px solid #E0E0E0;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:24px;"
)
open('review.html','w',encoding='utf-8').write(c)
print('Neutral avatar resized to 24px')
