import unittest
import dnstools
from dnstools import exception


class DnsResolverTest(unittest.TestCase):

    def test_query_empty_domain_raises_EmptyHostError(self):
        domain = ''
        with self.assertRaises(dnstools.exception.EmptyHostError):
            dnstools.query_ipv4_from_host(domain)

    def test_query_invalid_domain_raises_HostError(self):
        domain = 'notarealdomain.somefaketld'
        with self.assertRaises(dnstools.exception.HostError):
            dnstools.query_ipv4_from_host(domain)

    def test_query_live_domain_returns_list_of_ip_addresses(self):
        domain = 'google.com'
        answer = dnstools.query_ipv4_from_host(domain)
        self.assertNotEqual(answer, [])

    def test_host_is_active_returns_true_with_active_domain(self):
        domain = 'google.com'
        self.assertTrue(dnstools.host_is_active(domain))

    def test_host_is_active_returns_false_with_inactive_domain(self):
        domain = 'notarealdomain.somefaketld'
        self.assertFalse(dnstools.host_is_active(domain))

    def test_ip_is_active_returns_true_with_live_ip(self):
        ip = '8.8.8.8'  # google DNS server
        self.assertTrue(dnstools.ip_is_active(ip))

    def test_ip_is_active_returns_false_with_fake_ip(self):
        ip = '203.0.113.0'  # invalid IP - RFC 5737
        self.assertFalse(dnstools.ip_is_active(ip))

    def test_reverse_ipv4_octets_returns_octets_in_reversed_order(self):
        address = '001.002.003.004'
        expected = '004.003.002.001'
        reversed_ip = dnstools.reverse_ipv4_octets(address)
        self.assertEqual(reversed_ip, expected)


if __name__ == '__main__':
    unittest.main()
