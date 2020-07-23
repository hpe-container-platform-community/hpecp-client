# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from __future__ import absolute_import

from .base_resource import AbstractResourceController, AbstractResource

from requests.structures import CaseInsensitiveDict

try:
    basestring
except NameError:
    basestring = str


class User(AbstractResource):
    """Create an instance of User from json data returned from the HPE
    Container Platform API. Users of this library are not expected to create an
    instance of this class.

    Parameters
    ----------
    json : str
        The json returned by the API representing a User.

    Returns
    -------
    User
        An instance of User
    """

    all_fields = [
        "id",
        "name",
        "description",
        "label",
        "is_group_added_user",
        "is_external",
        "is_service_account",
        "default_tenant",
        "is_siteadmin",
    ]
    # All of the fields of User objects as returned by the HPE Container
    # Platform API

    @property
    def id(self):
        """@Field: from json['_links']['self']['href'] -

        id format: '/api/v1/user/[0-9]+'
        """
        return self.json["_links"]["self"]["href"]

    @property
    def name(self):
        return self.json["label"]["name"]

    @property
    def description(self):
        return self.json["label"]["description"]

    @property
    def label(self):
        """@Field: from json['label']"""
        return self.json["label"]

    @property
    def is_group_added_user(self):
        """@Field: from json['is_group_added_user']"""
        return self.json["is_group_added_user"]

    @property
    def is_external(self):
        """@Field: from json['is_external']"""
        return self.json["is_external"]

    @property
    def is_service_account(self):
        """@Field: from json['is_service_account']"""
        return self.json["is_service_account"]

    @property
    def default_tenant(self):
        """@Field: from json['default_tenant']"""
        return self.json["default_tenant"]

    @property
    def is_siteadmin(self):
        """@Field: from json['is_siteadmin']"""
        return self.json["is_siteadmin"]

    @property
    def _links(self):
        """@Field: from json['_links']"""
        return self.json["_links"]


class UserController(AbstractResourceController):
    """Class that users will interact with to work with catalogs.

    An instance of this class is available in the
    client.ContainerPlatformClient with the attribute name
    :py:attr:`user <.client.ContainerPlatformClient.user>`.  The methods of
    this class can be invoked using `client.user.method()`.  See the example
    below:

    Example
    -------
    >>> client = ContainerPlatformClient(...).create_session()
    >>> client.user.list()
    """

    base_resource_path = "/api/v1/user/"
    resource_class = User
    resource_list_path = "users"

    def create(self, name, description="", is_external=True):
        """Create a user by specifying name and description.

        Parameters
        ----------
        name: str
            Client name.
        description: str
            Description as a string.
        is_external: bool
            Set to True for external users

        Returns
        -------
        str
            The user ID
        """

        assert isinstance(
            name, basestring
        ), "'name' must be provided and must be a string"
        assert isinstance(
            description, basestring
        ), "'description must be a string"
        assert isinstance(
            is_external, bool
        ), "'is_external' must be provided and must be a bool"

        data = {
            "label": {"name": name, "description": description},
            "is_external": is_external,
        }

        response = self.client._request(
            url="/api/v1/user",
            http_method="post",
            data=data,
            description="user/create",
        )
        return CaseInsensitiveDict(response.headers)["location"]
