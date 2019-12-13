from scrapy.spiders import Spider
from scrapy.selector import Selector
import json
from acfun.items import ArticleItem, CommentItem
from scrapy import Request
from datetime import datetime
import math

class AcfunSpider(Spider):
    name = "acfun"
    allowed_domains = ["acfun.cn"]
    start_urls = []
    max_pageNo = 50
    size = 200  # total items should be less than 10000
    api_game = "https://webapi.acfun.cn/query/article/list?pageNo={}&size={}&realmIds=8%2C11%2C43%2C44%2C45%2C46&originalOnly=false&orderType=2&periodType=-1&filterTitleImage=true"
    api_life = "https://webapi.acfun.cn/query/article/list?pageNo={}&size={}&realmIds=25%2C34%2C7%2C6%2C17%2C1%2C2&originalOnly=false&orderType=2&periodType=-1&filterTitleImage=true"
    api_synthesis = "https://webapi.acfun.cn/query/article/list?pageNo={}&size={}&realmIds=5%2C22%2C3%2C4&originalOnly=false&orderType=2&periodType=-1&filterTitleImage=true"
    article_url = "https://www.acfun.cn/a/ac{}"
    user_url = "https://www.acfun.cn/u/{}.aspx"
    for pageNo in range(1, max_pageNo + 1):
        start_urls.append(api_game.format(pageNo, size))
    for pageNo in range(1, max_pageNo + 1):
        start_urls.append(api_life.format(pageNo, size))
    for pageNo in range(1, max_pageNo + 1):
        start_urls.append(api_synthesis.format(pageNo, size))

    def parse(self, response):
        article_list = json.loads(response.body)['data']['articleList']
        article_url = "https://www.acfun.cn/a/ac{}"
        for article in article_list:
            arc_item = ArticleItem()
            arc_item['id'] = article['id']
            arc_item['like_count'] = article['like_count']
            arc_item['channel_id'] = article['channel_id']
            arc_item['channel_name'] = article['channel_name']
            arc_item['parent_channel_id'] = article['parent_channel_id']
            arc_item['parent_channel_name'] = article['parent_channel_name']
            arc_item['parent_realm_id'] = article['parent_realm_id']
            arc_item['realm_id'] = article['realm_id']
            arc_item['realm_name'] = article['realm_name']
            arc_item['title'] = article['title']
            arc_item['tag_id'] = article['tag_list'][0]['id']
            arc_item['tag_name'] = article['tag_list'][0]['name']
            arc_item['user_id'] = article['user_id']
            arc_item['user_name'] = article['username']
            arc_item['scraping_time'] = int(datetime.now().timestamp() * 1000)  # current timestamp
            arc_item['contribute_time'] = article['contribute_time']
            arc_item['view_count'] = article['view_count']
            arc_item['banana_count'] = article['banana_count']
            arc_item['favorite_count'] = article['favorite_count']
            article_request = Request(article_url.format(article['id']),
                                      callback=self.parse_content)
            article_request.meta['item'] = arc_item
            yield article_request

    def parse_content(self, response):
        arc_item = response.meta['item']
        if response.status == 404:
            arc_item['is_del'] = 1
            arc_item['content'] = None
            arc_item['comment_count'] = None
            yield arc_item
        else:
            arc_item['is_del'] = 0
            arc_info = json.loads(
                response.xpath('//script[re:test(text(),"window.articleInfo")]/text()').extract()[0][:-1].replace(
                    'window.articleInfo = ', ''))
            article_content = ''.join(Selector(text=arc_info['parts'][0]['content']).xpath('//text()').extract())
            comment_count = arc_info['commentCount']
            arc_item['content'] = article_content
            arc_item['comment_count'] = comment_count
            comment_item = CommentItem()
            comment_item['article_id'] = arc_info['articleId']
            yield arc_item
            comment_page_size = 50
            total_comment_page = math.ceil(comment_count / comment_page_size)
            for page in range(1, total_comment_page + 1):
                comment_url = "https://www.acfun.cn/rest/pc-direct/comment/listByFloor?sourceId={}&sourceType=3&page={}&pivotCommentId=0&newPivotCommentId=0"
                comment_request = Request(comment_url.format(arc_info['articleId'], page),
                                          callback=self.parse_comment)
                comment_request.meta['item'] = comment_item
                yield comment_request

    def parse_comment(self, response):
        comment_item = response.meta['item']
        comment_info = json.loads(response.body)
        for id in comment_info['commentIds']:
            comment_item['cid'] = comment_info['commentsMap']['c' + str(id)]['cid']
            comment_item['content'] = comment_info['commentsMap']['c' + str(id)]['content']
            comment_item['device_model'] = comment_info['commentsMap']['c' + str(id)]['deviceModel']
            comment_item['floor'] = comment_info['commentsMap']['c' + str(id)]['floor']
            comment_item['is_del'] = comment_info['commentsMap']['c' + str(id)]['isDelete']
            comment_item['is_up'] = comment_info['commentsMap']['c' + str(id)]['isUp']
            comment_item['is_up_del'] = comment_info['commentsMap']['c' + str(id)]['isUpDelete']
            comment_item['quote_id'] = comment_info['commentsMap']['c' + str(id)]['quoteId']
            comment_item['source_id'] = comment_info['commentsMap']['c' + str(id)]['sourceId']
            comment_item['post_date'] = comment_info['commentsMap']['c' + str(id)]['postDate']
            comment_item['timestamp'] = comment_info['commentsMap']['c' + str(id)]['timestamp']
            comment_item['user_id'] = comment_info['commentsMap']['c' + str(id)]['userId']
            comment_item['user_name'] = comment_info['commentsMap']['c' + str(id)]['userName']
            comment_item['scraping_time'] = int(datetime.now().timestamp() * 1000)  # current timestamp

            yield comment_item
