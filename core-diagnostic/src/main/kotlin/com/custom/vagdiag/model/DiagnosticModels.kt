package com.custom.vagdiag.model

/**
 * Стандартні блоки керування (ECU) автомобілів групи VAG (PQ35, MQB, MLB).
 * Кожен блок має визначену пару 11-бітних CAN ID для запиту (txId) та відповіді (rxId).
 */
enum class VagEcu(
    val addressHex: String,
    val moduleNameUk: String,
    val txCanId: String,
    val rxCanId: String
) {
    ENGINE("01", "Блок керування двигуном (ECU)", "7E0", "7E8"),
    TRANSMISSION("02", "Автоматична трансмісія (DSG / Tiptronic)", "7E1", "7E9"),
    BRAKES_ABS("03", "Гальмівна система (ABS / ESP)", "713", "77D"),
    HVAC("08", "Кліматична система (HVAC)", "746", "7B0"),
    CENTRAL_ELECTRICS("09", "Блок бортової мережі / BCM", "70E", "778"),
    AIRBAG("15", "Система пасивної безпеки (Airbag)", "715", "77F"),
    INSTRUMENT_CLUSTER("17", "Панель приладів", "714", "77E"),
    CAN_GATEWAY("19", "Діагностичний інтерфейс (Gateway)", "710", "77A"),
    AWD("22", "Повний привід (AWD / Haldex)", "70F", "779"),
    STEERING_ASSIST("44", "Електропідсилювач керма (EPS)", "712", "77C"),
    PARKING_BRAKE("53", "Електронне стоянкове гальмо (EPB)", "752", "7BC"),
    INFOTAINMENT("5F", "Мультимедійна система (MIB)", "773", "7DD");

    companion object {
        fun fromAddress(address: String): VagEcu? =
            entries.find { it.addressHex.equals(address, ignoreCase = true) }
    }
}

/**
 * Ідентифікація блоку керування за стандартом UDS (ISO 14229).
 */
data class EcuIdentity(
    val ecu: VagEcu,
    val partNumber: String,
    val swVersion: String,
    val hwVersion: String? = null,
    val vin: String? = null,
    val longCodingHex: String? = null
)

/**
 * Діагностичний код несправності (DTC).
 */
data class FaultCode(
    val code: String,              // наприклад, "P0101", "U0100"
    val rawBytesHex: String,       // 3 байти в hex, наприклад "010122"
    val failureTypeHex: String,    // Байт типу несправності (Symptom byte)
    val statusByte: Int,           // Байт статусу за UDS ISO 14229-1
    val isConfirmed: Boolean,      // Підтверджена (біт 3: confirmedDTC)
    val isPending: Boolean,        // Тимчасова / очікує підтвердження (біт 2: pendingDTC)
    val isTestFailed: Boolean      // Поточна помилка (біт 0: testFailed)
) {
    companion object {
        /**
         * Декодування 3 байтів UDS DTC у стандартний формат OBD-II (P/C/B/U).
         */
        fun fromUdsBytes(b1: Int, b2: Int, b3: Int, status: Int): FaultCode {
            val prefix = when ((b1 and 0xC0) ushr 6) {
                0 -> "P"
                1 -> "C"
                2 -> "B"
                3 -> "U"
                else -> "P"
            }
            val d1 = (b1 and 0x30) ushr 4
            val d2 = b1 and 0x0F
            val d3 = (b2 and 0xF0) ushr 4
            val d4 = b2 and 0x0F
            val codeStr = "%s%X%X%X%X".format(prefix, d1, d2, d3, d4)
            val rawHex = "%02X%02X%02X".format(b1, b2, b3)
            val failureType = "%02X".format(b3)

            val testFailed = (status and 0x01) != 0
            val pending = (status and 0x04) != 0
            val confirmed = (status and 0x08) != 0

            return FaultCode(
                code = codeStr,
                rawBytesHex = rawHex,
                failureTypeHex = failureType,
                statusByte = status,
                isConfirmed = confirmed,
                isPending = pending,
                isTestFailed = testFailed
            )
        }
    }
}
