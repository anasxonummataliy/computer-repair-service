from fastapi import Response
from typing import Any, Optional, Dict
import json


class ResponseHelper:
    @staticmethod
    def send_json(
        status_code: int,
        data: Dict[str, Any],
        token: Optional[str] = None,
        cookie_max_age: int = 30 * 24 * 60 * 60  # 30 kun
    ) -> Response:
        """JSON response yaratish"""

        # Token ni data dan olib tashlash
        response_data = data.copy()
        if 'token' in response_data:
            del response_data['token']

        content = json.dumps(response_data, ensure_ascii=False, default=str)
        response = Response(
            content=content,
            status_code=status_code,
            media_type="application/json"
        )

        # Token cookie sifatida qo'shish
        if token:
            response.set_cookie(
                key="token",
                value=token,
                max_age=cookie_max_age,
                httponly=True,
                secure=True,
                samesite="strict",
                path="/"
            )

        return response

    @staticmethod
    def success_response(
        message: str = "Muvaffaqiyatli",
        data: Optional[Dict[str, Any]] = None,
        token: Optional[str] = None
    ) -> Response:
        """Muvaffaqiyatli response"""
        response_data = {"message": message}
        if data:
            response_data.update(data)
        return ResponseHelper.send_json(200, response_data, token)

    @staticmethod
    def error_response(
        message: str = "Xatolik yuz berdi",
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None
    ) -> Response:
        """Xatolik response"""
        response_data = {"error": message}
        if details:
            response_data.update(details)
        return ResponseHelper.send_json(status_code, response_data)

    @staticmethod
    def created_response(
        message: str = "Yaratildi",
        data: Optional[Dict[str, Any]] = None,
        token: Optional[str] = None
    ) -> Response:
        """Yaratilgan response (201)"""
        response_data = {"message": message}
        if data:
            response_data.update(data)
        return ResponseHelper.send_json(201, response_data, token)

# Global response helper functions


def send_json(status_code: int, data: Dict[str, Any], token: Optional[str] = None) -> Response:
    return ResponseHelper.send_json(status_code, data, token)


def success_response(message: str = "Muvaffaqiyatli", data: Optional[Dict[str, Any]] = None, token: Optional[str] = None) -> Response:
    return ResponseHelper.success_response(message, data, token)


def error_response(message: str = "Xatolik yuz berdi", status_code: int = 400, details: Optional[Dict[str, Any]] = None) -> Response:
    return ResponseHelper.error_response(message, status_code, details)


def created_response(message: str = "Yaratildi", data: Optional[Dict[str, Any]] = None, token: Optional[str] = None) -> Response:
    return ResponseHelper.created_response(message, data, token)
