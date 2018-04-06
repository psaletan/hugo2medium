"""medium_config.py
configuration for publishing a Hugo post to Medium
"""

# Medium settings
MEDIUM_USERNAME = "paul.saletan"
MEDIUM_PUBLISH_URL = "https://medium.com"
DEFAULT_TITLE = "My Title"
PUBLISH_STATUS = "draft"

# Hugo settings
# Where markdown files are located
DEFAULT_LOCAL_DIRECTORY = '/home/paul/site/hugo/tech/content/posts'

# For providing a link/attribution to the original Hugo post
INCLUDE_ATTRIBUTION = True
ORIGINAL_DOMAIN_NAME = "tech.surveypoint.com"
ORIGINAL_DOMAIN_URL = "https://tech.surveypoint.com"
ORIGINAL_DOMAIN_DIRECTORY = "posts"
ATTRIBUTION_TEMPLATE = "Originally published at [" + ORIGINAL_DOMAIN_NAME \
    + "](" + ORIGINAL_DOMAIN_URL + "/" + ORIGINAL_DOMAIN_DIRECTORY \
    + "/" + "$$POST_LINK$$/) on $$POST_DATE$$."
# Translation table: removes certain characters from Hugo tags
META_TRANS_TABLE = str.maketrans(dict.fromkeys(' "[]'))
IGNORE_LINES_CONTAINING = [ '<img ', '"caption"' ]

