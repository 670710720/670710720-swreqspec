# Tasks: จองคิวตรวจสุขภาพ (Booking)

- Feature: จองคิวตรวจสุขภาพ (Booking)
- Spec ID: SPEC-BKG-001
- อ้างอิง: [plan.md](./plan.md)
- วันที่: 2569-09-23

มีทั้งหมด 16 tasks โดย 1 task ต้องรอคำตอบ Open Question Q-02
งานที่ไม่เกี่ยวกับรูปแบบหมายเลขคิวสามารถเริ่มได้ทันทีตามลำดับการพึ่งพา

## รายการงาน

### T-01 สร้างโมเดลและ migration ฐานข้อมูล
- รองรับ: CON-TECH-01, IF-HIS-01, DOM-PDPA-01, FR-BKG-01, FR-BKG-02, FR-BKG-04
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02, T-03, T-04 และ T-07
- ไฟล์ที่แตะ: `backend/app/db/models.py`, `backend/app/db/session.py`, `backend/app/db/migrations/001_init.py`, `backend/tests/conftest.py`, `backend/tests/test_T01_database.py`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: migration สร้างตาราง `slots`, `bookings` และ `audit_logs` ได้ และตาราง `bookings` ไม่มีคอลัมน์ `national_id`
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 สร้างการตรวจสิทธิ์ยืนยันตัวตนและการค้น HN
- รองรับ: IF-IDP-01, IF-HIS-01, ASM-04
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03 และ T-08
- ไฟล์ที่แตะ: `backend/app/auth/idp.py`, `backend/app/his/client.py`, `backend/app/main.py`, `backend/tests/test_idp_his.py`
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: endpoint ที่แตะข้อมูลผู้รับบริการตรวจผลยืนยันตัวตน และ lookup ส่งเลขบัตรต่อ HIS แล้วคืนเฉพาะ `hn` โดยไม่บันทึกเลขบัตร
- สถานะ: พร้อมทำ

### T-03 สร้าง API ค้นช่วงเวลาว่าง
- รองรับ: FR-BKG-01, FR-BKG-06, ASM-01, ASM-02, IF-IDP-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: `backend/app/slots/service.py`, `backend/app/slots/router.py`, `backend/app/main.py`, `backend/tests/test_AC_BKG_05.py`
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: `GET /slots` คืนช่วงเวลาภายใน 30 วันพร้อม `remaining` และคำนวณรายการใหม่เมื่อเปลี่ยน `package_code` ได้
- สถานะ: พร้อมทำ

### T-04 สร้างบริการจองและตัดที่นั่งแบบปลอดภัย
- รองรับ: FR-BKG-04, CON-TECH-01, IF-IDP-01, IF-HIS-01
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: `backend/app/booking/service.py`, `backend/app/booking/router.py`, `backend/app/main.py`, `backend/tests/test_AC_BKG_01.py`
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: `POST /bookings` บันทึก booking ด้วย `hn`, ตัด `remaining` เหลือ 0 เมื่อมีที่นั่งสุดท้าย และคืน booking id กับหมายเลขคิวตามส่วนที่ระบบกำหนดได้
- สถานะ: พร้อมทำ

### T-05 ป้องกันการจองซ้ำในวันเดียวกัน
- รองรับ: FR-BKG-02, ASM-02, IF-IDP-01
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: `backend/app/booking/service.py`, `backend/app/booking/router.py`, `backend/tests/test_AC_BKG_02.py`
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: การจองซ้ำของผู้รับบริการในวันเดียวกันถูกปฏิเสธและ response แสดงหมายเลขคิวเดิม
- สถานะ: พร้อมทำ

