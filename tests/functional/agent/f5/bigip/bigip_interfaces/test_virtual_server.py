from tests.functional.agent.f5.bigip.bigip_base import BigIPTestBase
from netaddr import IPAddress

vlan = {'name': 'test-virtual-server-vlan',
        'id': 1001,
        'interface': 1.3}

virtual_server_http = {'folder': '/tenant1',
                       'name': 'test-virtual-server-http',
                       'protocol': 'HTTP',
                       'addr': '1.1.1.1',
                       'mask': '255.255.255.255',
                       'port': 80}

virtual_server_tcp = {'folder': '/tenant2',
                      'name': 'test-virtual-server-tcp',
                      'protocol': 'TCP',
                      'addr': '1.1.1.2',
                      'mask': '255.255.255.255',
                      'port': 22}

virtual_server_udp = {'folder': '/tenant3',
                      'name': 'test-virtual-server-udp',
                      'protocol': 'UDP',
                      'addr': '1.1.1.3',
                      'mask': '255.255.255.255',
                      'port': 53}

pool_http = {'pool_folder': '/Common',
             'name': 'test-pool-1',
             'lb_method': 'LEAST_CONNECTIONS'}


class TestBigIPInterfaceVirtualServer(BigIPTestBase):
    def setUp(self):
        super(TestBigIPInterfaceVirtualServer, self).setUp()

        self.bigip.vlan.create(vlan['name'], vlan['id'], vlan['interface'])

    def test_create_virtual_server_http(self):
        self._create_virtual_server_and_assert(virtual_server_http)

    def test_create_virtual_server_tcp(self):
        self._create_virtual_server_and_assert(virtual_server_tcp)

    def test_create_virtual_server_udp(self):
        self._create_virtual_server_and_assert(virtual_server_udp)

    def test_set_addr(self):
        new_address = str(IPAddress(virtual_server_http['addr']) + 1)

        self._create_virtual_server_and_assert(virtual_server_http)

        self.bigip.virtual_server.set_addr_port(
            name=virtual_server_http['name'], ip_address=new_address,
            port=virtual_server_http['port'],
            folder=virtual_server_http['folder'])

        self.assertEqual(new_address, self.bigip.virtual_server.get_addr(
            name=virtual_server_http['name'],
            folder=virtual_server_http['folder']))

    def test_get_addr(self):
        self._create_virtual_server_and_assert(virtual_server_http)

        self.assertEqual(virtual_server_http['addr'],
                         self.bigip.virtual_server.get_addr(
                             name=virtual_server_http['name'],
                             folder=virtual_server_http['folder']))

    def test_set_port(self):
        new_port = virtual_server_http['port'] + 1

        self._create_virtual_server_and_assert(virtual_server_http)

        self.bigip.virtual_server.set_addr_port(
            name=virtual_server_http['name'],
            ip_address=virtual_server_http['addr'], port=new_port,
            folder=virtual_server_http['folder'])

        self.assertEqual(new_port, self.bigip.virtual_server.get_port(
            name=virtual_server_http['name'],
            folder=virtual_server_http['folder']))

    def test_get_port(self):
        self._create_virtual_server_and_assert(virtual_server_http)

        self.assertEqual(virtual_server_http['port'],
                         self.bigip.virtual_server.get_port(
                             name=virtual_server_http['name'],
                             folder=virtual_server_http['folder']))

    def test_set_pool(self):
        self._create_virtual_server_and_assert(virtual_server_http)

        self.bigip.virtual_server.set_pool(name=virtual_server_http['name'],
                                           pool_name=pool_http['name'],
                                           folder=virtual_server_http[
                                               'folder'])

        self.assertEqual(pool_http['name'], self.bigip.virtual_server.get_pool(
            name=virtual_server_http['name'],
            virtual_server_folder=virtual_server_http['folder']))

    def test_get_pool(self):
        self._create_virtual_server_and_assert(virtual_server_http)

        self.bigip.virtual_server.set_pool(name=virtual_server_http['name'],
                                           pool_name=pool_http['name'],
                                           folder=virtual_server_http[
                                               'folder'])

        self.assertEqual(pool_http['name'], self.bigip.virtual_server.get_pool(
            name=virtual_server_http['name'],
            virtual_server_folder=virtual_server_http['folder']))

    def test_delete_virtual_server_http(self):
        self._create_virtual_server_and_assert(virtual_server_http)
        self._delete_virtual_server_and_assert(virtual_server_http)

    def test_delete_virtual_server_tcp(self):
        self._create_virtual_server_and_assert(virtual_server_tcp)
        self._delete_virtual_server_and_assert(virtual_server_tcp)

    def test_delete_virtual_server_udp(self):
        self._create_virtual_server_and_assert(virtual_server_udp)
        self._delete_virtual_server_and_assert(virtual_server_udp)

    def _create_virtual_server_and_assert(self, virtual_server):
        self.bigip.virtual_server.create(name=virtual_server['name'],
                                         ip_address=virtual_server['addr'],
                                         mask=virtual_server['mask'],
                                         port=virtual_server['port'],
                                         protocol=virtual_server['protocol'],
                                         vlan_name=vlan['name'],
                                         folder=virtual_server['folder'])

        # assertions
        self.assertTrue(
            self.bigip.virtual_server.exists(virtual_server['name'],
                                             folder=virtual_server['folder']))
        self.assertEqual(virtual_server['protocol'],
                         self.bigip.virtual_server.get_protocol(
                             virtual_server['name'],
                             folder=virtual_server['folder']))
        self.assertEqual(virtual_server['addr'],
                         self.bigip.virtual_server.get_addr(
                             virtual_server['name'],
                             folder=virtual_server['folder']))
        self.assertEqual(virtual_server['mask'],
                         self.bigip.virtual_server.get_mask(
                             virtual_server['name'],
                             folder=virtual_server['folder']))
        self.assertEqual(virtual_server['port'],
                         self.bigip.virtual_server.get_port(
                             virtual_server['name'],
                             folder=virtual_server['folder']))

    def _delete_virtual_server_and_assert(self, virtual_server):
        self.bigip.virtual_server.delete(name=virtual_server['name'],
                                         folder=virtual_server['folder'])

        self.assertFalse(
            self.bigip.virtual_server.exists(name=virtual_server['name'],
                                             folder=virtual_server['folder']))

    def _create_pool_and_assert(self, virtual_server):
        self.bigip.pool.create(name=virtual_server['name'],
                               folder=virtual_server['folder'])

        self.assertTrue(self.bigip.pool.exists(name=virtual_server['name'],
                                               folder=virtual_server[
                                                   'folder']))

    def _remove_all_test_artifacts(self):
        for virtual_server in [virtual_server_http, virtual_server_tcp,
                               virtual_server_udp]:

            self.bigip.virtual_server.delete(name=virtual_server['name'],
                                             folder=virtual_server['folder'])

    def tearDown(self):
        # remove all test artifacts
        self._remove_all_test_artifacts()

        # remove test VLAN
        self.bigip.vlan.delete(self.vlan_name)