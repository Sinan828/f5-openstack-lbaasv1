# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 New Dream Network, LLC (DreamHost)
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
# @author: Mark McClain, DreamHost

from neutron.openstack.common.rpc import proxy
from neutron.common import log


class LbaasAgentApi(proxy.RpcProxy):
    """Agent side of the Agent to Plugin RPC API."""

    API_VERSION = '1.0'

    def __init__(self, topic, context, host):
        super(LbaasAgentApi, self).__init__(topic, self.API_VERSION)
        self.context = context
        self.host = host

    @log.log
    def get_ready_services(self, tenant_ids=None):
        if tenant_ids:
            return self.call(
                self.context,
                self.make_msg('get_ready_services', tenant_ids=tenant_ids),
                topic=self.topic
            )
        else:
            return self.call(
                self.context,
                self.make_msg('get_ready_services'),
                topic=self.topic
            )

    @log.log
    def get_logical_service(self, pool_id):
        return self.call(
            self.context,
            self.make_msg(
                'get_logical_service',
                pool_id=pool_id,
                host=self.host
            ),
            topic=self.topic
        )

    @log.log
    def create_port(self, subnet_id=None,
                    mac_address=None, name=None,
                    fixed_address_count=1):
        return self.call(
                         self.context,
                         self.make_msg(
                                       'create_port',
                                       subnet_id=subnet_id,
                                       mac_address=mac_address,
                                       name=name,
                                       fixed_address_count=fixed_address_count,
                                       host=self.host
                                      ),
                         topic=self.topic
                )

    @log.log
    def delete_port(self, port_id=None, mac_address=None):
        return self.call(
                         self.context,
                         self.make_msg(
                                       'delete_port',
                                       port_id=port_id,
                                       mac_address=mac_address
                                      ),
                         topic=self.topic
                )

    @log.log
    def allocate_fixed_address(self, subnet_id=None,
                               port_id=None, name=None,
                               fixed_address_count=1):
        return self.call(
                         self.context,
                         self.make_msg(
                                       'allocate_fixed_address',
                                       subnet_id=subnet_id,
                                       port_id=port_id,
                                       name=name,
                                       fixed_address_count=fixed_address_count,
                                       host=self.host
                                      ),
                         topic=self.topic
                )

    @log.log
    def deallocate_fixed_address(self, fixed_addresses=None,
                             subnet_id=None, auto_delete_port=False):
        return self.call(
                         self.context,
                         self.make_msg(
                                       'deallocate_fixed_address',
                                       fixed_addresses=fixed_addresses,
                                       subnet_id=subnet_id,
                                       host=self.host,
                                       auto_delete_port=auto_delete_port
                                      ),
                         topic=self.topic
                )

    @log.log
    def update_vip_status(self, vip_id=None,
                           status=None, status_description=None):
        return self.call(
                         self.context,
                         self.make_msg(
                                       'update_vip_status',
                                       vip_id=vip_id,
                                       status=status,
                                       status_description=status_description,
                                       host=self.host
                                      ),
                         topic=self.topic
                )

    @log.log
    def vip_destroyed(self, vip_id=None):
        return self.call(
            self.context,
            self.make_msg('vip_destroyed', vip_id=vip_id, host=self.host),
            topic=self.topic
        )

    @log.log
    def update_pool_status(self, pool_id=None,
                           status=None, status_description=None):
        return self.call(
                         self.context,
                         self.make_msg(
                                       'update_pool_status',
                                       pool_id=pool_id,
                                       status=status,
                                       status_description=status_description,
                                       host=self.host
                                      ),
                         topic=self.topic
                )

    @log.log
    def pool_destroyed(self, pool_id):
        return self.call(
            self.context,
            self.make_msg('pool_destroyed', pool_id=pool_id, host=self.host),
            topic=self.topic
        )

    @log.log
    def update_member_status(self, member_id=None,
                           status=None, status_description=None):
        return self.call(
                         self.context,
                         self.make_msg(
                                       'update_vip_status',
                                       member_id=member_id,
                                       status=status,
                                       status_description=status_description,
                                       host=self.host
                                      ),
                         topic=self.topic
                )

    @log.log
    def member_destroyed(self, member_id):
        return self.call(
            self.context,
            self.make_msg('member_destroyed', member_id=member_id,
                          host=self.host),
            topic=self.topic
        )

    @log.log
    def update_health_monitor_status(self, health_monitor_id=None,
                           status=None, status_description=None):
        return self.call(
                         self.context,
                         self.make_msg(
                                       'update_health_monitor_status',
                                       health_monitor_id=health_monitor_id,
                                       status=status,
                                       status_description=status_description,
                                       host=self.host
                                      ),
                         topic=self.topic
                )

    @log.log
    def health_monitor_destroyed(self, health_monitor_id=None,
                                 pool_id=None):
        return self.call(
            self.context,
            self.make_msg('health_monitor_destroyed',
                          health_monitor_id=health_monitor_id, host=self.host),
            topic=self.topic
        )

    @log.log
    def update_pool_stats(self, pool_id, stats):
        return self.call(
            self.context,
            self.make_msg(
                'update_pool_stats',
                pool_id=pool_id,
                stats=stats,
                host=self.host
            ),
            topic=self.topic
        )
