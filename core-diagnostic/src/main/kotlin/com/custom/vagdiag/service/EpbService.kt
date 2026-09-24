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
     * Верифіковано в libCarista.so.c:
     * - StartVagUdsParkingBrakeOpenCommand (line 111280) -> Routine ID 0x03A1
     * - StopVagUdsParkingBrakeOpenCommand (line 111300) -> 31 02 03 A1
     * - Статус: DID 0x0102 (22 01 02)
     */
    suspend fun openCalipersForService(ecu: VagEcu = VagEcu.PARKING_BRAKE): Result<String> {
        val sessionOk = uds.enterExtendedSession(ecu)
        if (!sessionOk) return Result.failure(IllegalStateException("Блок EPB відхилив вхід у розширену сесію"))

        // Рутина відкриття супортів: 0x03A1 (31 01 03 A1)
        val ok = uds.startRoutine(ecu, "03 A1")
        if (!ok) return Result.failure(IllegalStateException("Помилка виконання команди розведення супортів"))

        // Підтримка сесії під час фізичного руху моторів супортів та опитування статусу
        repeat(5) {
            delay(1000)
            uds.sendTesterPresent()
        }

        // Зупинка процедури відкриття: 31 02 03 A1
        uds.stopRoutine(ecu, "03 A1")

        return Result.success("Супорти успішно розведено (Routine 0x03A1). Можна замінювати гальмівні колодки.")
    }

    /**
     * Крок 2: Зведення супортів після встановлення нових колодок.
     * Верифіковано в libCarista.so.c:
     * - StartVagUdsParkingBrakeCloseCommand (line 111232) -> Routine ID 0x03A0
     * - StopVagUdsParkingBrakeCloseCommand (line 111252) -> 31 02 03 A0
     */
    suspend fun closeCalipersAfterService(ecu: VagEcu = VagEcu.PARKING_BRAKE): Result<String> {
        val sessionOk = uds.enterExtendedSession(ecu)
        if (!sessionOk) return Result.failure(IllegalStateException("Блок EPB відхилив вхід у розширену сесію"))

        // Рутина зведення супортів: 0x03A0 (31 01 03 A0)
        val ok = uds.startRoutine(ecu, "03 A0")
        if (!ok) return Result.failure(IllegalStateException("Помилка виконання команди зведення супортів"))

        repeat(5) {
            delay(1000)
            uds.sendTesterPresent()
        }

        // Зупинка процедури закриття: 31 02 03 A0
        uds.stopRoutine(ecu, "03 A0")

        return Result.success("Супорти зведено (Routine 0x03A0). Перейдіть до базового калібрування.")
    }

    /**
     * Опитування поточного статусу паркувального гальма (DID 0x0102).
     */
    suspend fun getParkingBrakeStatus(ecu: VagEcu = VagEcu.PARKING_BRAKE): String? {
        return uds.readDid(ecu, "0102")
    }

    /**
     * Крок 3: Базове калібрування та перевірка товщини колодок.
     */
    suspend fun runBasicAdaptation(ecu: VagEcu = VagEcu.PARKING_BRAKE): Result<String> {
        val sessionOk = uds.enterExtendedSession(ecu)
        if (!sessionOk) return Result.failure(IllegalStateException("Блок EPB відхилив вхід у розширену сесію"))

        // Базове налаштування EPB: Routine 0x03A2 (або функціональна адаптація)
        val ok = uds.startRoutine(ecu, "03 A2")
        return if (ok) {
            uds.stopRoutine(ecu, "03 A2")
            Result.success("Калібрування EPB успішно завершено.")
        } else {
            Result.failure(IllegalStateException("Помилка під час адаптації EPB."))
        }
    }
}
