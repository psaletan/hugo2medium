# hugo2medium: Publish a Hugo markdown blog post to Medium

This repository contains a python3 command-line application that converts
a single blog post written for the [Hugo](https://gohugo.io/) static site
builder into a Medium blog article.  The code uses the
[Medium SDK for Python](https://github.com/Medium/medium-sdk-python).

## Installation

Install the Medium SDK library and its dependencies:

    $ pip3 install -r requirements.txt

## Configuration

Rename or copy `medium_secrets.example.py` as `medium_secrets.py`.
Replace these values:

* `MEDIUM_TOKEN`: your Medium access token.  The
[Medium API docs](https://github.com/Medium/medium-api-docs#22-self-issued-access-tokens)
have instructions on how to generate a self-issued access token
that doesn't expire.  Use this method, not the browser-based authentication
method.

Edit `medium_config.py` with your preferred settings.  You'll definitely
want to change:

* `MEDIUM_USERNAME`: your Medium username.
* `DEFAULT_LOCAL_DIRECTORY`: where your Hugo markdown (.md) files are located.

The article will be published as a draft, unless you change the
`PUBLISH_STATUS` setting.

Edit the setting for `IGNORE_LINES_CONTAINING` to include any text
identifying lines you want skipped.  The default setting will skip lines
with `<img` or `"caption"` present, because the code doesn't provide a way
to upload images accompanying the markdown text.

If you elect to include an attribution line saying where the post was
originally published, change the settings for `ORIGINAL_DOMAIN_NAME`,
`ORIGINAL_DOMAIN_URL`, `ORIGINAL_DOMAIN_DIRECTORY`, and
`ATTRIBUTION_TEMPLATE`.

## Execution

    $ cd <DIRECTORY_WHERE_YOU_CLONED_THIS_REPO>
    $ ./mediumpub.py "<PATH_TO_YOUR_HUGO_MARKDOWN_FILE>"

## Limitations

Besides images, the application doesn't convert Categories or Tags.
