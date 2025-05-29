from fastapi import Request, HTTPException
from typing import Dict, Any
import json


class RequestHandler:
    @staticmethod
    async def handle_request(request: Request) -> Dict[str, Any]:
        """Request body ni parse qilish"""
        try:
            # Content-Type tekshirish
            content_type = request.headers.get("content-type", "")

            if "application/json" in content_type:
                body = await request.body()
                if not body:
                    return {}

                try:
                    parsed_data = json.loads(body.decode('utf-8'))
                    return parsed_data
                except json.JSONDecodeError as e:
                    raise HTTPException(
                        status_code=400, detail="Noto'g'ri JSON format")

            elif "application/x-www-form-urlencoded" in content_type:
                form_data = await request.form()
                return dict(form_data)

            elif "multipart/form-data" in content_type:
                form_data = await request.form()
                return dict(form_data)

            else:
                # Raw body ni olish
                body = await request.body()
                if body:
                    try:
                        return json.loads(body.decode('utf-8'))
                    except:
                        return {"raw_body": body.decode('utf-8')}
                return {}

        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Request ni parse qilishda xatolik: {str(e)}")

    @staticmethod
    def get_query_params(request: Request) -> Dict[str, Any]:
        """Query parametrlarni olish"""
        return dict(request.query_params)

    @staticmethod
    def get_headers(request: Request) -> Dict[str, str]:
        """Headerlarni olish"""
        return dict(request.headers)

    @staticmethod
    def get_cookies(request: Request) -> Dict[str, str]:
        """Cookie larni olish"""
        return dict(request.cookies)

# Global request handler functions


async def handle_request(request: Request) -> Dict[str, Any]:
    return await RequestHandler.handle_request(request)


def get_query_params(request: Request) -> Dict[str, Any]:
    return RequestHandler.get_query_params(request)


def get_headers(request: Request) -> Dict[str, str]:
    return RequestHandler.get_headers(request)


def get_cookies(request: Request) -> Dict[str, str]:
    return RequestHandler.get_cookies(request)
