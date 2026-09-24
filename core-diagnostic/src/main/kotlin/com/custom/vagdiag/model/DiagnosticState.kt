package com.custom.vagdiag.model

/**
 * Скінченний автомат станів діагностичного процесу (State Machine).
 * Запобігає багам із race conditions, підвисанням Bluetooth та невідомими станами UI.
 */
sealed interface DiagnosticState {
    // 1. Початковий стан очікування
    object Idle : DiagnosticState

    // 2. З'єднання та ініціалізація адаптера
    data class Connecting(val deviceName: String) : DiagnosticState
    data class AdapterInitialized(val adapterVersion: String) : DiagnosticState

    // 3. Автосканування блоків авто (AutoScan)
    data class AutoScanProgress(
        val currentEcu: VagEcu,
        val foundEcus: List<EcuIdentity>,
        val progressPercent: Int
    ) : DiagnosticState

    data class AutoScanCompleted(
        val discoveredEcus: List<EcuIdentity>
    ) : DiagnosticState

    // 4. Зчитування та очищення помилок (DTC)
    data class QueryingDtc(val ecu: VagEcu) : DiagnosticState
    data class DtcScanResults(
        val ecu: VagEcu,
        val faults: List<FaultCode>
    ) : DiagnosticState
    data class DtcCleared(val ecu: VagEcu, val success: Boolean) : DiagnosticState

    // 5. Виконання спеціальних сервісних процедур (EPB, WIV Reset)
    data class ServiceRoutineRunning(
        val routineName: String,
        val stepDescription: String
    ) : DiagnosticState

    data class ServiceRoutineFinished(
        val routineName: String,
        val success: Boolean,
        val message: String
    ) : DiagnosticState

    // 6. Обробка помилок зв'язку та таймаутів
    data class Error(
        val errorType: ErrorType,
        val message: String,
        val canRetry: Boolean
    ) : DiagnosticState
}

enum class ErrorType {
    BLUETOOTH_DISCONNECTED,
    ADAPTER_NO_DATA,
    ADAPTER_UNSUPPORTED,
    ECU_BUSY,
    SECURITY_ACCESS_DENIED,
    TIMEOUT
}
