# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2026-10-07 08:31 | test: 5 ผ่าน, 1 skipped

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 (ย่อ) | T-02 | backend/app/slots/service.py:list_available_slots; backend/app/slots/router.py:get_slots | backend/tests/test_AC_BKG_05.py:test_AC_BKG_05 -> ผ่าน | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 | ไม่มีโค้ด/ทดสอบที่เกี่ยวข้อง | ไม่มี | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05, T-11, T-12 | frontend/src/pages/ConfirmBooking.jsx:ConfirmBooking; frontend/src/__tests__/AC-BKG-03.test.jsx:AC-BKG-03 ช่วงเวลาเต็ม แจ้งผู้ใช้และเสนอช่วงใกล้เคียง -> ไม่ผ่าน | frontend/src/__tests__/AC-BKG-03.test.jsx -> ไม่ผ่าน: alert text ต้องมี "ช่วงเวลาเต็ม" แต่โค้ดแสดง "เต็มแล้ว" และแสดงเฉพาะ 2 ตัวเลือกแทน 3 ตัว | ช่องโหว่ |
| FR-BKG-04 | AC-BKG-01 | T-03, T-06 | backend/app/booking/service.py:create_booking; backend/app/booking/router.py:create_booking | backend/tests/test_AC_BKG_01.py:test_TC_BKG_01_1_successful_booking, test_TC_BKG_01_2_boundary_one_slot_remaining -> ผ่าน; test_TC_BKG_01_3_duplicate_submit_ambiguous -> skipped | รอ Q-02 |
| FR-BKG-05 | AC-BKG-04 | T-07 | ไม่มีโค้ด/ทดสอบที่เกี่ยวข้อง | ไม่มี | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02 | backend/app/slots/service.py:list_available_slots; backend/app/slots/router.py:get_slots | backend/tests/test_AC_BKG_05.py เพียงตรวจความเร็ว ไม่ใช่การคัดกรองตามแพ็กเกจ | ครบ |
| NFR-PERF-01 | AC-BKG-05 | T-02 | backend/app/slots/service.py:list_available_slots | backend/tests/test_AC_BKG_05.py:test_AC_BKG_05 -> ผ่าน | ครบ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี | ไม่มี | ไม่มี | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 | ไม่มีโค้ด/ทดสอบที่เกี่ยวข้อง | ไม่มี | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี | ไม่มี | ไม่มี | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 | backend/app/db/session.py:get_db; backend/app/config.py | ไม่ใช่ test ที่ระบุชัดเจน แต่โครงแบบมีโค้ดตั้งค่า PostgreSQL ให้ใช้ `DATABASE_URL` | ครบ |
| DOM-PDPA-01 | AC-BKG-06 | T-08 | ไม่มีโค้ด/ทดสอบที่เกี่ยวข้อง | ไม่มี | ยังไม่ถึง |
| IF-IDP-01 | ไม่มี AC | T-03 | backend/app/auth/idp.py:get_verified_hn | backend/tests/test_AC_BKG_01.py ผ่านเนื่องจาก Authorization header ถูกยืนยัน | ครบ |
| IF-HIS-01 | ไม่มี AC | T-09 | backend/app/booking/router.py:BookingRequest.national_id; backend/app/booking/service.py:create_booking | ไม่มี | ยังไม่ถึง |
| IF-NOT-01 | AC-BKG-04 | T-07 | ไม่มีโค้ด/ทดสอบที่เกี่ยวข้อง | ไม่มี | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/app/slots/router.py:get_slots | FR-BKG-01, FR-BKG-06 | ไม่ครบ | `package_code` ถูกส่งเป็น required parameter และ filter ตามแพ็กเกจ แต่ช่วงเวลาที่คืนมีค่า `DAYS_AHEAD = 14` ไม่ตรง 30 วันตาม spec |
| backend/app/booking/router.py:create_booking | FR-BKG-04, IF-IDP-01 | บางส่วน | จองสำเร็จและตัดที่นั่งได้ แต่ `queue_no` ผูกกับคำตอบ Q-02 ซึ่งยังไม่ชัดเจน จึงยังไม่สามารถยืนยันความครบของรูปแบบหมายเลขคิว |
| backend/app/booking/router.py:BookingRequest | IF-HIS-01, DOM-PDPA-01 | ไม่ครบ | รับ `national_id` ลง request model และ log `national_id` โดย `logger.info` แม้ไม่ได้เก็บในตาราง bookings แต่กลับมีข้อมูลที่ constraints ต้องปกป้อง |
| backend/app/auth/idp.py:get_verified_hn | IF-IDP-01 | ครบ | ตรวจ Authorization header และคืน HN หลังจากยืนยันตัวตนแล้ว |
| backend/app/main.py:lifespan | CON-TECH-01 | บางส่วน | สร้าง schema ใน SQLite สำหรับ test ไม่ใช่ PostgreSQL จริง แต่โครงสร้างคำสั่งมี `DATABASE_URL` และแยกออกจาก config อย่างชัดเจน |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-01 | ตัวเลขไม่ตรง spec | backend/app/slots/service.py:DAYS_AHEAD = 14 | FR-BKG-01 | โค้ดกำหนดให้ส่งช่วงเวลาเพียง 14 วันข้างหน้า ขณะที่ spec กำหนด 30 วันข้างหน้า; test ที่มีอยู่ตรวจเฉพาะความเร็ว ไม่ได้ตรวจวัน 30 |  |
| F-02 | test อ่อน | backend/tests/test_AC_BKG_01.py:test_TC_BKG_01_1_successful_booking | AC-BKG-01 | Test ตรวจแค่ status 201 และมี `queue_no` แต่ไม่ตรวจว่า `remaining` ลดถูกต้องหลังจากการจองและไม่ตรวจกรณี slot=0 หรือ negative values |  |
| F-03 | ละเมิด Constraint | backend/app/booking/router.py:BookingRequest / logger.info | IF-HIS-01, DOM-PDPA-01 | รับและ log เลขบัตรประชาชน `national_id` แม้ไม่ได้เก็บลง bookings แต่ข้อมูลยังอยู่ใน request model และ log ของระบบ อาจรั่วไหลตามข้อมูลสุขภาพ/เลขประจำตัว |  |
| F-04 | test อ่อน / ไม่ตรง spec | frontend/src/pages/ConfirmBooking.jsx:ConfirmBooking; frontend/src/__tests__/AC-BKG-03.test.jsx | FR-BKG-03 | UI แจ้ง "เต็มแล้ว" แทน "ช่วงเวลาเต็ม" ตาม AC และ map เฉพาะ 2 ตัวเลือก (`slice(0, 2)`) แทน 3 ตัวเลือกที่ต้องเสนอ; test แสดงว่าตัวเลือกไม่ตรงกับ Then ของ AC |  |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
