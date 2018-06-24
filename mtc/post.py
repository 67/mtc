from . import config, errors
import urllib.parse
import random
from requests import Session
import json

session = Session()


class Post(object):
    data = ''

    def __init__(self, data=None, id=None):
        """Create a post instance."""
        if id is not None:
            contents = json.loads(session.get(f"{config.url}post/show.json?&id={id}", headers=config.headers).text)
            self.data = contents
            if not contents.get('success', True):
                raise errors.E621Error(contents.get('reason'))
        if data is not None:
            self.data = data

    def __repr__(self):
        # idk, this is mostly for debugging right now
        return str(self.data)

    @property
    def id(self):
        return self.data['id']

    @property
    def author(self):
        return self.data['author']

    @property
    def creator_id(self):
        return self.data['creator_id']

    @property
    def created_at(self):
        return self.data['created_at']['s']

    @property
    def status(self):
        return self.data['status']

    @property
    def source(self):
        return self.data['source']

    @property
    def sources(self):
        if 'sources' in self.data:
            return self.data['sources']
        else:
            return None

    @property
    def tags(self):
        return self.data['tags']

    @property
    def artist(self):
        return self.data['artist']

    @property
    def description(self):
        return self.data['description']

    @property
    def fav_count(self):
        return self.data['fav_count']

    @property
    def score(self):
        return self.data['status']

    @property
    def rating(self):
        return self.data['rating']

    @property
    def parent_id(self):
        return self.data['parent_id']

    @property
    def has_children(self):
        return self.data['has_children']

    @property
    def children(self):
        return self.data['children']

    @property
    def has_notes(self):
        return self.data['has_notes']

    @property
    def has_comments(self):
        return self.data['has_comments']

    @property
    def md5(self):
        return self.data['md5']

    @property
    def file_url(self):
        return self.data['file_url']

    @property
    def file_ext(self):
        return self.data['file_ext']

    @property
    def file_size(self):
        return self.data['file_size']

    @property
    def width(self):
        return self.data['width']

    @property
    def height(self):
        return self.data['height']

    @property
    def sample_url(self):
        return self.data['sample_url']

    @property
    def sample_width(self):
        return self.data['sample_width']

    @property
    def sample_height(self):
        return self.data['sample_height']

    @property
    def preview_url(self):
        return self.data['preview_url']

    @property
    def preview_width(self):
        return self.data['preview_width']

    @property
    def preview_height(self):
        return self.data['preview_height']

    @property
    def delreason(self):
        if 'delreason' in self.data:
            return self.data['delreason']
        else:
            return None

    @property
    def locked_tags(self):
        # As far as I can tell, this is never ever used
        return self.data['locked_tags']


def search(tags, limit=75):
    """Gets posts from a certain set of tags."""
    posts = []
    tags = urllib.parse.quote(tags.encode('utf-8'))
    query = f"{config.url}post/index.json?&tags={tags}&limit={limit}"
    contents = json.loads(session.get(query, headers=config.headers).text)
    try:
        if not contents.get('success', True):
            raise errors.E621Error(contents.get('reason'))
    except AttributeError:
        pass
    for p in contents:
        posts.append(Post(p))
    return posts


def random_from_tags(tags):
    """Return a random image from tags."""
    return random.choice(search(tags))


def get_post_by_id(id):
    """Get a post by an ID number."""
    p = Post(None, id)
    return p


def recent(tags=None, limit=100):
    """Gets recent posts, optionally with some tags."""
    posts = []
    query = f"{config.url}post/index.json?&limit={limit}"
    if tags is not None:
        tags = urllib.parse.quote(tags.encode('utf-8'))
        query += f"&tags={tags}"
    contents = json.loads(session.get(query, headers=config.headers).text)
    try:
        if not contents.get('success', True):
            raise errors.E621Error(contents.get('reason'))
    except AttributeError:
        pass
    for p in contents:
        posts.append(Post(p))
    return posts