package com.custom.vagdiag.protocol

import com.custom.vagdiag.model.EcuIdentity
import com.custom.vagdiag.model.FaultCode
import com.custom.vagdiag.model.VagEcu
import com.custom.vagdiag.transport.Elm327Engine

/**
 * Реалізація сервісів UDS (Unified Diagnostic Services - ISO 14229-1) для блоків VAG.
 */
class UdsCommunicator(private val engine: Elm327Engine) {

    /**
     * Перехід у розширену діагностичну сесію (0x10 0x03).
     * Необхідна для кодування, базових налаштувань, скидання сервісу та EPB.
     */
    suspend fun enterExtendedSession(ecu: VagEcu): Boolean {
        engine.setEcuFilter(ecu.txCanId, ecu.rxCanId)
        val resp = engine.sendUdsFrame("10 03")
        return resp.contains("5003")
    }

    /**
     * Відправка пінґу TesterPresent (0x3E 0x80) для утримання активної сесії.
     */
    suspend fun sendTesterPresent() {
        engine.sendUdsFrame("3E 80")
    }

    /**
     * Зчитування повної ідентифікації блоку (номер деталі, софт, VIN, кодування).
     */
    suspend fun readEcuIdentity(ecu: VagEcu): EcuIdentity? {
        engine.setEcuFilter(ecu.txCanId, ecu.rxCanId)

        // 1. Номер запчастини VAG Part No (DID 0xF187)
        val partNoRaw = readDidString(ecu, "F187") ?: return null

        // 2. Версія прошивки SW Version (DID 0xF189)
        val swVer = readDidString(ecu, "F189") ?: "Unknown"

        // 3. VIN авто (DID 0xF190)
        val vin = readDidString(ecu, "F190")

        // 4. Довге кодування (DID 0xF1A3)
        val codingHex = readDidHex(ecu, "F1A3")

        return EcuIdentity(
            ecu = ecu,
            partNumber = partNoRaw,
            swVersion = swVer,
            vin = vin,
            longCodingHex = codingHex
        )
    }

    /**
     * Зчитування активних та збережених помилок DTC (Сервіс 0x19 0x02 0x09).
     */
    suspend fun readFaultCodes(ecu: VagEcu): List<FaultCode> {
        engine.setEcuFilter(ecu.txCanId, ecu.rxCanId)
        val resp = engine.sendUdsFrame("19 02 09")

        // Очікуваний заголовок позитивної відповіді: 59 02 09
        val marker = "590209"
        val idx = resp.indexOf(marker)
        if (idx == -1) return emptyList()

        val payload = resp.substring(idx + marker.length)
        if (payload.isEmpty() || payload.length % 8 != 0) {
            // Кожна помилка в UDS займає 4 байти (8 hex символів): 3 байти DTC + 1 байт статусу
            val validLength = (payload.length / 8) * 8
            if (validLength == 0) return emptyList()
        }

        val result = mutableListOf<FaultCode>()
        val chunks = payload.chunked(8)
        for (chunk in chunks) {
            if (chunk.length == 8) {
                val b1 = chunk.substring(0, 2).toInt(16)
                val b2 = chunk.substring(2, 4).toInt(16)
                val b3 = chunk.substring(4, 6).toInt(16)
                val status = chunk.substring(6, 8).toInt(16)
                result.add(FaultCode.fromUdsBytes(b1, b2, b3, status))
            }
        }
        return result
    }

    /**
     * Очищення пам'яті помилок усіх груп (Сервіс 0x14 FF FF FF).
     */
    suspend fun clearAllDtc(ecu: VagEcu): Boolean {
        engine.setEcuFilter(ecu.txCanId, ecu.rxCanId)
        val resp = engine.sendUdsFrame("14 FF FF FF")
        // Позитивна відповідь: 54
        return resp.contains("54")
    }

    /**
     * Запуск спеціальної процедури RoutineControl (0x31 0x01 <RoutineId>).
     */
    suspend fun startRoutine(ecu: VagEcu, routineIdHex: String): Boolean {
        enterExtendedSession(ecu)
        val resp = engine.sendUdsFrame("31 01 $routineIdHex")
        // Позитивна відповідь починається з 71 01
        return resp.contains("7101")
    }

    // --- Допоміжні методи читання DID (Data Identifier 0x22) ---

    private suspend fun readDidString(ecu: VagEcu, didHex: String): String? {
        val resp = engine.sendUdsFrame("22 $didHex")
        val marker = "62" + didHex.replace(" ", "")
        val idx = resp.indexOf(marker)
        if (idx == -1) return null

        val hexData = resp.substring(idx + marker.length)
        return hexData.chunked(2)
            .mapNotNull {
                try {
                    val code = it.toInt(16)
                    if (code in 32..126) code.toChar() else null
                } catch (e: Exception) { null }
            }
            .joinToString("")
            .trim()
    }

    private suspend fun readDidHex(ecu: VagEcu, didHex: String): String? {
        val resp = engine.sendUdsFrame("22 $didHex")
        val marker = "62" + didHex.replace(" ", "")
        val idx = resp.indexOf(marker)
        if (idx == -1) return null
        return resp.substring(idx + marker.length)
    }
}
