from pathlib import Path
from fastapi import UploadFile
from .interfaces.service import ImageServiceInterface
import aiofiles
from aiofiles import os as _os
import base64
from typing import Optional

class ImageService(ImageServiceInterface):

    def __init__(self, path: str) -> None:
        self._path = path

    async def read_image(self, imagename: str, as_base64: bool = False, **kwargs):
        try:
            async with aiofiles.open(f'{self._path}/{imagename}', mode='rb') as file:
                image = await file.read()
                if as_base64:
                    # Convert binary to base64
                    return base64.b64encode(image).decode('utf-8')
                return image
        except FileNotFoundError as error:
            raise FileNotFoundError(error)

    async def write_image(self, imagename: str, image: Union[UploadFile, str], is_base64: bool = False, **kwargs):
        async with aiofiles.open(f'{self._path}/{imagename}', mode='wb') as file:
            if is_base64:
                # Convert base64 string to binary
                content = base64.b64decode(image)
            else:
                content = await image.read()
            await file.write(content)

    async def delete_image(self, imagename: str, **kwargs):
        try:
            await _os.remove(f'{self._path}/{imagename}')
        except FileNotFoundError as error:
            raise FileNotFoundError(error)

    async def encode_to_base64(self, image_binary: bytes) -> str:
        """Helper method to convert binary to base64"""
        return base64.b64encode(image_binary).decode('utf-8')

    async def decode_from_base64(self, base64_string: str) -> bytes:
        """Helper method to convert base64 to binary"""
        return base64.b64decode(base64_string)

