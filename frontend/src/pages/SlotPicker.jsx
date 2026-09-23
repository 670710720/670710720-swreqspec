import { useEffect, useState } from 'react'
import { api } from '../api/client.js'

const packages = [
  { code: 'GENERAL', label: 'ตรวจสุขภาพทั่วไป' },
  { code: 'EXECUTIVE', label: 'ตรวจสุขภาพผู้บริหาร' },
]

function formatSlotTime(startTime) {
  return startTime.slice(0, 5)
}

// หน้าจอเลือกแพ็กเกจและช่วงเวลาตาม FR-BKG-01 และ FR-BKG-06
export default function SlotPicker({ apiClient = api }) {
  const [packageCode, setPackageCode] = useState(packages[0].code)
  const [dateFrom, setDateFrom] = useState(() =>
    new Date().toISOString().slice(0, 10),
  )
  const [slots, setSlots] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    setLoading(true)
    setError('')

    apiClient
      .getSlots({ dateFrom, packageCode })
      .then((result) => {
        if (active) setSlots(result.slots ?? result)
      })
      .catch(() => {
        if (active) setError('ไม่สามารถโหลดช่วงเวลาว่างได้')
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => {
      active = false
    }
  }, [apiClient, dateFrom, packageCode])

  return (
    <section aria-labelledby="slot-picker-title">
      <h2 id="slot-picker-title" className="text-xl font-semibold text-teal-800">
        เลือกแพ็กเกจและช่วงเวลาตรวจ
      </h2>

      <div className="mt-4 grid gap-4 sm:grid-cols-2">
        <label className="grid gap-1">
          <span>แพ็กเกจ</span>
          <select
            aria-label="แพ็กเกจ"
            value={packageCode}
            onChange={(event) => setPackageCode(event.target.value)}
            className="rounded border p-2"
          >
            {packages.map((item) => (
              <option key={item.code} value={item.code}>
                {item.label}
              </option>
            ))}
          </select>
        </label>

        <label className="grid gap-1">
          <span>วันที่เริ่มค้นหา</span>
          <input
            aria-label="วันที่เริ่มค้นหา"
            type="date"
            value={dateFrom}
            onChange={(event) => setDateFrom(event.target.value)}
            className="rounded border p-2"
          />
        </label>
      </div>

      {loading && <p className="mt-4">กำลังโหลดช่วงเวลาว่าง...</p>}
      {error && (
        <p role="alert" className="mt-4 text-red-700">
          {error}
        </p>
      )}

      {!loading && !error && (
        <ul className="mt-4 grid gap-3" aria-label="ช่วงเวลาว่าง">
          {slots.length === 0 && <li>ไม่พบช่วงเวลาว่าง</li>}
          {slots.map((slot) => (
            <li key={slot.id} className="rounded border p-3">
              <div>
                {slot.slot_date} เวลา {formatSlotTime(slot.start_time)}
              </div>
              <div>ที่นั่งคงเหลือ {slot.remaining} ที่</div>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
