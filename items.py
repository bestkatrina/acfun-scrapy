# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    like_count = scrapy.Field()
    channel_id = scrapy.Field()
    channel_name = scrapy.Field()
    parent_channel_id = scrapy.Field()
    parent_channel_name = scrapy.Field()
    parent_realm_id = scrapy.Field()
    realm_id = scrapy.Field()
    realm_name = scrapy.Field()
    title = scrapy.Field()
    tag_id = scrapy.Field()
    tag_name = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    content = scrapy.Field()
    scraping_time = scrapy.Field()
    contribute_time = scrapy.Field()
    view_count = scrapy.Field()
    banana_count = scrapy.Field()
    favorite_count = scrapy.Field()
    comment_count = scrapy.Field()
    is_del = scrapy.Field()


class CommentItem(scrapy.Item):
    cid = scrapy.Field()
    article_id = scrapy.Field()
    content = scrapy.Field()
    post_date = scrapy.Field()
    timestamp = scrapy.Field()
    device_model = scrapy.Field()
    floor = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    quote_id = scrapy.Field()
    source_id = scrapy.Field()
    scraping_time = scrapy.Field()
    is_del = scrapy.Field()
    is_up = scrapy.Field()
    is_up_del = scrapy.Field()
