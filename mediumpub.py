#!/usr/bin/env python3
"""mediumpub.py
Publish Hugo markdown blog post file as a Medium.com article.
Uses Markdown SDK for Python
"""

# Python libraries
from datetime import date
import argparse

# Third party libraries
from medium import Client

# Project custom modules
import medium_config as config
import medium_secrets as secrets

def arg_parser():
    """Parses command line arguments and provides --help"""
    parser = argparse.ArgumentParser(description="Creates medium.com draft post from Hugo markdwon file")
    parser.add_argument("markdown_file")
    args = parser.parse_args()
    return args

class HugoPost(object):
    """Single article"""

    def __init__(self):
        self.meta = {}
        self.original_lines = []
        self.final_lines = []
        self.content = ''
        self.include_attribution = config.INCLUDE_ATTRIBUTION
        self.attribution_text = ''
        self.post = None

    def push_to_medium(self):
        """Prepare final content, upload post to Medium"""
        self.title = self.meta.get('title', config.DEFAULT_TITLE)
        if self.include_attribution:
            self.add_attribution()
        self.content = ''.join(self.final_lines)
        client = Client(access_token=secrets.MEDIUM_TOKEN)
        me = client.get_current_user()
        self.post = client.create_post(user_id=me['id'], title=self.title, \
            content=self.content, content_format="markdown", \
            publish_status=config.PUBLISH_STATUS)
        print(self.post)

    def read_markdown_file(self, filename):
        """Read markdown file from disk and return a list of its lines."""
        with open(filename, 'r') as myfile:
            lines=myfile.readlines()
        self.original_lines = lines

    def parse_meta_line(self, line):
        """Read a line containing a Hugo meta tag and update the corresponding meta dictionary elements."""
        meta_tag = line.split('=')
        tag_name = meta_tag[0].strip()
        tag_value = meta_tag[1].strip()
        if tag_name == 'title':
            self.meta['title'] = tag_value.strip().replace('"', '')
            self.meta['title_url_text'] = self.meta['title'].lower().replace(' ','-')
        elif tag_name == 'date':
            self.meta['pubdate_long'] = tag_value.strip().replace('"', '')
            dstr = self.meta['pubdate_long'][:10]
            pub_date = date(int(dstr[0:4]), int(dstr[5:7]), int(dstr[8:10]))
            self.meta['pubdate_text'] = pub_date.strftime("%B %d, %Y")
        elif tag_name == 'draft':
            self.meta['draft'] = tag_value.strip().replace('"', '')
        elif tag_name == 'image':
            self.meta['image'] = tag_value.strip().replace('"', '')
        elif tag_name == 'categories':
            self.meta['categories_list'] = tag_value.strip()
            self.meta['categories'] = self.meta['categories_list'].translate(config.META_TRANS_TABLE).split(',')
        elif tag_name == 'tags':
            self.meta['tags_list'] = tag_value.strip()
            self.meta['tags'] = self.meta['tags_list'].translate(config.META_TRANS_TABLE).split(',')

    def parse_lines(self):
        """
        Read markdown file, one line at a time.
        Parse tags, exclude certain lines from body text.
        """
        found_first_content_line = False
        found_metadata_begin = False
        found_metadata_end = False
        found_code_begin = False
        found_code_end = False
        blank_count = 0
        for line in self.original_lines:
            # Check if we're within the meta block bounded by +++ delimiters
            is_meta_line = False
            is_meta_delimiter = False
            if line[:3] == '+++':
                is_meta_line = True
                is_meta_delimiter = True
                if not found_metadata_begin:
                    found_metadata_begin = True
                else:
                    found_metadata_end = True
            if (found_metadata_begin) and (not found_metadata_end) and not is_meta_delimiter:
                line = line.strip()
                # Parse meta lines individually, adding them to the meta dictionary
                if line.find('=') >= 0:
                    is_meta_line = True
                    self.parse_meta_line(line)
            append = True
            # Don't append meta tag lines to body text
            if is_meta_line:
                append = False
            else:
                # Skip any blank lines before beginning of real content
                current_line_blank = True if len(line.strip()) == 0 else False
                if not current_line_blank:
                    blank_count = 0
                else:
                    blank_count += 1
                if not found_first_content_line:
                    if not current_line_blank:
                        found_first_content_line = True
                    else:
                        append = False
            # Ignore more than two consecutive line feeds unless they're
            # within a code block. For code blocks, repeat verbatim, don't skip
            # any extra blank lines.
            if append:
                is_code_line = False
                if line[0:3] == '```':
                    if found_code_begin == True:
                        found_code_end = True
                    else:
                        found_code_begin = True
                if (found_code_begin) and (not found_code_end):
                    is_code_line = True
                elif not current_line_blank and line[0] != ' ':
                    is_code_line = False
                if len(line) >= 2 and (line[0:2] == '  ' or line[0] == '\t'):
                    is_code_line = True
                if current_line_blank and blank_count > 2 and not is_code_line:
                    append = False
                # Ignore lines containing text defined in config.IGNORE_LINES_CONTAINING
                for substr in config.IGNORE_LINES_CONTAINING:
                    if line.find(substr) >= 0:
                        append = False
                # TO DO: Replace image classes with figure and figcaption.
                # See: https://blog.medium.com/accepted-markup-for-medium-s-publishing-api-a4367010924e
            if append:
                self.final_lines.append(line)
        #return meta, final_lines                

    def add_attribution(self):
        self.attribution_text = config.ATTRIBUTION_TEMPLATE.replace(
            '$$POST_DATE$$', self.meta['pubdate_text'])
        self.attribution_text = '*' + self.attribution_text.replace(
            '$$POST_LINK$$', self.meta['title_url_text']) + '*'
        self.final_lines.append('\n' + self.attribution_text)

def main():
    """Main program loop."""

    args = arg_parser()
    markdown_file = config.DEFAULT_LOCAL_DIRECTORY + '/' + args.markdown_file

    post = HugoPost()
    post.read_markdown_file(markdown_file)
    post.parse_lines()
    post.push_to_medium()

if __name__ == "__main__":
    main()
