"""
Utility modules for FastAPI backend
"""

from .mongodb import connect_to_mongodb, close_mongodb_connection, get_database, get_collection
from .jwt_utils import create_token, verify_token, JWTManager
from .hash_utils import hash_password, compare_password, PasswordHasher
from .email_utils import send_to_email, EmailSender
from .response_utils import send_json, success_response, error_response, created_response, ResponseHelper
from .request_utils import handle_request, get_query_params, get_headers, get_cookies, RequestHandler
from .auth_utils import get_current_user, require_auth, require_role, require_roles, AuthManager

__all__ = [
    # MongoDB
    "connect_to_mongodb",
    "close_mongodb_connection", 
    "get_database",
    "get_collection",
    
    # JWT
    "create_token",
    "verify_token",
    "JWTManager",
    
    # Password hashing
    "hash_password",
    "compare_password",
    "PasswordHasher",
    
    # Email
    "send_to_email",
    "EmailSender",
    
    # Response helpers
    "send_json",
    "success_response",
    "error_response", 
    "created_response",
    "ResponseHelper",
    
    # Request helpers
    "handle_request",
    "get_query_params",
    "get_headers",
    "get_cookies",
    "RequestHandler",
    
    # Auth helpers
    "get_current_user",
    "require_auth",
    "require_role",
    "require_roles",
    "AuthManager",
]
