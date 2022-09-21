from pathlib import Path
with open('usernames.txt','r') as f:
    usernames = f.readlines()
    for username in usernames:
        html_output = '<div class="ig-feed">'
        username=username.strip()
        for i in range(22):
            html_output+='<div class="ig-post">'
            for x in range(5):
                img_file = Path(f"{username}/{i}-{x}.jpg")
                if img_file.exists():
                    html_output+=f'<img src="{username}/{i}-{x}.jpg" />'
            html_output+='</div>'         
        html_output += '</div>'
        with open(f'{username}-feed.html','w+',encoding="utf-8") as t:
            t.write(html_output)
