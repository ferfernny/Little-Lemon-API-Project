from rest_framework.response import Response
from rest_framework import status

class http_status_code_business_logic:
    
    @classmethod
    def status_200_ok(cls, message: str) -> Response:
        return Response(
            {"Message":message}, 
            status=status.HTTP_200_OK
            )
    
    @classmethod
    def status_201_created(cls, message: str) -> Response:
        return Response(
            {"Message":message}, 
            status=status.HTTP_201_CREATED
            )
    
    @classmethod
    def status_204_no_content(cls, message: str) -> Response:
        return Response(
            {"Message":message}, 
            status=status.HTTP_204_NO_CONTENT
            )
        
    @classmethod
    def status_401_unauthorized(cls, message: str) -> Response:
        return Response(
            {"Message":message}, 
            status=status.HTTP_401_UNAUTHORIZED
            )
        
    @classmethod
    def status_400_bad_request(cls, message: str) -> Response:
        return Response(
            {"Message":message}, 
            status=status.HTTP_400_BAD_REQUEST
            )
        
    @classmethod
    def status_403_forbidden(cls, message: str) -> Response:
        return Response(
            {"Message":message}, 
            status=status.HTTP_403_FORBIDDEN
            )
        
    @classmethod
    def status_404_not_found(cls, message: str) -> Response:
        return Response(
            {"Message":message}, 
            status=status.HTTP_404_NOT_FOUND
            )
        
    