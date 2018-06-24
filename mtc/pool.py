from . import config, errors, post
import urllib.parse
from requests import Session
import json

session = Session()


class Pool(object):
    data = ''

    def __init__(self, id=None, data=None):
        """Create a pool instance."""
        if data is not None:
            self.data = data
        else:
            contents = json.loads(session.get(f"{config.url}pool/show.json?&id={id}", headers=config.headers).text)
            if not contents.get('success', True):
                raise errors.E621Error(contents.get('reason'))
            self.data = contents

    def __repr__(self):
        # mostly debug, might stay, I dunno
        return str(self.data)

    @property
    def created_at(self):
        return self.data['created_at']['s']

    @property
    def description(self):
        return self.data['description']

    @property
    def id(self):
        return self.data['id']

    @property
    def is_active(self):
        return self.data['is_active']

    @property
    def is_locked(self):
        return self.data['is_locked']

    @property
    def name(self):
        return self.data['name']

    @property
    def post_count(self):
        return self.data['post_count']

    @property
    def user_id(self):
        return self.data['user_id']

    @property
    def creator_id(self):
        # Some people might think the "creator_id" in posts applies here and it doesn't, sadly
        return self.data['user_id']


def get_pool_by_id(id):
    """Get a pool by an ID number."""
    p = Pool(id)
    return p


def get_posts(id):
    """Get a list of posts in a pool."""
    posts = []
    contents = json.loads(session.get(f"{config.url}pool/show.json?&id={id}", headers=config.headers).text)
    if not contents.get('success', True):
        raise errors.E621Error(contents.get('reason'))
    for p in contents['posts']:
        posts.append(post.Post(p))
    return posts


def recent(title=None, page=None):
    """Gets recent posts, optionally with some tags."""
    pools = []
    query = f"{config.url}pool/index.json?"
    if title is not None:
        title = urllib.parse.quote(title.encode('utf-8'))
        query += f"&query={title}"
    if page is not None:
        query += f"&tags={page}"
    print(query)
    contents = json.loads(session.get(query, headers=config.headers).text)
    print(contents)
    try:
        if not contents.get('success', True):
            raise errors.E621Error(contents.get('reason'))
    except AttributeError:
        pass
    for p in contents:
        pools.append(Pool(None, p))
    return pools