### T-06 เสนอช่วงเวลาใกล้เคียงเมื่อช่วงเต็ม
- รองรับ: FR-BKG-03, ASM-02, IF-IDP-01
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: `backend/app/slots/service.py`, `backend/app/booking/service.py`, `backend/app/booking/router.py`, `backend/tests/test_AC_BKG_03.py`
- ต้องทำหลัง: T-03, T-04
- เสร็จเมื่อ: เมื่อช่วงเต็มระหว่างยืนยัน API คืน 409 พร้อม 3 ช่วงที่ว่างและใกล้ที่สุดในวันเดียวกันหรือวันถัดไป และไม่สร้าง booking ซ้อน
- สถานะ: พร้อมทำ

### T-07 สร้างคิวส่งข้อความและการส่งซ้ำ
- รองรับ: FR-BKG-05, IF-NOT-01, NFR-REL-02, ASM-03
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: `backend/app/notify/queue.py`, `backend/app/booking/service.py`, `backend/app/booking/router.py`, `backend/tests/test_AC_BKG_04.py`
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: การจองยังคงถูกบันทึกและแสดงผลได้เมื่อ notification ล้มเหลว พร้อมมีงาน retry ในคิวที่กำหนดส่งภายใน 5 นาที
- สถานะ: พร้อมทำ

### T-08 บันทึก audit log ทุกการเข้าถึง
- รองรับ: DOM-PDPA-01, IF-IDP-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: `backend/app/audit/middleware.py`, `backend/app/main.py`, `backend/tests/test_AC_BKG_06.py`
- ต้องทำหลัง: T-01, T-02, T-04
- เสร็จเมื่อ: การเปิดดูข้อมูล booking สร้าง audit log ที่มี `actor_id`, `accessed_at` และ `hn` และกำหนดการเก็บรักษาไม่น้อยกว่า 1 ปี
- สถานะ: พร้อมทำ

### T-09 บังคับการรับส่งข้อมูลด้วย TLS
- รองรับ: NFR-SEC-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของการ deploy API
- ไฟล์ที่แตะ: `backend/app/config.py`, `backend/app/main.py`, `backend/tests/test_security_transport.py`
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: การตั้งค่า API และเอกสารรันระบบกำหนดให้ client เชื่อมต่อด้วย TLS 1.2 ขึ้นไปและมี test ตรวจค่า configuration
- สถานะ: พร้อมทำ

### T-10 กำหนดวิธีออกหมายเลขคิว
- รองรับ: FR-BKG-04, FR-BKG-05, Q-02
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-11
- ไฟล์ที่แตะ: `backend/app/booking/service.py`, `backend/app/db/models.py`, `backend/tests/test_queue_number.py`
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: ทีมตอบ Q-02 แล้วจึงกำหนดรูปแบบและกติกาการออก `queue_no` ในระบบและ test ได้
- สถานะ: รอ Q-02

### T-11 สร้างหน้าเลือกแพ็กเกจและช่วงเวลา
- รองรับ: FR-BKG-01, FR-BKG-06, IF-IDP-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-12
- ไฟล์ที่แตะ: `frontend/src/pages/SlotPicker.jsx`, `frontend/src/api/client.js`, `frontend/src/App.jsx`, `frontend/src/__tests__/SlotPicker.test.jsx`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้าจอเลือกแพ็กเกจ เรียก API จำลองเพื่อแสดงช่วงเวลาว่างและจำนวนที่นั่ง และโหลดข้อมูลใหม่เมื่อเปลี่ยนแพ็กเกจได้
- สถานะ: เสร็จ รอทีมตรวจ

### T-12 สร้างหน้ายืนยันและตัวเลือกช่วงทดแทน
- รองรับ: FR-BKG-03, FR-BKG-04
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: `frontend/src/pages/ConfirmBooking.jsx`, `frontend/src/__tests__/AC-BKG-03.test.jsx`
- ต้องทำหลัง: T-11
- เสร็จเมื่อ: เมื่อ API จำลองตอบ 409 หน้าจอแสดง “ช่วงเวลาเต็ม” และตัวเลือกช่วงว่าง 3 รายการ พร้อมทำงานกรณียืนยันสำเร็จ
- สถานะ: พร้อมทำ

