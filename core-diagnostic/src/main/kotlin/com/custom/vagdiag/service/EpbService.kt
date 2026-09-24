package com.custom.vagdiag.service

import com.custom.vagdiag.model.VagEcu
import com.custom.vagdiag.protocol.UdsCommunicator
import kotlinx.coroutines.delay

/**
 * Сервіс заміни задніх гальмівних колодок (EPB - Electronic Parking Brake).
 * Працює через блок стоянкового гальма (0x53 або 0x03 ABS у платформі MQB).
 */
class EpbService(private val uds: UdsCommunicator) {

    /**
     * Крок 1: Розведення гальмівних супортів (відкриття поршнів).
     * Автомобіль повинен стояти на рівній поверхні з вимкненим ручником.
     */
    suspend fun openCalipersForService(ecu: VagEcu = VagEcu.PARKING_BRAKE): Result<String> {
        val sessionOk = uds.enterExtendedSession(ecu)
        if (!sessionOk) return Result.failure(IllegalStateException("Блок EPB відхилив вхід у розширену сесію"))

        // Рутина відкриття супортів: 0x0010
        val ok = uds.startRoutine(ecu, "00 10")
        if (!ok) return Result.failure(IllegalStateException("Помилка виконання команди розведення супортів"))

        // Підтримка сесії під час фізичного руху моторів супортів
        repeat(5) {
            delay(1000)
            uds.sendTesterPresent()
        }

        return Result.success("Супорти успішно розведено. Можна замінювати гальмівні колодки.")
    }

    /**
     * Крок 2: Зведення супортів після встановлення нових колодок.
     */
    suspend fun closeCalipersAfterService(ecu: VagEcu = VagEcu.PARKING_BRAKE): Result<String> {
        val sessionOk = uds.enterExtendedSession(ecu)
        if (!sessionOk) return Result.failure(IllegalStateException("Блок EPB відхилив вхід у розширену сесію"))

        // Рутина зведення супортів: 0x0011
        val ok = uds.startRoutine(ecu, "00 11")
        if (!ok) return Result.failure(IllegalStateException("Помилка виконання команди зведення супортів"))

        repeat(5) {
            delay(1000)
            uds.sendTesterPresent()
        }

        return Result.success("Супорти зведено. Перейдіть до базового калібрування.")
    }

    /**
     * Крок 3: Базове калібрування та перевірка товщини колодок.
     */
    suspend fun runBasicAdaptation(ecu: VagEcu = VagEcu.PARKING_BRAKE): Result<String> {
        uds.enterExtendedSession(ecu)
        // Рутина адаптації EPB: 0x0012
        val ok = uds.startRoutine(ecu, "00 12")
        return if (ok) {
            Result.success("Калібрування EPB успішно завершено.")
        } else {
            Result.failure(IllegalStateException("Помилка під час адаптації EPB."))
        }
    }
}
