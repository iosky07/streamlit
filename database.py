from deta import Deta

DETA_KEY = "a0pievcgefr_QhfpG9enmnt76kEbTmSCTuzbnRabJ3bZ"

# Load the environment variables
DETA_KEY = st.secrets["DETA_KEY"]

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("garuda_articles")

def fetch_all_articles():
    """Returns a dict of all articles"""
    res = db.fetch()
    return res.items


def get_article(article):
    """If not found, the function will return None"""
    return db.get(article)