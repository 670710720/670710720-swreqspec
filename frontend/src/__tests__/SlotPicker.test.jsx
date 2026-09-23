import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import SlotPicker from '../pages/SlotPicker.jsx'

const slotsByPackage = {
  GENERAL: [
    { id: 1, slot_date: '2026-09-24', start_time: '09:00:00', remaining: 2 },
  ],
  EXECUTIVE: [
    { id: 2, slot_date: '2026-09-24', start_time: '10:00:00', remaining: 1 },
  ],
}

test('แสดงช่วงเวลาว่างและจำนวนที่นั่งจาก API จำลอง และโหลดใหม่เมื่อเปลี่ยนแพ็กเกจ', async () => {
  const getSlots = vi.fn(({ packageCode }) =>
    Promise.resolve({ slots: slotsByPackage[packageCode] }),
  )
  render(<SlotPicker apiClient={{ getSlots }} />)

  expect(await screen.findByText(/09:00/)).toBeTruthy()
  expect(screen.getByText('ที่นั่งคงเหลือ 2 ที่')).toBeTruthy()

  fireEvent.change(screen.getByLabelText('แพ็กเกจ'), {
    target: { value: 'EXECUTIVE' },
  })

  await waitFor(() => expect(screen.getByText(/10:00/)).toBeTruthy())
  expect(screen.getByText('ที่นั่งคงเหลือ 1 ที่')).toBeTruthy()
  expect(getSlots).toHaveBeenLastCalledWith({
    dateFrom: expect.any(String),
    packageCode: 'EXECUTIVE',
  })
})
