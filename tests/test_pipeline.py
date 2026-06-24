import pytest
from app.crypto.search import SearchableEncryption
from app.crypto.encrypt import encrypt_data, decrypt_data
from app.auth.rbac import RBAC
from app.coordinator.query_router import ShardRouter


# ==============================
# Test 1: Encryption round-trip
# ==============================
def test_encrypt_decrypt_roundtrip():
    """Encrypting then decrypting should return original text"""
    original = "Employee Salary: 100000"
    nonce, ciphertext, key_version = encrypt_data(original)
    result = decrypt_data(nonce, ciphertext, key_version)
    assert result == original


# ==============================
# Test 2: Trapdoor matches token
# ==============================
def test_trapdoor_matches_token():
    """Trapdoor generated for a keyword must match its stored token"""
    key = b"week3-secret-key"
    se = SearchableEncryption(key)
    token = se.generate_token("salary")
    trapdoor = se.generate_trapdoor("salary")
    assert token == trapdoor


# ==============================
# Test 3: Different keywords give different tokens
# ==============================
def test_different_keywords_different_tokens():
    """Two different keywords must never produce the same token"""
    key = b"week3-secret-key"
    se = SearchableEncryption(key)
    assert se.generate_token("salary") != se.generate_token("bonus")


# ==============================
# Test 4: Multi-keyword trapdoor count
# ==============================
def test_multi_keyword_trapdoor_count():
    """generate_and_trapdoor should return one trapdoor per keyword"""
    key = b"week3-secret-key"
    se = SearchableEncryption(key)
    trapdoors = se.generate_and_trapdoor(["salary", "bonus", "tax"])
    assert len(trapdoors) == 3


# ==============================
# Test 5: RBAC - admin can search and decrypt
# ==============================
def test_admin_can_search_and_decrypt():
    rbac = RBAC()
    assert rbac.authorize("admin", "search") == True
    assert rbac.authorize("admin", "decrypt") == True


# ==============================
# Test 6: RBAC - analyst cannot decrypt
# ==============================
def test_analyst_cannot_decrypt():
    rbac = RBAC()
    assert rbac.authorize("analyst", "search") == True
    assert rbac.authorize("analyst", "decrypt") == False


# ==============================
# Test 7: RBAC - unknown role is rejected
# ==============================
def test_unknown_role_rejected():
    rbac = RBAC()
    assert rbac.authorize("hacker", "search") == False
    assert rbac.authorize("guest", "decrypt") == False


# ==============================
# Test 8: Shard routing is deterministic
# ==============================
def test_shard_routing_is_deterministic():
    """Same user must always route to the same shard"""
    router = ShardRouter()
    _, index1 = router.route("sarbasish")
    _, index2 = router.route("sarbasish")
    assert index1 == index2


# ==============================
# Test 9: Different users can route to different shards
# ==============================
def test_different_users_can_route_differently():
    """Routing function should distribute users across shards"""
    router = ShardRouter()
    indices = set()
    users = ["sarbasish", "kunal", "rohit", "alice", "bob", "charlie"]
    for user in users:
        _, index = router.route(user)
        indices.add(index)
    # With 6 users across 3 shards, we expect more than 1 shard used
    assert len(indices) > 1