### T-13 สร้างหน้าผลการจอง
- รองรับ: FR-BKG-04, FR-BKG-05
- ตรวจด้วย: AC-BKG-01, AC-BKG-04
- ไฟล์ที่แตะ: `frontend/src/pages/BookingResult.jsx`, `frontend/src/__tests__/BookingResult.test.jsx`
- ต้องทำหลัง: T-11
- เสร็จเมื่อ: หน้าจอแสดงหมายเลขคิวจาก API จำลองทั้งกรณีส่งข้อความสำเร็จและกรณีส่งข้อความไม่สำเร็จ
- สถานะ: พร้อมทำ

### T-14 เชื่อมหน้าจอกับ API จริง
- รองรับ: FR-BKG-01, FR-BKG-03, FR-BKG-04, FR-BKG-05, IF-IDP-01
- ตรวจด้วย: AC-BKG-01, AC-BKG-03, AC-BKG-04
- ไฟล์ที่แตะ: `frontend/src/api/client.js`, `frontend/src/App.jsx`, `frontend/src/pages/SlotPicker.jsx`, `frontend/src/pages/ConfirmBooking.jsx`, `frontend/src/pages/BookingResult.jsx`
- ต้องทำหลัง: T-03, T-06, T-07, T-11, T-12, T-13
- เสร็จเมื่อ: หน้าจอเรียก endpoint จริงผ่าน `/api` และแสดงผลสำเร็จ, 409 ช่วงเต็ม และผล notification ล้มเหลวตามสัญญา API
- สถานะ: พร้อมทำ

### T-15 ทดสอบประสิทธิภาพการค้นหาช่วงเวลา
- รองรับ: NFR-PERF-01, FR-BKG-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: `backend/tests/test_AC_BKG_05.py`, `backend/tests/performance/`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: การทดสอบยิง `GET /slots` แบบจำลองผู้ใช้พร้อมกัน 200 คนรายงานค่า p95 และตรวจเกณฑ์ไม่เกิน 2 วินาที
- สถานะ: พร้อมทำ

### T-16 ประเมิน usability สำหรับผู้ใช้ใหม่
- รองรับ: NFR-USE-01, ASM-05
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นการตรวจ NFR-USE-01
- ไฟล์ที่แตะ: `frontend/src/__tests__/usability/`, `frontend/README.md`
- ต้องทำหลัง: T-14
- เสร็จเมื่อ: มีแผนและแบบบันทึกการทดสอบกับอาสาสมัครใหม่ 10 คน เพื่อวัดว่าผ่านภายใน 3 นาทีอย่างน้อย 8 คนโดยไม่ขอความช่วยเหลือ
- สถานะ: พร้อมทำ

## ตารางตรวจความครบ

### Acceptance Criteria

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-04, T-13, T-14 |
| AC-BKG-02 | T-05 |
| AC-BKG-03 | T-06, T-12, T-14 |
| AC-BKG-04 | T-07, T-13, T-14 |
| AC-BKG-05 | T-03, T-15 |
| AC-BKG-06 | T-08 |

### Constraints

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01, T-04 |
| DOM-PDPA-01 | T-01, T-08 |
| IF-IDP-01 | T-02, T-03, T-04, T-05, T-06, T-08, T-14 |
| IF-HIS-01 | T-01, T-02, T-04 |
| IF-NOT-01 | T-07, T-14 |

## สิ่งที่ยังไม่ทำ

- Q-02: หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง และมีรูปแบบอย่างไร (เช่น A001) ต้องถามเจ้าหน้าที่เวชระเบียน
  - งานที่รอ: T-10
  - จนกว่าจะได้คำตอบ ยังไม่กำหนดวิธีออกหมายเลขคิว แต่ task อื่นสามารถใช้ช่อง `queue_no` ตามสัญญาได้
