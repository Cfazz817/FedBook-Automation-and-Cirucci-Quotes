from facebook_graph import get_json_posts, format_fposts, write_post, rando_cspawn, logger

std_posts = []
std_dicts = []


def std_post():
    index = rando_cspawn(std_posts)
    write_post(std_posts[index], std_dicts[index]['link'])
    logger.info((
        f"Title: {std_dicts[index]['title']}\n\n"
        f"Passage: {std_dicts[index]['text'][0:20]}"))


if __name__ == "__main__":
    get_json_posts("stdPosts.json", std_dicts)
    format_fposts(std_dicts, std_posts)
    std_post()
    # write_post(std_posts[0],
    #            std_dicts[0]['link'])
