# Import writer class from csv module
from csv import writer
import uuid
from icrawler import ImageDownloader, Crawler,Parser
from icrawler.builtin.google import GoogleImageCrawler, GoogleFeeder,GoogleParser
import argparse
import datetime
import json
from underthesea import pos_tag
    
def combine_text_with_pos(text):
    tagged_words = pos_tag(text)
    nouns = []
    adjectives = []
    verbs = []

    for word, pos in tagged_words:
        if pos.startswith('N'):  # Noun
            nouns.append(word)
        # elif pos.startswith('A'):  # Adjective
        #     adjectives.append(word)
        elif pos.startswith('V'):  # Verb
            verbs.append(word)

    combined_text = " ".join(nouns + adjectives + verbs)
    return combined_text

class AdvancedDownloader(ImageDownloader):
    def get_filename(self, task, default_ext):
        filename = super(AdvancedDownloader, self).get_filename(
            task, default_ext)
        return  filename

    def download(self, task, default_ext, timeout=5, max_retry=3, **kwargs):
        ImageDownloader.download(self, task, default_ext, timeout, max_retry, **kwargs)
        List = [kwargs['idx'],kwargs['keyword'],task['filename'],task['file_url']]
        if task['filename'] is None:
            pass
        else:
            # Open our existing CSV file in append mode
            # Create a file object for this file
            with open("data_withtext"+"/vlsp/train"+".csv", 'a',encoding='utf8') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(List)
                f_object.close()

class AdvancedImageCrawler(GoogleImageCrawler):
    def __init__(self, *args, **kwargs):
        Crawler.__init__(self,
            feeder_cls=GoogleFeeder,
            parser_cls=GoogleParser,
            downloader_cls=AdvancedDownloader,
            *args,
            **kwargs)

with open(r'/kaggle/working/a-ba-ner/documents/vlsp/train.txt','r',encoding='utf8') as f:
    lines = f.readlines()

# need image size > 224
filters = dict(size=">640x480")
for idx,item in enumerate(lines):
    google_crawler = AdvancedImageCrawler(storage={'root_dir': r'data\vlsp'},
                                        feeder_threads=1, parser_threads=1, downloader_threads=1)
    google_crawler.crawl(keyword=combine_text_with_pos(item).strip(),filters=filters, max_num=1,overwrite=True,file_idx_offset='auto',language='vi',idx=idx)

# truyền vào dữ liệu là text thuần ==> tạo file datawith_text ==> tạo thư mục chứa các ảnh
