from . import models

def RequestObjectMiddleware(get_response):
    """
    Middleware to process the request and add a 'request_object' attribute to the request.
    """

    def middleware(request):
        
        # Create a request object with the necessary attributes
        
        models.request_object = request
        
        response = get_response(request)
        

        return response

    return middleware