#coding=utf-8
import sys
sys.path.insert(0, '.')

# from app import create_app
#
# create_app()

from models.content import Content

ARTICLE_KEY = 'nationalday:content:{id}'


# songs = [song.name for song in Song.objects.all()]
contents = [content.id for content in Content.objects.all()]
# artists = [artist.name for artist in Artist.objects.all()]

text_set = set()


# for content in Content.objects.all():
#     print 'cache search artist', content.id
    # search(content.id, 'artist')
#
