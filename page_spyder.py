import os
import argparse
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import trange
import pandas as pd


# from utilities import url_utilities, database_utilities, scrape
from utilities import scrape


# def main(database: str, url_list_file: str):


def main():
    # Extract the total number of pages to be scraped
    base_url = 'https://www.biorxiv.org/search/covid-19%252Btemperature'
    raw_html = scrape.simple_get(base_url)
    html = BeautifulSoup(raw_html, 'html.parser')

    page_count = int(html.select('li.pager-last > a')[0].text)
    print(page_count)

    # Scrape all the pages (takes about 2 seconds per page)
    preprints = []

    for i in trange(page_count):
        url = "https://www.biorxiv.org/search/covid-19%252Btemperature?page={}".format(i)

        raw_html = scrape.simple_get(url)
        html = BeautifulSoup(raw_html, 'html.parser')

        for div in html.find_all(name='div', attrs={'class': 'highwire-list-wrapper'}):
            pub_date_txt = div.find('h3').text
            # February 5, 2019 -> 20190205
            pub_date = datetime.strptime(pub_date_txt, '%B %d, %Y')

            for li in div.select('div > ul > li'):
                p_div = li.find('div', attrs={'class': 'highwire-article-citation'})
                p_attrs = p_div.attrs

                # some articles don't have type annotation
                p_type = p_div.select('div.highwire-cite-metadata > span.highwire-cite-metadata-overline')
                if len(p_type) < 1:
                    p_type_str = ''
                else:
                    p_type_str = p_type[0].text

                # really old articles have missing titles
                p_title = p_attrs.get('title', None)
                if p_title is None:
                    p_title = p_attrs.get('oldtitle', None)

                preprint = {'node_id': p_attrs['data-node-nid'],
                            'version_id': p_attrs['data-pisa'].split(';')[1],
                            'master_id': p_attrs['data-pisa-master'].split(';')[1],
                            'title': p_title,
                            'preprint_type': p_type_str,
                            'is_revision': not p_attrs['data-pisa'].endswith('v1'),
                            'pub_date': pub_date_txt,
                            'pub_date_year': pub_date.year,
                            'pub_date_month': pub_date.month,
                            'pub_date_day': pub_date.day}

                preprints.append(preprint)

    preprints_df = pd.DataFrame.from_dict(preprints)
    preprints_df.to_csv('preprints.csv')

    print('Total preprints scraped: {}'.format(len(preprints)))

    # From LinkedIn Learning Class
    # big_word_list = []
    # print("we are going to work with " + database)
    # print("we are going to scan " + url_list_file)
    # urls = url_utilities.load_urls_from_file(url_list_file)
    # for url in urls:
    #     print("reading " + url)
    #     page_content = url_utilities.load_page(url=url)
    #     words = url_utilities.scrape_page(page_contents=page_content)
    #     big_word_list.extend(words)
    #
    # # database code
    # os.chdir(os.path.dirname(__file__))
    # path = os.path.join(os.getcwd(), "words.db")
    # database_utilities.create_database(database_path=path)
    # database_utilities.save_words_to_database(database_path=path, words_list=big_word_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-db", "--database", help="SQLite File Name")
    parser.add_argument("-i", "--input", help="File containing urls to read")
    args = parser.parse_args()
    database_file = args.database
    input_file = args.input
    main()
    # main(database=database_file, url_list_file=input_file)
