package com.custom.vagdiag.mock

import com.custom.vagdiag.transport.TransportInterface

/**
 * Віртуальний симулятор автомобіля та ELM327 адаптера.
 * Дозволяє тестувати 100% діагностичного стеку без підключення до реального авто.
 */
class MockTransport : TransportInterface {

    private var connected = false
    private var currentTxId = "7DF"
    private var currentRxId = "7E8"

    override suspend fun open(): Boolean {
        connected = true
        return true
    }

    override suspend fun close() {
        connected = false
    }

    override fun isConnected(): Boolean = connected

    override suspend fun sendCommand(command: String, timeoutMs: Long): String {
        val cleanCmd = command.trim()

        // 1. Обробка AT-команд адаптера
        if (cleanCmd.startsWith("AT")) {
            return when {
                cleanCmd == "AT Z" || cleanCmd == "AT WS" -> "ELM327 v1.5\r\r>"
                cleanCmd.startsWith("AT SH") -> {
                    currentTxId = cleanCmd.removePrefix("AT SH").trim()
                    "OK\r\r>"
                }
                cleanCmd.startsWith("AT CRA") -> {
                    currentRxId = cleanCmd.removePrefix("AT CRA").trim()
                    "OK\r\r>"
                }
                else -> "OK\r\r>"
            }
        }

        // 2. Обробка діагностичних UDS команд відповідно до обраного блоку
        return when {
            // Вхід у сесію: 10 03 -> відповідь 50 03
            cleanCmd.startsWith("10 03") -> "50 03 00 32 01 F4\r\r>"

            // TesterPresent: 3E 80 -> немає відповіді (або OK)
            cleanCmd.startsWith("3E") -> "\r\r>"

            // Зчитування VIN (22 F1 90)
            cleanCmd.startsWith("22 F1 90") -> {
                // Відповідь: "WVWZZZ1KZ8P000001" у Hex ASCII
                "62 F1 90 57 56 57 5A 5A 5A 31 4B 5A 38 50 30 30 30 30 30 31\r\r>"
            }

            // Зчитування номера деталі (22 F1 87)
            cleanCmd.startsWith("22 F1 87") -> {
                when (currentTxId) {
                    "7E0" -> "62 F1 87 30 33 47 39 30 36 30 32 31 51 4A\r\r>" // 03G906021QJ (EDC16)
                    "714" -> "62 F1 87 31 4B 30 39 32 30 38 37 34 41\r\r>"       // 1K0920874A (Cluster)
                    "713" -> "62 F1 87 31 4B 30 36 31 34 35 31 37\r\r>"          // 1K0614517 (ABS)
                    else -> "62 F1 87 35 51 30 39 33 37 30 38 34\r\r>"           // 5Q0937084 (BCM)
                }
            }

            // Зчитування версії софту (22 F1 89)
            cleanCmd.startsWith("22 F1 89") -> "62 F1 89 39 39 37 31\r\r>" // "9971"

            // Зчитування списку встановлених ECU з Gateway (22 04 A1 - 4 байти на запис)
            cleanCmd.startsWith("22 04 A1") -> {
                // Відповідь Gateway: список ECU (01-Engine, 02-Trans, 03-ABS, 08-HVAC, 09-BCM, 15-Airbag, 17-Cluster, 19-Gateway, 53-EPB)
                "62 04 A1 01 01 00 00 02 01 00 00 03 01 00 00 08 01 00 00 09 01 00 00 15 01 00 00 17 01 00 00 19 01 00 00 53 01 00 00\r\r>"
            }

            // Статус паркувального гальма (DID 0x0102)
            cleanCmd.startsWith("22 01 02") -> "62 01 02 00 00\r\r>"

            // Зчитування помилок DTC (19 02 8D / 19 02)
            cleanCmd.startsWith("19 02") -> {
                if (currentTxId == "7E0") {
                    // Симулюємо помилку двигуна: P0101-22 зі статусом 0x24 (Confirmed + Pending)
                    // Формат: 59 02 [AvailabilityMask] [DTC 3-byte] [Status 1-byte]
                    "59 02 8D 01 01 22 24\r\r>"
                } else {
                    // Інші блоки без помилок
                    "59 02 8D\r\r>"
                }
            }

            // Стирання помилок (14 FF FF FF)
            cleanCmd.startsWith("14") -> "54\r\r>"

            // Рутини сервісу EPB (Start/Stop: 0x03A1 Open, 0x03A0 Close, 0x03A2 Adapt)
            cleanCmd.startsWith("31 01 03 A1") -> "71 01 03 A1 00\r\r>"
            cleanCmd.startsWith("31 02 03 A1") -> "71 02 03 A1 00\r\r>"
            cleanCmd.startsWith("31 01 03 A0") -> "71 01 03 A0 00\r\r>"
            cleanCmd.startsWith("31 02 03 A0") -> "71 02 03 A0 00\r\r>"
            cleanCmd.startsWith("31 01 03 A2") -> "71 01 03 A2 00\r\r>"
            cleanCmd.startsWith("31 02 03 A2") -> "71 02 03 A2 00\r\r>"
            cleanCmd.startsWith("31 01") -> "71 01 00 00 00\r\r>"
            cleanCmd.startsWith("31 02") -> "71 02 00 00 00\r\r>"

            else -> "NO DATA\r\r>"
        }
    }
}
