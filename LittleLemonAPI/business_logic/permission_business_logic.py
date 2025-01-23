from typing import List
from django.contrib.auth.models import User

class permission_business_logic:
        
        @classmethod
        def has_permission(cls, user: User, groups: List[str]) -> bool:
                return user.groups.filter(name__in=groups).exists()
        
        @classmethod
        def customer_permission(cls, user: User) -> bool:
                return user.is_authenticated and not user.groups.exists()
        
        @classmethod
        def authenticated_user_permission(cls, user: User) -> bool:
                return user.is_authenticated