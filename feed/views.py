import json

from django.http.response   import JsonResponse
from django.views           import View

from .models                import Feed, Comment, ImageUrl
from user.models            import User
from product.models         import Product

class FeedView(View):    
    def get(self, request):
        MAXIMUM_COMMENT = 2
        feed_list   = []
        offset      = int(request.GET.get('offset'))
        limit       = int(request.GET.get('limit'))
    
        for feed in Feed.objects.all().order_by('-id'):
            feed_data = {
                'feed_basic_data' : {
                    'feed_id'         : feed.id, 
                    'feed_user'       : feed.user.nickname,
                    'created_at'      : feed.created_at,
                    'description'     : feed.description,
                    'like_number'     : feed.like_number,
                    'tag_item_number' : feed.tag_item_number,
                    'feed_main_image' : feed.imageurl_set.values('image_url').first()
                    },

                'product_data'   : {
                    'product_id'     : feed.product_id,
                    'product_name'   : feed.product.name,
                    'discount_rate'  : feed.product.discount_rate,
                    'price'          : feed.product.price,
                    'product_image'  : feed.product.productimageurl_set.get(is_main=1).image_url
                    } if feed.product_id else {
                    'product_id'     : '',
                    'product_name'   : '',
                    'discount_rate'  : '',
                    'price'          : '',
                    'product_image'  : ''
                    },

                'feed_comment_data'  : {
                    'feed_comment_count' : feed.comment_set.count(),
                    'comment_list'       : [{
                            'user'      : User.objects.get(id = comment.user_id).nickname,
                            'content'   : comment.content
                        } for comment in feed.comment_set.all().order_by('-created_at')[:MAXIMUM_COMMENT]
                        ] if feed.comment_set.exists() else
                        [{
                            'user':'',
                            'content':''
                        }]
                    }
                }

            feed_list.append(feed_data)
        feed_list = feed_list[offset:offset+limit]

        return JsonResponse({'feed_list': feed_list}, status=200)