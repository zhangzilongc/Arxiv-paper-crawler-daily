#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib.parse
import urllib.request
import lxml
from bs4 import BeautifulSoup
import re
import ssl
import time
import os
"""
1. add comments

2. add daily
"""


class main_arxiv(object):

    def __init__(self, query_word: str, domain='cs.CV/', query_mode='all',
                 key_words=['self-supervised', 'transformer', 'contrastive learning', 'anomaly detection',
                           'novelty detection', 'representation learning', 'out-of-distribution']):
        """query_word: month_year, recent, pastweek"""
        self.original_url = 'https://arxiv.org/'
        self.domain_url = self.original_url + 'list/' + domain + query_word
        assert 'all' or 'daily' in query_mode, 'please input correct query mode(all, daily)'
        self.query_mode = query_mode
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
        }
        self.key_words = key_words
        self.root_dir = '/Users/zhangzilong/Desktop/arxiv/'
        current_time = time.strftime("%Y_%m_%d", time.localtime())
        self.current_time_dir = self.root_dir + current_time
        if not os.path.exists(self.current_time_dir):
            os.mkdir(self.current_time_dir)

    def get_url_context(self, target_url, pdf=False):
        context = ssl._create_unverified_context()
        request = urllib.request.Request(target_url, headers=self.headers)
        if not pdf:
            response = urllib.request.urlopen(request, context=context).read().decode()
        else:
            response = urllib.request.urlopen(request, context=context).read()
        return response

    def get_pdf(self, title_name_pdf, pdf_temp, element, UL=False):
        if UL:
            element = 'unsupervised learning'
        if not os.path.exists(os.path.join(self.current_time_dir, element)):
            os.mkdir(os.path.join(self.current_time_dir, element))
        sub_dir = os.path.join(self.current_time_dir, element)

        pdf_response = self.get_url_context(self.original_url + pdf_temp, pdf=True)

        with open(sub_dir + '/' + title_name_pdf, 'wb') as f:
            f.write(pdf_response)
        time.sleep(1)

    def run_get_pdf(self):
        response = self.get_url_context(self.domain_url)
        # get the target page range
        soup = BeautifulSoup(response, 'lxml')
        # all mode
        if self.query_mode == 'all':
            html_all_page = soup.find('div', id='dlpage').find('small').text
            pattern = re.compile(r'.*?total of (\d*) entries.*?', re.S)
            target_total_page = pattern.findall(html_all_page)
        # add daily mode
        elif self.query_mode == 'daily':
            html_all_page = soup.find('h3').text
            pattern = re.compile(r'.*? of (\d*) entries.*?', re.S)
            target_total_page = pattern.findall(html_all_page)

        query_string = {
            "show": target_total_page[0]
        }

        query_string_encode = urllib.parse.urlencode(query_string)

        url_immediate = self.domain_url + '?' + query_string_encode

        # get_final_url, get title and pdf
        target_response = self.get_url_context(url_immediate)
        soup = BeautifulSoup(target_response, 'lxml')
        total_context = soup.find('div', id='dlpage')

        list_title_dd = total_context.find_all('dd')
        list_pdf_dt = total_context.find_all('dt')
        pattern_title = re.compile(r'.Title: (.*).', re.S)

        ab_f = open(self.current_time_dir + '/' + 'summary.txt', 'w')
        start_val_paper = 0

        for i in range(len(list_pdf_dt)):
            query_state = False

            title_temp = list_title_dd[i].find('div', class_='list-title mathjax').text
            comments_temp = list_title_dd[i].find('div', class_='list-comments mathjax')
            if comments_temp:
                comments_temp_text = comments_temp.text.replace('\n', '')
            pdf_temp = list_pdf_dt[i].find('a', title='Download PDF')['href']

            title_name = pattern_title.findall(title_temp)[0]
            title_name = title_name.replace('/', ' ')
            title_name_pdf = title_name + '.pdf'
            for element in self.key_words:
                if element in title_name.lower():
                    query_state = True
                    self.get_pdf(title_name_pdf, pdf_temp, element)
                    break

            if not query_state:
                pattern_word_match = re.compile(r'(.*)unsupervised (.*?)learning(.*)', re.S)
                if pattern_word_match.findall(title_name.lower()):
                    query_state = True
                    self.get_pdf(title_name_pdf, pdf_temp, element='unsupervised learning', UL=True)

            if query_state:
                start_val_paper += 1
                print("Download {} papers!".format(str(start_val_paper)))
                Abstract_temp = list_pdf_dt[i].find('a', title='Abstract')['href']
                abstract_url = self.original_url + Abstract_temp[1:]
                abstract_response = self.get_url_context(abstract_url)
                soup = BeautifulSoup(abstract_response, 'lxml')
                abstract_text = soup.find('blockquote', class_='abstract mathjax').text.replace('\n', ' ')

                ab_f.write("[{}] ".format(str(i)) + title_name + '\n' * 2)
                if comments_temp:
                    ab_f.write(comments_temp_text + '\n')
                ab_f.write(abstract_text + '\n' * 2)
        ab_f.close()


if __name__ == "__main__":
    query_word = input("input your query range:")
    query_mode = input("input your query mode:")
    arxiv_download = main_arxiv(query_word=query_word, query_mode=query_mode)
    arxiv_download.run_get_pdf()
