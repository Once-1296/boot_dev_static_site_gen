import re

def extract_markdown_images(text:str)->list[tuple[str,str]]:
    matches:list[str] = re.findall(r"\!\[.*?\]\(.*?\)",text)
    # print(matches)
    imgs = []
    for match in matches:
        parts = match.split('](')
        if len(parts) != 2:
            raise ValueError("Image link format is invalid")
        alt = parts[0][2:]
        url = parts[1][:-1]
        imgs.append((alt,url))
    return imgs

def extract_markdown_links(text:str)->list[tuple[str,str]]:
    matches:list[str] = re.findall(r"\[.*?\]\(.*?\)",text)
    links = []
    for match in matches:
        parts = match.split('](')
        if len(parts) != 2:
            raise ValueError("Anchor link format is invalid")
        alt = parts[0][1:]
        url = parts[1][:-1]
        links.append((alt,url))
    return links

# matches = extract_markdown_images(
#             "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
#         )
# print(matches)