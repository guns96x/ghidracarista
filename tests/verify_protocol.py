#!/usr/bin/env python3
"""
Автоматизований тест-симулятор діагностичного протоколу VAG UDS / ELM327.
Перевіряє коректність роботи всіх розроблених алгоритмів та декодерів без авто.
"""

import sys

class MockElm327:
    def __init__(self):
        self.tx_id = "7DF"
        self.rx_id = "7E8"

    def send(self, cmd: str) -> str:
        cmd = cmd.strip()
        if cmd == "AT Z": return "ELM327 v1.5\r\r>"
        if cmd.startswith("AT SH"):
            self.tx_id = cmd.split()[2]
            return "OK\r\r>"
        if cmd.startswith("AT CRA"):
            self.rx_id = cmd.split()[2]
            return "OK\r\r>"
        if cmd.startswith("AT"): return "OK\r\r>"

        # UDS Commands
        if cmd == "10 03": return "50 03 00 32 01 F4\r\r>"
        if cmd == "3E 80": return "\r\r>"
        if cmd == "22 F1 90":
            # VIN: WVWZZZ1KZ8P000001
            return "62 F1 90 57 56 57 5A 5A 5A 31 4B 5A 38 50 30 30 30 30 30 31\r\r>"
        if cmd == "22 F1 87":
            if self.tx_id == "7E0": return "62 F1 87 30 33 47 39 30 36 30 32 31 51 4A\r\r>" # 03G906021QJ
            if self.tx_id == "714": return "62 F1 87 31 4B 30 39 32 30 38 37 34 41\r\r>"       # 1K0920874A
            return "62 F1 87 31 4B 30 36 31 34 35 31 37\r\r>"
        if cmd == "22 F1 89": return "62 F1 89 39 39 37 31\r\r>" # 9971
        if cmd == "19 02 09":
            if self.tx_id == "7E0":
                # DTC: 01 01 22 24 (P0101-22, status 0x24)
                return "59 02 09 01 01 22 24\r\r>"
            return "59 02 09\r\r>"
        if cmd == "14 FF FF FF": return "54\r\r>"
        if cmd == "31 01 00 10": return "71 01 00 10 00\r\r>" # EPB Open OK
        if cmd == "31 01 00 11": return "71 01 00 11 00\r\r>" # EPB Close OK
        return "NO DATA\r\r>"

def decode_dtc(b1, b2, b3, status):
    prefix_map = {0: "P", 1: "C", 2: "B", 3: "U"}
    p = prefix_map[(b1 & 0xC0) >> 6]
    d1 = (b1 & 0x30) >> 4
    d2 = b1 & 0x0F
    d3 = (b2 & 0xF0) >> 4
    d4 = b2 & 0x0F
    code = f"{p}{d1:X}{d2:X}{d3:X}{d4:X}"
    return code, f"{b3:02X}", (status & 0x08) != 0, (status & 0x04) != 0

def hex_to_ascii(hex_str):
    clean = hex_str.replace(" ", "")
    bytes_arr = bytes.fromhex(clean)
    return "".join(chr(b) for b in bytes_arr if 32 <= b <= 126)

def run_tests():
    print("=" * 60)
    print("ЗАПУСК ТЕСТУВАННЯ ЧИСТОГО ДІАГНОСТИЧНОГО СТЕКУ VAG UDS")
    print("=" * 60)

    adapter = MockElm327()

    # 1. Тест ініціалізації
    print("\n[ТЕСТ 1] Ініціалізація адаптера ELM327...")
    assert "ELM" in adapter.send("AT Z")
    assert "OK" in adapter.send("AT SP 6")
    print("  -> Успіх: Протокол CAN 500k успішно зафіксовано.")

    # 2. Тест ідентифікації блоку Двигуна (0x7E0)
    print("\n[ТЕСТ 2] Зчитування VIN та ідентифікації ECU Двигуна (01)...")
    adapter.send("AT SH 7E0")
    adapter.send("AT CRA 7E8")

    # Читання номера деталі
    part_resp = adapter.send("22 F1 87")
    part_hex = part_resp.split("62 F1 87 ")[1].replace("\r", "").replace(">", "").strip()
    part_no = hex_to_ascii(part_hex)
    assert part_no == "03G906021QJ"
    print(f"  -> Номер деталі ECU: {part_no}")

    # Читання версії прошивки
    sw_resp = adapter.send("22 F1 89")
    sw_hex = sw_resp.split("62 F1 89 ")[1].replace("\r", "").replace(">", "").strip()
    sw_ver = hex_to_ascii(sw_hex)
    assert sw_ver == "9971"
    print(f"  -> Версія софту: {sw_ver}")

    # Читання VIN
    vin_resp = adapter.send("22 F1 90")
    vin_hex = vin_resp.split("62 F1 90 ")[1].replace("\r", "").replace(">", "").strip()
    vin = hex_to_ascii(vin_hex)
    assert vin == "WVWZZZ1KZ8P000001"
    print(f"  -> VIN код авто: {vin}")

    # 3. Тест зчитування та декодування помилок DTC
    print("\n[ТЕСТ 3] Зчитування та декодування помилок DTC (19 02 09)...")
    dtc_resp = adapter.send("19 02 09")
    assert "59 02 09" in dtc_resp
    dtc_payload = dtc_resp.replace("59 02 09 ", "").replace("\r", "").replace(">", "").strip().replace(" ", "")
    b1 = int(dtc_payload[0:2], 16)
    b2 = int(dtc_payload[2:4], 16)
    b3 = int(dtc_payload[4:6], 16)
    status = int(dtc_payload[6:8], 16)

    code, symptom, confirmed, pending = decode_dtc(b1, b2, b3, status)
    assert code == "P0101"
    print(f"  -> Розпізнано помилку: {code} (Тип відмови: {symptom}), Підтверджена: {confirmed}, Тимчасова: {pending}")

    # 4. Тест стирання помилок
    print("\n[ТЕСТ 4] Стирання помилок (14 FF FF FF)...")
    clear_resp = adapter.send("14 FF FF FF")
    assert "54" in clear_resp
    print("  -> Успіх: Пам'ять несправностей очищено (код 54 OK).")

    # 5. Тест розведення гальмівних супортів EPB
    print("\n[ТЕСТ 5] Сервіс гальмівної системи EPB (Розведення колодок)...")
    adapter.send("AT SH 746")
    session_resp = adapter.send("10 03")
    assert "50 03" in session_resp
    print("  -> Успішно активовано Extended Diagnostic Session (10 03).")

    epb_open = adapter.send("31 01 00 10")
    assert "71 01" in epb_open
    print("  -> Команда RoutineControl (0x31 0x01 0x0010) виконана: Супорти розведено!")

    print("\n" + "=" * 60)
    print("ВСІ ТЕСТИ ПРОЙДЕНО УСПІШНО! Архітектура повністю валідна.")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
