import unittest
from dnstools.resolver import DnsResolver


class DnsResolverTest(unittest.TestCase):

    def setUp(self) -> None:
        self.resolver = DnsResolver()

    def test_query_empty_domain_returns_empty_list(self):
        domain = ''
        answer = self.resolver.query_ipv4_from_domain(domain)
        self.assertListEqual(answer, [])

    def test_query_invalid_domain_returns_empty_list(self):
        domain = 'notarealdomain.somefaketld'
        answer = self.resolver.query_ipv4_from_domain(domain)
        self.assertListEqual(answer, [])

    def test_query_live_domain_returns_list_of_ip_addresses(self):
        domain = 'google.com'
        answer = self.resolver.query_ipv4_from_domain(domain)
        self.assertNotEqual(answer, [])

    def test_host_is_active_returns_true_with_active_domain(self):
        domain = 'google.com'
        self.assertTrue(self.resolver.host_is_active(domain))

    def test_host_is_active_returns_false_with_inactive_domain(self):
        domain = 'notarealdomain.somefaketld'
        self.assertFalse(self.resolver.host_is_active(domain))

    def test_ip_is_active_returns_true_with_live_ip(self):
        ip = '8.8.8.8'  # google DNS server
        self.assertTrue(self.resolver.ip_is_active(ip))

    def test_ip_is_active_returns_false_with_fake_ip(self):
        ip = '203.0.113.0'  # invalid IP - RFC 5737
        self.assertFalse(self.resolver.ip_is_active(ip))


if __name__ == '__main__':
    unittest.main()
