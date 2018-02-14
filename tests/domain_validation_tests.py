#! python3

from lookup import valid_domain, valid_tld

def test_tld_validation():
    print("com", valid_tld("com"))
    print("net", valid_tld("net"))
    print("biz", valid_tld("biz"))
    print("us", valid_tld("us"))
    print("info", valid_tld("info"))
    print("online", valid_tld("online"))
    print("blank", valid_tld(""))
    print("abc", valid_tld("abc"))
    print("-1", valid_tld("-1"))


def test_domain_validation():
    errors = 0
    invalid_domains = ["",
                       "-1",
                       "google.123",
                       "google.",
                       "google",
                       "www.google",
                       "www.shop.spotify.theinternet",
                       "google.wtf"]

    valid_domains = ["google.com,"
                     "www.google.com"
                     "patientprograms.us",
                     "test.biz",
                     "test.us",
                     "test.online",
                     "test.info",
                     "test.net"]

    print("====== TESTING DOMAIN VALIDATION ======")
    for domain in invalid_domains:
        try:
            assert not valid_domain(domain)
        except AssertionError:
            errors += 1
            print("Failed to identify valid domain.....: " + domain)

    for domain in valid_domains:
        try:
            assert valid_domain(domain)
        except AssertionError:
            errors += 1
            print("Failed to identify invalid domain...: " + domain)

    if errors > 0:
        print("Total failed tests:", errors)
    else:
        print("All tests passed OK.")


def run_all_tests():
    test_tld_validation()
    test_domain_validation()

