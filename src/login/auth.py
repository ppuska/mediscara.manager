import logging
import os
from typing import Any, Optional

import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpRequest
from requests.auth import HTTPBasicAuth

logger = logging.getLogger("django")

User = get_user_model()


class KeyRockBackend(BaseBackend):
    """Custom backend model for managing authentication with the KeyRock IDM"""

    def authenticate(self, _: Optional[HttpRequest], **kwargs: Any) -> Optional[AbstractBaseUser]:
        """Method to authenticate the user based on either email-password (not working) or login token"""

        keyrock_url = os.getenv("KEYROCK_URL")

        if "email" in kwargs and "password" in kwargs:
            # email and password login method
            email = kwargs["email"]
            password = kwargs["password"]

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            }

            auth = HTTPBasicAuth(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))

            data = f"username={email}&password={password}&grant_type=password"

            url = f"{keyrock_url}/oauth2/token"

            response = requests.post(url=url, headers=headers, data=data, auth=auth)

            print(response.content.decode("utf-8"))

            return None

        if "token" in kwargs:
            # token login method
            token = kwargs["token"]

            response = requests.get(f"{keyrock_url}/user", params={"access_token": token}).json()

            assert isinstance(response, dict)

            try:
                username = response["username"]
                email = response["email"]
                display_name = response["displayName"]

            except KeyError:
                logger.warning("Got a KeyError while parsing user information")
                return None

            try:
                user = User.objects.get(username=username)

            except User.DoesNotExist:
                logger.info("User '%s' does not exist in db, creating user...", username)
                user = User(username=username)
                user.email = email
                user.first_name = display_name
                user.save()

            return user

        logger.warning("Email or password is missing from KeyRock authentication call")
        return None

    def get_user(self, user_id: int) -> Optional[AbstractBaseUser]:
        """Fetch the user based on their user id"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
