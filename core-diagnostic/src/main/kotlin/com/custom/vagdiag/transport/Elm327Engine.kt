package com.custom.vagdiag.transport

/**
 * Абстракція фізичного каналу передачі даних.
 * Дозволяє однаково легко працювати з:
 * 1. Реальний Bluetooth Classic SPP сокет
 * 2. Bluetooth Low Energy (BLE) GATT характеристика
 * 3. Мок-адаптер (Unit-тести на ПК без машини)
 */
interface TransportInterface {
    suspend fun open(): Boolean
    suspend fun close()
    suspend fun sendCommand(command: String, timeoutMs: Long = 3000): String
    fun isConnected(): Boolean
}

/**
 * Рушій взаємодії з адаптером ELM327 / STN / vLinker.
 * Відповідає за чергу команд, правильну ініціалізацію та вибір протоколу.
 */
class Elm327Engine(private val transport: TransportInterface) {

    var adapterVersion: String = "Unknown"
        private set

    /**
     * Повна ініціалізація зв'язку з адаптером за специфікацією.
     */
    suspend fun initialize(): Result<String> {
        if (!transport.isConnected()) {
            val opened = transport.open()
            if (!opened) return Result.failure(IllegalStateException("Не вдалося відкрити Bluetooth-канал"))
        }

        // 1. Скидання мікроконтролера
        val resetResp = transport.sendCommand("AT Z")
        adapterVersion = resetResp.lines().firstOrNull { it.contains("ELM") || it.contains("vLinker") || it.contains("OBDLink") }
            ?: "ELM327 Compatible"

        // 2. Оптимізація потоку даних
        transport.sendCommand("AT E0") // Вимкнути відлуння
        transport.sendCommand("AT L0") // Вимкнути linefeed
        transport.sendCommand("AT S0") // Вимкнути пробіли
        transport.sendCommand("AT H1") // Увімкнути показ CAN-заголовків
        transport.sendCommand("AT AL") // Дозволити довгі повідомлення

        // 3. Фіксація протоколу ISO 15765-4 CAN 11-bit / 500k
        val protoResp = transport.sendCommand("AT SP 6")
        if (!protoResp.contains("OK")) {
            return Result.failure(IllegalStateException("Адаптер не підтримує протокол CAN 500k: $protoResp"))
        }

        return Result.success(adapterVersion)
    }

    /**
     * Перемикання фільтрів адаптера на конкретний блок ECU.
     */
    suspend fun setEcuFilter(txCanId: String, rxCanId: String): Boolean {
        val sh = transport.sendCommand("AT SH $txCanId")
        val cra = transport.sendCommand("AT CRA $rxCanId")
        return sh.contains("OK") && cra.contains("OK")
    }

    /**
     * Відправка сирої UDS команди та очищення відповіді.
     */
    suspend fun sendUdsFrame(hexPayload: String): String {
        val raw = transport.sendCommand(hexPayload)
        // Видаляємо сміття (пробіли, символи кінця рядка, знак '>' від ELM327)
        return raw.replace(" ", "")
            .replace("\r", "")
            .replace("\n", "")
            .replace(">", "")
            .trim()
    }
}
