import requests
import keytime
from keytime import APP_ID, APP_SECRET, SHORT_LIVED_TOKEN, DEFAULT_MESSAGE
from loguru import logger
import json
from random import randint
from typing import List

_NORMAL = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
)
_BOLD = (
    "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
    "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"
)
_ITALIC = (
    "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡"
    "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻"
)

BOLD_MAP = dict(zip(_NORMAL, _BOLD))
ITALIC_MAP = dict(zip(_NORMAL, _ITALIC))

cirucci_posts = []
cirucci_dicts = []
images = []
videos = []
default_message = DEFAULT_MESSAGE


logger.add("facebook_automation.log", rotation="500 MB")


# Setup
def get_long_utoken() -> str | None:
    post_url = f'https://graph.facebook.com/v25.0/oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={SHORT_LIVED_TOKEN}'
    r = requests.get(post_url)
    data = r.json()
    if 'access_token' in data:
        print("[+] Data Recieved!")
        return data['access_token']
    else:
        print(f"[-] Error: {data}")
        return None


def get_long_ptoken(ltoken):
    post_url = f'https://graph.facebook.com/v25.0/me/accounts?access_token={ltoken}'
    r = requests.get(post_url)
    print(r.text)
    data = r.json()
    return data

# Parsing / Unicode trix


def text_bold(text: str) -> str:
    return "".join([BOLD_MAP.get(c, c) for c in text])


def text_italic(text: str) -> str:
    return "".join([ITALIC_MAP.get(c, c) for c in text])


def make_heading(text: str) -> str:
    return text_bold(text.strip().upper())


# Cirucci book quotes parsing / formatting
def get_json_posts(file: str = "cirucci_posts.json",
                   destination: List[dict] = cirucci_dicts):
    try:
        with open(file, "r", encoding="utf-8") as f:
            posts_data = json.load(f)
            for dict in posts_data:
                destination.append(dict)
    except FileNotFoundError:
        print(f"[-] Error: Could not find '{file}'.")
        return
    except json.JSONDecodeError as e:
        print(f"[-] {file} decode error: {e}")
        return


def format_cposts(site="Amazon", posts=cirucci_dicts, destination=cirucci_posts):
    for post in posts:
        destination.append((
            f"{make_heading(post['book_title'])}\n"
            f"{post['text']}\n\n"
            f"- {post['author']}, {text_italic(post['book_title'])}\n"
            f"Book availible on {site}:  {post['purchase_link']}"
        ))


def format_fposts(posts, destination):
    for post in posts:
        destination.append((
            f"{make_heading(post['title'])}\n"
            f"{post['text']}\n"
            f"- {post['link']}"
        ))

# Post Requests


def write_post(msg=default_message, link=None):
    post_url = f'https://graph.facebook.com/v25.0/{keytime.PAGE_ID}/feed'
    payload = {'message': msg,
               "link": link,
               'access_token': keytime.FB_ACCESS
               } if link else {'message': msg,
                               'access_token': keytime.FB_ACCESS
                               }
    r = requests.post(post_url, data=payload)
    if r.status_code == 200:
        logger.success(f"Successfully posted: {r.json().get('id')}")
    else:
        logger.error(f"Failed to post: {r.text}")
    print(r.text)


def send_picture(path, caption):
    image_url = f'https://graph.facebook.com/v25.0/{keytime.PAGE_ID}/photos'
    data = {'caption': caption,
            'access_token': keytime.FB_ACCESS,
            }
    with open(path, "rb") as f:
        files = {'source': f
                 }
        r = requests.post(image_url, files=files, data=data)
        if r.status_code == 200:
            logger.success(f"Successfully posted: {r.json().get('id')}")
        else:
            logger.error(f"Failed to post: {r.text}")
            print(r.text)


def send_video(path, description, title):
    video_url = f'https://graph-video.facebook.com/v25.0/{keytime.PAGE_ID}/videos'
    data = {'description': description,
            'access_token': keytime.FB_ACCESS,
            'title': title
            }
    with open(path, "rb") as f:
        files = {'source': f
                 }
        print(
            f"[*] Uploading video {path}... this might take a minute depending on file size.")
        r = requests.post(video_url, files=files, data=data)

        if r.status_code == 200:
            logger.success(
                f"Successfully posted video ID: {r.json().get('id')}")
        else:
            logger.error(f"Failed to post video: {r.text}")
            print(r.text)


# Customized Posting
def rando_cspawn(list=cirucci_posts):
    return randint(0, len(list) - 1)


def post_cirucci():
    index = rando_cspawn()
    write_post(cirucci_posts[index], cirucci_dicts[index]['purchase_link'])
    logger.info(
        f"Book: {cirucci_dicts[index]['book_title']} Passage: '{cirucci_dicts[index]['text'][0:20]}...'")


def print_quotes():
    for post in cirucci_dicts:
        print(f"{post['book_title']}:\n{post['text']}\n\n")


if __name__ == "__main__":
    n = 28
    get_json_posts()
    format_cposts()
    write_post(cirucci_posts[n],
               cirucci_dicts[n]['purchase_link'])
    # post_cirucci()
    # print(len(cirucci_posts))
