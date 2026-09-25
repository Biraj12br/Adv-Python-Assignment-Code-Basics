
from testing.pricing import member_price, add_gst, delivery_fee, loyalty_points


def test_member_price():
    assert member_price(1000, 10) == 900.0


def test_member_price_full_discount():
    assert member_price(250, 100) == 0.0


def test_add_gst():
    assert add_gst(1000, 5) == 1050.0


def test_add_gst_custom_rate():
    assert add_gst(1000, 10) == 1100.0


def test_delivery_fee_below_threshold():
    assert delivery_fee(499) == 40


def test_delivery_fee_at_threshold():
    assert delivery_fee(500) == 0


def test_delivery_fee_above_threshold():
    assert delivery_fee(600) == 0


def test_loyalty_points():
    assert loyalty_points(950) == 9


def test_loyalty_points_edge_case():
    assert loyalty_points(99) == 0

