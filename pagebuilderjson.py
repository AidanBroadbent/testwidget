import json
import wget
import shutil
import os
with open('data.json',encoding="utf-8") as f:
    data = json.load(f)
    for dat in data:
        username = dat['username']
        try:
            os.mkdir(username)
        except:
            shutil.rmtree(f'{username}')
            os.mkdir(username)
        html_output = '<div class="ig-feed">'
        videos = dat['latestPosts']
        videos += dat['latestIgtvVideos']
        for video in videos:
            short_code = video['shortCode']
            url = f"https://instagram.com/p/{short_code}"
            caption = video['caption']
            html_output+=f'<a href="{url}">'
            html_output+='<div class="ig-post">'
            try:
                file_type = "video"
                video_url = video['videoUrl']
                destination = f"{username}\\{short_code}.mp4"
                wget.download(video_url, destination)
                source = destination
            except:
                file_type = "image"
                image_url = video['displayUrl']
                destination = f"{username}\\{short_code}.jpg"
                wget.download(image_url, destination)
                source = destination
                try:
                    images = video['images']
                    i=0
                    for image in images:
                        wget.download(image, f"{username}\\{short_code}-{i}.jpg")
                        i+=1
                except:
                    pass
            if file_type == "image":
                html_output+=f'<img src="{source}" width="100%" height="100%"/>'
            else:
                html_output+=f'<video src="{source}" autoplay loop width="100%" height="100%"></video>'
            html_output+=f'<div class="ig-caption">{caption}</div>'
            html_output+='</div>'
            html_output+='</a>'
        html_output+='</div>'
        html_output+='''
        <style>
    * {
        margin: 0;
        padding: 0;
        font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    }
    .ig-feed {
            width: 100%;
            height: 100%;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            grid-template-rows: repeat(auto-fit, minmax(320px, 1fr));
            grid-gap: 0;
            overflow-x: hidden;
        }
        .ig-post {
        }
        a {
            text-decoration: none;
            color: white;
            overflow: hidden;
        }
        .ig-caption {
            opacity: 0;
            position: relative;
            text-align: center;
            margin: auto;
            margin-top: -100%;
            width: 90%;
            transition: 0.3s;
            color: white;
            word-break: break-all;
            text-decoration: none;
        }
        .ig-caption:visited {
            text-decoration: none;
            color: white;
        }
        .ig-post:hover img,.ig-post:hover video {
            width: 110%;
            height: 110%;
            filter: blur(3px);
        }
        .ig-post:hover .ig-caption {
            opacity: 1;
        }
        .ig-post img, .ig-post video {
            object-fit: none;
            transition: 0.3s;
        }</style>
        '''
        with open(f'{username}-appify-feed.html','w+',encoding="utf-8") as f:
            f.write(html_output)
