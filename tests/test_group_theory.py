import pytest
from src.group_theory.group import Group, GroupElement

@pytest.fixture
def C4():
    return Group(list(range(4)), lambda a, b: (a + b) % 4, identity_value=0)

@pytest.fixture
def C2():
    return Group([0, 1], lambda a, b: (a + b) % 2, identity_value=0)

def test_elements(C4):
    elements = C4.elements()
    assert len(elements) == 4
    assert all(isinstance(e, GroupElement) for e in elements)

def test_operation(C4):
    assert C4.operation(1, 2) == 3
    assert C4.operation(3, 2) == 1

def test_identity(C4):
    identity = C4.identity()
    assert identity.element == 0
    for e in C4.elements():
        assert e * identity == e
        assert identity * e == e

def test_inverse_property(C4):
    for e in C4.elements():
        inv = C4.inverse(e.element)
        assert e * inv == C4.identity()

def test_specific_inverse_values(C4, C4_elements):
    e, a = C4_elements
    assert a.inverse() == GroupElement(3, C4)
    assert e.inverse() == e

def test_order(C4):
    assert C4.order() == 4

def test_is_abelian(C4):
    assert C4.is_abelian()

def test_semidirect_product(C4, C2):
    def action(h, n):
        return n if h == 0 else (4 - n) % 4
    
    D4 = Group.semidirect_product(C4, C2, action)
    
    assert D4.order() == 8
    assert not D4.is_abelian()
    
    e = D4.identity()
    r = GroupElement((1, 0), D4)  # rotation
    s = GroupElement((0, 1), D4)  # reflection
    
    assert r * r * r * r == e
    assert s * s == e
    assert r * s != s * r

@pytest.fixture
def C4_elements(C4):
    return GroupElement(0, C4), GroupElement(1, C4)

def test_multiplication(C4, C4_elements):
    e, a = C4_elements
    assert a * a == GroupElement(2, C4)
    assert a * a * a == GroupElement(3, C4)
    assert a * a * a * a == e

def test_power(C4_elements):
    e, a = C4_elements
    assert a ** 0 == e
    assert a ** 1 == a
    assert a ** 2 == a * a
    assert a ** 4 == e
    assert a ** -1 == a ** 3

def test_element_equality(C4, C4_elements):
    e, a = C4_elements
    assert e == GroupElement(0, C4)
    assert e != a

def test_group_equality():
    # Test case 1: Same groups should be equal
    G1 = Group([0, 1], lambda a, b: (a + b) % 2, identity_value=0)
    G2 = Group([0, 1], lambda a, b: (a + b) % 2, identity_value=0)
    assert G1 == G2

    # Test case 2: Groups with different elements should not be equal
    G3 = Group([0, 1, 2], lambda a, b: (a + b) % 3, identity_value=0)
    assert G1 != G3

    # Test case 3: Groups with same elements but different operations should not be equal
    G4 = Group([0, 1], lambda a, b: max(a, b), identity_value=0)
    assert G1 != G4

    # Test case 4: Groups with same elements and operations but different identity values should not be equal
    G5 = Group([0, 1], lambda a, b: (a + b) % 2, identity_value=1)
    assert G1 != G5

    # Test case 5: A group should be equal to itself
    assert G1 == G1

    # Test case 6: Groups created with different but equivalent lambdas should be equal
    G6 = Group([0, 1], lambda x, y: (x + y) % 2, identity_value=0)
    assert G1 == G6

    # Test case 7: Group should not be equal to non-Group objects
    assert G1 != "Not a group"
    assert G1 != 42

    # Test case 8: Groups with elements in different order should still be equal
    G7 = Group([1, 0], lambda a, b: (a + b) % 2, identity_value=0)
    assert G1 == G7

def test_order(C4_elements):
    e, a = C4_elements
    assert e.order() == 1
    assert a.order() == 4

@pytest.fixture
def C2():
    return Group([0, 1], lambda a, b: (a + b) % 2, identity_value=0)

@pytest.fixture
def C3():
    return Group([0, 1, 2], lambda a, b: (a + b) % 3, identity_value=0)

@pytest.fixture
def C2_X_C3(C2, C3):
    return Group.direct_product(C2, C3)

def test_direct_product_order(C2_X_C3):
    assert C2_X_C3.order() == 6

def test_direct_product_elements(C2_X_C3):
    elements = C2_X_C3.elements()
    assert len(elements) == 6
    assert GroupElement((0, 0), C2_X_C3) in elements
    assert GroupElement((1, 2), C2_X_C3) in elements

def test_direct_product_operation(C2_X_C3):
    a = GroupElement((1, 0), C2_X_C3)
    b = GroupElement((0, 1), C2_X_C3)
    assert a * b == GroupElement((1, 1), C2_X_C3)
    assert b * a == GroupElement((1, 1), C2_X_C3)

def test_direct_product_identity(C2_X_C3):
    identity = C2_X_C3.identity()
    assert identity.element == (0, 0)
    a = GroupElement((1, 2), C2_X_C3)
    assert a * identity == a
    assert identity * a == a

def test_direct_product_inverse(C2_X_C3):
    a = GroupElement((1, 2), C2_X_C3)
    a_inv = C2_X_C3.inverse(a.element)
    assert a * a_inv == C2_X_C3.identity()
    assert a_inv * a == C2_X_C3.identity()

def test_direct_product_is_abelian(C2_X_C3):
    assert C2_X_C3.is_abelian()

def test_multiple_direct_product(C2, C3):
    C2_X_C2_X_C3 = Group.direct_product(C2, C2, C3)
    assert C2_X_C2_X_C3.order() == 12
    a = GroupElement((1, 0, 2), C2_X_C2_X_C3)
    b = GroupElement((0, 1, 1), C2_X_C2_X_C3)
    assert a * b == GroupElement((1, 1, 0), C2_X_C2_X_C3)