#!/usr/bin/env python3
"""Regression tests: exact suffix matches, rate limiting, and source provenance."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import capture_batch as c

assert c.exact_model_in_text("IMS-K22NH(DC)","Внутренний блок IGC IMS-K22NH(DC)"),"Exact original DC should match"
assert not c.exact_model_in_text("IMS-K22NH(DC)","Внутренний блок IGC IMS-K22NH(DC5)"),"DC5 must not be treated as DC"
assert not c.exact_model_in_text("IMS-QV45NH(DC)","IGC IMS-QV45NH(DC7)"),"DC7 must not match DC"
assert not c.exact_model_in_text("MIH90GHN18","Midea MIH90GHN18(DP)"),"Midea DP is a different SKU"
assert c.exact_model_in_text("MIH90GHN18(DP)","Midea MIH90GHN18(DP)"),"Exact DP should match"
assert not c.exact_model_in_text("KTKB18HZBN1","Kentatsu KTKB180HZBN1"),"Neighboring SKU must not match"
assert c.exact_model_in_text("KTKB18HZBN1","Внутренний блок Kentatsu KTKB18HZBN1"),"Exact Kentatsu SKU should match"

class FakeResponse:
    status_code=429
    headers={"Retry-After":"3600"}
    content=b"Too Many Requests"
    url="https://shop.example/ratelimited"
class FakeSession:
    calls=0
    def get(self,*args,**kwargs):
        self.calls+=1
        return FakeResponse()
old=c.SESSION
try:
    fake=FakeSession()
    c.SESSION=fake
    c.HTTP_ATTEMPT_LOG.clear()
    assert c.get("https://shop.example/ratelimited") is None
    assert fake.calls==1,"Respect long Retry-After; don't hammer site"
    assert c.HTTP_ATTEMPT_LOG[0]["status"]==429
finally:
    c.SESSION=old
print("REGRESSION_TESTS_PASSED: DC vs DC5/DC7, MIH DP suffix, neighboring SKU, HTTP Retry-After throttle")
