# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
import pytest

from app.db.models import Booking
from tests.conftest import AUTH


# Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
# When: ผู้ใช้กดยืนยันการจองช่วง 09.00 น.
# Then: บันทึกสำเร็จ; แสดงหมายเลขคิว; ที่นั่งว่างของช่วงนั้นเป็น 0

def test_TC_BKG_01_1_successful_booking(client, make_slot, db):
    """TC-BKG-01-1: ทางปกติ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201
    payload = res.json()
    assert payload["queue_no"]
    booking = db.query(Booking).filter_by(slot_id=slot.id).one()
    assert booking.queue_no == payload["queue_no"]
    db.refresh(slot)
    assert slot.remaining == 0


# Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่างตรง 1 ที่ (ค่าแคมปัสขอบเขตก่อนจอง)
# When: ผู้ใช้กดยืนยันการจองช่วง 09.00 น.
# Then: บันทึกสำเร็จ; แสดงหมายเลขคิว; ที่นั่งว่างของช่วงนั้นลดจาก 1 เป็น 0

def test_TC_BKG_01_2_boundary_one_slot_remaining(client, make_slot, db):
    """TC-BKG-01-2: ขอบ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201
    payload = res.json()
    assert payload["queue_no"] == "A001"
    db.refresh(slot)
    assert slot.remaining == 0


# Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่ แต่ผู้ใช้ส่งยืนยันซ้ำในเวลาเดียวกัน
# When: ผู้ใช้กดยืนยันการจองช่วง 09.00 น. ครั้งที่ 2
# Then: spec ไม่ได้บอกว่าควรบันทึกหรือปฏิเสธเมื่อส่งคำขอซ้ำในเวลาเดียวกัน; ต้องมีการตัดสินใจจากทีมก่อนเขียน assert
@pytest.mark.skip(reason="spec ไม่ได้กำหนดผลลัพธ์สำหรับการยืนยันซ้ำในเวลาเดียวกัน จึงไม่เขียน assert จนกว่าจะมีการตัดสินใจจากทีม")
def test_TC_BKG_01_3_duplicate_submit_ambiguous(client, make_slot):
    """TC-BKG-01-3: ทางผิด (เงื่อนไขไม่ชัดเจนใน spec)"""
    slot = make_slot(start="09:00", remaining=1)

    client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)
    # ยังไม่ตรวจผลสำหรับการยืนยันซ้ำ เพราะ spec ไม่ได้บอกว่าควรเป็นอย่างไร
    pytest.skip("รอความชัดเจนจากทีมก่อนตรวจกรณีนี้")
