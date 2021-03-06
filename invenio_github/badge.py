# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2014, 2015, 2016 CERN.
#
# Invenio is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Utility module to create badge."""

import requests
from flask import current_app
from six.moves.urllib import parse


def shieldsio_encode(text):
    """Encode text for shields.io."""
    return parse.quote_plus(text.replace('-', '--').replace('_', '__'))


def create_badge(subject, status, color, output_path, style=None):
    """Retrieve an SVG DOI badge from shields.io."""
    subject = shieldsio_encode(subject)
    status = shieldsio_encode(status)

    if style not in current_app.config["GITHUB_BADGE_STYLES"]:
        style = current_app.config["GITHUB_BADGE_DEFAULT_STYLE"]
    if color not in current_app.config["GITHUB_BADGE_COLORS"]:
        color = current_app.config["GITHUB_BADGE_DEFAULT_COLOR"]

    options = "?{}".format(parse.urlencode(dict(style=style)))

    url = '{url}{subject}-{status}-{color}.svg{style}'.format(
        url=current_app.config['GITHUB_SHIELDSIO_BASE_URL'],
        subject=subject,
        status=status,
        color=color,
        style=options,
    )

    response = requests.get(url)

    if response.status_code != 200:
        raise RuntimeError("Couldn't get image from shields.io", response)

    with open(output_path, 'wb') as f:
        f.write(response.content)
