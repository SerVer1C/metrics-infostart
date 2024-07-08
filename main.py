import sys
import requests
from bs4 import BeautifulSoup as Bs


SERVER = r'https://infostart.ru'


def parse_is(html):
    articles = []

    soup = Bs(html, 'html.parser')
    blocks = soup.find_all('div', class_='well clearfix publication-item row')

    for block in blocks:
        art = {}
        link = block.find('a', class_='preloaded lazy-background', recursive=True)
        art['img_src'] = SERVER + link.attrs['data-src']
        data_block = block.find('div', class_='grid-width-fix col-sm-9 col-md-9', recursive=True)
        link = data_block.find('a', class_='font-md', recursive=True)
        art['title'] = link.text.strip()
        art['link'] = SERVER + link.attrs['href']
        link = data_block.find('span', class_='obj-rate-count-p', recursive=True)
        art['stars'] = int(link.text.strip())
        link = data_block.find('p', class_='public-preview-text-wrap', recursive=True)
        art['preview'] = link.text.strip()
        data_block2 = data_block.find('p', class_='text-muted desc-article', recursive=True)
        span = data_block2.find('i', class_='fa fa-calendar', recursive=True).parent
        art['date'] = span.text.strip()
        eye_block = data_block2.find('i', class_='fa fa-eye', recursive=True)
        art['views'] = int(eye_block.parent.text.strip()) if eye_block else 0
        dl_block = data_block2.find('i', class_='fa fa-download', recursive=True)
        art['downloads'] = int(dl_block.parent.text.strip()) if dl_block else 0
        comm_block = data_block2.find('i', class_='fa fa-comments', recursive=True)
        art['comments'] = int(comm_block.parent.text.strip()) if comm_block else 0
        articles.append(art)

    return articles


def main(args):
    user_id = args[1]
    count = int(args[2])
    template_file = args[3]
    readme_file = args[4]

    with open(template_file, 'r') as f:
        template = f.read()

    url = SERVER + r'/profile/' + str(user_id) + r'/objects/'
    response = requests.get(url)
    html = response.content.decode('cp1251')

    articles = parse_is(html)
    articles.sort(key=lambda x: x['stars'], reverse=True)

    res = ""

    for art in articles[:count]:
        res += template.format(
                    art['img_src'],
                    art['title'],
                    art['link'],
                    art['preview'],
                    art['stars'],
                    art['views'],
                    art['downloads'],
                    art['comments'],
                    art['date']
                )

    res += '<br><br>'
    res += (f'> | :point_right: | <h4 style="color: cyan"><u><a href="{url}">Полный профиль на Инфостарт</a></u></h4> |'
            f'> |-|-|')

    div_start = '<div id="is_start" />'
    div_end = '<div id="is_end" />'

    with open(readme_file, 'r', encoding='utf-8') as f:
        file = f.read()

    pos_start = file.find(div_start)
    pos_end = file.find(div_end)

    if pos_start != -1 and pos_end != -1:
        with open(readme_file, 'w', encoding='utf-8') as f:
            file = f'{file[:pos_start]}\n{res}\n{file[pos_end + len(div_end) + 1:]}'
            f.write(file)


if __name__ == '__main__':
    main(sys.argv)
