# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2012 Cisco Systems, Inc.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# @author: Sumit Naiksatam, Cisco Systems, Inc.

import logging as LOG

from neutron.plugins.cisco.common import cisco_constants as const
from neutron.plugins.cisco.common import cisco_exceptions as cexc
from neutron.plugins.cisco.common import config
from neutron.plugins.cisco.db import network_db_v2 as cdb

LOG.basicConfig(level=LOG.WARN)
LOG.getLogger(const.LOGGER_COMPONENT_NAME)


class Store(object):
    """Credential Store."""

    @staticmethod
    def initialize():
        dev_dict = config.get_device_dictionary()
        for key in dev_dict:
            dev_id, dev_ip, dev_key = key
            if dev_key == const.USERNAME:
                try:
                    cdb.add_credential(
                        dev_ip,
                        dev_dict[dev_id, dev_ip, const.USERNAME],
                        dev_dict[dev_id, dev_ip, const.PASSWORD],
                        dev_id)
                except cexc.CredentialAlreadyExists:
                    # We are quietly ignoring this, since it only happens
                    # if this class module is loaded more than once, in
                    # which case, the credentials are already populated
                    pass

    @staticmethod
    def put_credential(cred_name, username, password):
        """Set the username and password."""
        cdb.add_credential(cred_name, username, password)

    @staticmethod
    def get_username(cred_name):
        """Get the username."""
        credential = cdb.get_credential_name(cred_name)
        return credential[const.CREDENTIAL_USERNAME]

    @staticmethod
    def get_password(cred_name):
        """Get the password."""
        credential = cdb.get_credential_name(cred_name)
        return credential[const.CREDENTIAL_PASSWORD]

    @staticmethod
    def get_credential(cred_name):
        """Get the username and password."""
        cdb.get_credential_name(cred_name)
        return {const.USERNAME: const.CREDENTIAL_USERNAME,
                const.PASSWORD: const.CREDENTIAL_PASSWORD}

    @staticmethod
    def delete_credential(cred_name):
        """Delete a credential."""
        cdb.remove_credential(cred_name)
