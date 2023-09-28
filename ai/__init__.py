# Copyright 2023 The AI Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Union, List

import os
import pathlib
import re
import base64

from bs4 import BeautifulSoup
from urllib.parse import urlparse

from .correlation import corrcoef

from .neighbors import KNeighborsClassifier
from .naive_bayes import GaussianNaiveBayes
from .linear_model import (LinearRegression, LogisticRegression)

_README = pathlib.Path(
  os.fspath(os.path.normpath(__file__))
).parent.parent / 'README.md'


def _ResizeImages(width: int = None, height: int = None) -> callable:
  def resizer(soup: BeautifulSoup) -> BeautifulSoup:
    for img in soup.find_all('img'):
      if width is not None:
        img['width'] = width
      if height is not None:
        img['height'] = height
    return soup

  return resizer


def _ConvertImagePath2Base64(soup: BeautifulSoup) -> BeautifulSoup:
  for img in soup.find_all('img'):
    src = img.get('src')

    if urlparse(src).scheme == '':
      with open(src, 'rb') as img_f:
        base64_img = base64.b64encode(img_f.read()).decode('utf-8')
    img['src'] = f'data:image/png;base64,{base64_img}'
  return soup


def _MarkdownPreprocessPipeline(
  soup: BeautifulSoup, pipeline: List[callable]
) -> BeautifulSoup:
  for call in pipeline:
    soup = call(soup)
  return soup


def _PreprocessReadme(fpath: Union[str, pathlib.Path]) -> str:
  with open(fpath, mode='r', encoding='utf-8') as f:
    readme = f.read()

  soup = BeautifulSoup(readme, 'html.parser')
  soup = _MarkdownPreprocessPipeline(
    soup, (_ConvertImagePath2Base64, _ResizeImages(width=600))
  )
  return str(soup)


__doc__ = _PreprocessReadme(_README)
