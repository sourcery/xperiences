import pymongo

connection = pymongo.Connection()

class MongoMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        db = connection.test
        if hasattr(view_func, '__call__'):
            return view_func(db, request, **view_kwargs)
        else:
            return None
        
        
