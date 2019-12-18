from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from utils.decorators import login_required
from flask_restful import current_app


class SearchResource(Resource):
    method_decorators = [login_required]

    def get(self):
        qs_parser = RequestParser()
        qs_parser.add_argument('q', type=inputs.regex(r'^.{1,50}$'), required=True,
                               location='args')  # 搜索关键词 限制输入1-50个字符
        qs_parser.add_argument('page', type=inputs.positive, required=False, location='args')  # 页号，限制整数自然数
        qs_parser.add_argument('per_page',  # 每页多少个
                               required=False,
                               location='args',
                               type=inputs.int_range(1, 20, 'per_page'))
        args = qs_parser.parse_args()
        q = args.q
        page = 1 if args.page is None else args.page

        # if args.page is None:
        #     page = 1
        # else:
        #     page= args.page

        per_page = 10 if args.per_page is None else args.per_page

        query = {
            'from': (page - 1) * per_page,  # 从第几条开始
            'size': per_page,  # 一共返回多少条
            '_source': ['title', 'article_id'],  # 指定要返回的字段
            'query': {
                'bool': {
                    'must': [
                        {'match': {'_all': q}}  # 全文检索
                    ],
                    'filter': [
                        {'term': {'status': 2}}  # 审核状态必须是2 过审
                    ]
                }
            }
        }
        es_ret = current_app.es.search(index='articles', doc_type='article', body=query)  # 返回dict
        results = [i['_source'] for i in es_ret['hits']['hits']]
        return {'page': page, 'per_page': per_page,
                'results': results, 'total_count': es_ret['hits']['total']}


class SuggestionResource(Resource):

    def get(self):
        parser = Resource()
        parser.add_argument('q', type=inputs.regex(r'^.{1,50}$'), required=True, location='args')
        args = parser.parse_grgs()
        q = args.q

        query = {
            'from': 0,
            'size': 10,
            '_source': False,
            'suggest': {
                'word-completion': {  # word-completion自定义返回字段
                    'prefix': q,
                    'completion': {
                        'field': 'suggest'
                    }
                }
            }
        }

        ret = current_app.es.search(index='completions',body=query)
        options_list = ret['suggest']['word-completion'][0]['options']

        if not options_list:
            query = {
                'from': 0,
                'size': 10,
                '_source': False,
                'suggest': {
                    'text': q,
                    'word-phrase': {
                        'phrase': {
                            'field': '_all',
                            'size': 1
                        }
                    }
                }
            }
            ret = current_app.es.search(index='articles',doc_type='article',body=query)
            options = ret['suggest']['word-phrase'][0]['options']
        results= []
        for option in options:
            if option['text'] not in results:
                results.append(option['text'])
        return {'options':results}

