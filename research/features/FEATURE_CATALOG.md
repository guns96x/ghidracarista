# Full Carista Feature Catalog & Applicability Matrix

Total Verified Features: **478**
Generated via clean-room disassembly of `libCarista.so.c` and resource mapping of `resources.arsc`.

---

## Audi Drive Select (ADS) (4 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0004_ADS_AMI_MENU` | **Ads Ami Menu**<br>`car_setting_ads_ami_menu` | `0x5F` (INFOTAINMENT) | UDS | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0005_ADS_ENGINE_MENU` | **Show engine option in ADS menu**<br>`car_setting_ads_engine_menu` | `0x01` (ENGINE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0006_ADS_MODE_RACE` | **Ads Mode Race**<br>`car_setting_ads_mode_race` | `0x5F` (INFOTAINMENT) | UDS | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0007_ADS_STEERING_MENU` | **Show steering option in ADS menu**<br>`car_setting_ads_steering_menu` | `0x5F` (INFOTAINMENT) | UDS | MultipleChoice | Yes / No | `VERIFIED` |

---

## Chassis & Engine (7 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0375_START_STOP` | **Start Stop**<br>`car_setting_start_stop` | `0x19` (CAN_GATEWAY) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0376_START_STOP_DISABLE` | **Disable auto start/stop system**<br>`car_setting_start_stop_disable` | `0x19` (CAN_GATEWAY) | UDS / KWP2000 | MultipleChoice | Enabled / Disabled | `VERIFIED` |
| `FEAT_0377_START_STOP_DISABLE_METHOD_B` | **Disable auto start/stop system (method B)**<br>`car_setting_start_stop_disable_method_b` | `0x19` (CAN_GATEWAY) | UDS / KWP2000 | MultipleChoice | Enabled / Disabled | `VERIFIED` |
| `FEAT_0378_START_STOP_DISABLE_METHOD_C` | **Disable auto start/stop system (method C)**<br>`car_setting_start_stop_disable_method_c` | `0x19` (CAN_GATEWAY) | UDS / KWP2000 | MultipleChoice | Enabled / Disabled | `VERIFIED` |
| `FEAT_0379_START_STOP_INFO` | **Start Stop Info**<br>`car_setting_start_stop_info` | `0x19` (CAN_GATEWAY) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0380_START_STOP_LAST_STATE` | **Auto start/stop: remember last state**<br>`car_setting_start_stop_last_state` | `0x19` (CAN_GATEWAY) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0393_THROTTLE_RESPONSE_BEHAVIOR` | **Throttle response behavior**<br>`car_setting_throttle_response_behavior` | `0x01` (ENGINE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Diagnostics (2 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `DIAG_AUTOSCAN` | **Full Diagnostic Scan (AutoScan)**<br>`autoscan_full_gateway_discovery` | `0x19` (CAN_GATEWAY) | UDS (ISO 14229) / TP2.0 (KWP2000) | Structured Record List | List of installed ECUs with FaultCode models | `VERIFIED` |
| `DIAG_CLEAR_DTC` | **Clear Fault Codes (DTC Reset)**<br>`clear_fault_codes_all_groups` | `All Discovered ECUs` (MULTI_ECU) | UDS / KWP2000 | Command | Execute | `VERIFIED` |

---

## Dings & Warnings (14 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0037_AUTO_HOLD_WITHOUT_SEAT_BELT` | **Auto Hold Without Seat Belt**<br>`car_setting_auto_hold_without_seat_belt` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0134_DISABLE_BRAKE_PAD_WARNING_LIGHT` | **Disable brake pad warning light**<br>`car_setting_disable_brake_pad_warning_light` | `0x03` (BRAKES_ABS) | UDS / KWP2000 | MultipleChoice | Enabled / Disabled | `VERIFIED` |
| `FEAT_0225_ICE_WARNING_THRESHOLD_ON_EXIT` | **Ice warning temperature threshold (when exiting the vehicle)**<br>`car_setting_ice_warning_threshold_on_exit` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0311_POWER_SLIDING_DOORS` | **Power sliding doors**<br>`car_setting_power_sliding_doors` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0337_REQ_SEAT_BELT_WHEN_RELEASING_EPB` | **Require seat belt when releasing parking brake**<br>`car_setting_req_seat_belt_when_releasing_epb` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0342_SEAT_BELT_WARN_TYPE` | **Seat belt warning type**<br>`car_setting_seat_belt_warn_type` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0343_SEAT_BELT_WARNING` | **Seat belt warning**<br>`car_setting_seat_belt_warning` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0344_SEAT_BELT_WARNING_DING_DRIVER` | **Seat belt warning ding (driver)**<br>`car_setting_seat_belt_warning_ding_driver` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0345_SEAT_BELT_WARNING_DING_FRONT_PASSENGER` | **Seat belt warning ding (front passenger)**<br>`car_setting_seat_belt_warning_ding_front_passenger` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0346_SEAT_BELT_WARNING_DING_REAR_PASSENGERS` | **Seat belt warning ding (rear passengers)**<br>`car_setting_seat_belt_warning_ding_rear_passengers` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0347_SEAT_BELT_WARNING_EXPERIMENTAL` | **Seat Belt Warning Experimental**<br>`car_setting_seat_belt_warning_experimental` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0351_SEATBELT_WARNING_DING_REAR_CENTER` | **Seat belt warning ding (rear center passenger)**<br>`car_setting_seatbelt_warning_ding_rear_center` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0352_SEATBELT_WARNING_DING_REAR_LEFT` | **Seat belt warning ding (rear left passenger)**<br>`car_setting_seatbelt_warning_ding_rear_left` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0353_SEATBELT_WARNING_DING_REAR_RIGHT` | **Seat belt warning ding (rear right passenger)**<br>`car_setting_seatbelt_warning_ding_rear_right` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Driver Assist (8 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0003_ACC_OVERTAKING_ON_RIGHT` | **Adaptive cruise control overtaking on the right**<br>`car_setting_acc_overtaking_on_right` | `0x13` (AUTO_DIST_REG) | UDS | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0407_TRAFFIC_SIGN_RECOGNITION_STEP_1` | **Traffic Sign Recognition Step 1**<br>`car_setting_traffic_sign_recognition_step_1` | `0xA5` (FRONT_SENSORS) | UDS | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0408_TRAFFIC_SIGN_RECOGNITION_STEP_2` | **Traffic Sign Recognition Step 2**<br>`car_setting_traffic_sign_recognition_step_2` | `0xA5` (FRONT_SENSORS) | UDS | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0409_TRAFFIC_SIGN_RECOGNITION_STEP_3` | **Traffic Sign Recognition Step 3**<br>`car_setting_traffic_sign_recognition_step_3` | `0xA5` (FRONT_SENSORS) | UDS | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0410_TRAFFIC_SIGN_RECOGNITION_STEP_4` | **Traffic Sign Recognition Step 4**<br>`car_setting_traffic_sign_recognition_step_4` | `0xA5` (FRONT_SENSORS) | UDS | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0411_TRAFFIC_SIGN_RECOGNITION_STEP_5` | **Traffic Sign Recognition Step 5**<br>`car_setting_traffic_sign_recognition_step_5` | `0xA5` (FRONT_SENSORS) | UDS | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0412_TRAFFIC_SIGN_RECOGNITION_STEP_6` | **Traffic Sign Recognition Step 6**<br>`car_setting_traffic_sign_recognition_step_6` | `0xA5` (FRONT_SENSORS) | UDS | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0413_TRAFFIC_SIGN_RECOGNITION_THRESHOLD` | **Traffic Sign Recognition Threshold**<br>`car_setting_traffic_sign_recognition_threshold` | `0xA5` (FRONT_SENSORS) | UDS | Numerical | Range / Percentage / Value steps | `VERIFIED` |

---

## Heater & A/C (2 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0002_AC_REFRIGERANT_SHORTAGE_CHECK` | **Ac Refrigerant Shortage Check**<br>`car_setting_ac_refrigerant_shortage_check` | `0x01` (ENGINE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0355_SHOW_BLOWER_SPEED_IN_AUTO` | **Show A/C blower speed when in AUTO**<br>`car_setting_show_blower_speed_in_auto` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |

---

## Instruments: Displays & Nav (15 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0139_DISPLAY_GEAR_IN_INSTRUMENT_CLUSTER` | **Display current gear in dash**<br>`car_setting_display_gear_in_instrument_cluster` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0206_GAUGE_ARROW_OFFSET` | **Gauge arrow offset**<br>`car_setting_gauge_arrow_offset` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0207_GAUGE_ARROW_SENSITIVITY` | **Gauge arrow response sensitivity**<br>`car_setting_gauge_arrow_sensitivity` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0227_INSTR_NEEDLE_SWEEP` | **Gauge needle sweep at startup**<br>`car_setting_instr_needle_sweep` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0228_INSTR_NEEDLE_SWEEP_LAP_COUNTER_UPSHIFT_INDICATOR` | **Instr Needle Sweep Lap Counter Upshift Indicator**<br>`car_setting_instr_needle_sweep_lap_counter_upshift_indicator` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0229_INSTR_NEEDLE_SWEEP_LAP_TIMER_UPSHIFT_INDICATOR_SOME_MODULES_ONLY` | **Instr Needle Sweep Lap Timer Upshift Indicator Some Modules Only**<br>`car_setting_instr_needle_sweep_lap_timer_upshift_indicator_some_modules_only` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0234_INSTRUCTION_GAUGE_ARROW_OFFSET` | **Larger values move the arrow offset to the left, smaller values move it to the right.**<br>`car_setting_instruction_gauge_arrow_offset` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0244_INSTRUMENT_CLUSTER_LCD_BACKGROUND` | **Instrument cluster LCD background**<br>`car_setting_instrument_cluster_lcd_background` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0248_INTRO_CLUSTER_GAUGE_CONFIG` | **Allows you to configure the small gauge on the right side of the instrument cluster. Please note that this tool may not be supported on diesel vehicles.**<br>`car_setting_intro_cluster_gauge_config` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0254_LAP_COUNTER_NEEDLE_SWEEP` | **Lap Counter Needle Sweep**<br>`car_setting_lap_counter_needle_sweep` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0255_LAP_TIMER_OIL_TEMP` | **Lap timer and oil temperature in dashboard**<br>`car_setting_lap_timer_oil_temp` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0285_OIL_TEMP_DISPLAY` | **Oil temperature display**<br>`car_setting_oil_temp_display` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0374_START_SCREEN_INSTRUMENT_CLUSTER` | **Start screen logo (instrument cluster)**<br>`car_setting_start_screen_instrument_cluster` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0434_UPSHIFT_INDICATOR_NEEDLE_SWEEP` | **Upshift Indicator Needle Sweep**<br>`car_setting_upshift_indicator_needle_sweep` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0457_VIRTUAL_INSTRUMENT_CLUSTER_THEME` | **Virtual instrument cluster theme**<br>`car_setting_virtual_instrument_cluster_theme` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Instruments: Language & Units (6 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0252_LANGUAGE` | **Instrument cluster language**<br>`car_setting_language` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0427_UNITS_GALLONS_UK` | **Gallons (UK)**<br>`car_setting_units_gallons_uk` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0428_UNITS_GALLONS_US` | **Gallons (US)**<br>`car_setting_units_gallons_us` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0429_UNITS_L_100_KM` | **l/100km**<br>`car_setting_units_l_100_km` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0430_UNITS_L_HOUR` | **l/h**<br>`car_setting_units_l_hour` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0431_UNITS_PRESSURE` | **Pressure display units**<br>`car_setting_units_pressure` | `0x17` (INSTRUMENT_CLUSTER) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Lights: Automatic (4 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0036_AUTO_HEADLIGHTS_ABOVE_140_KPH` | **Auto Headlights Above 140 Kph**<br>`car_setting_auto_headlights_above_140_kph` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0218_HIGHWAY_LIGHTS` | **Highway lights**<br>`car_setting_highway_lights` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0235_INSTRUCTION_HIGHWAY_LIGHTS` | **The effect of this customization depends on the front lights installed:
Xenon plus: high beams tilt up above 140 km/h (90 mph).
Others: low beams turn on automatically above 140 km/h (90 mph).**<br>`car_setting_instruction_highway_lights` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0318_RAIN_LIGHT_SENSOR` | **Rain/light sensor**<br>`car_setting_rain_light_sensor` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Lights: Bulb Checks (2 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0087_BULB_CHECK_ALL_LIGHTS` | **Bulb Check All Lights**<br>`car_setting_bulb_check_all_lights` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0089_BULB_CHECK_LICENSE_PLATE_LIGHTS` | **Bulb check: license plate lights**<br>`car_setting_bulb_check_license_plate_lights` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Lights: Coming/Leaving Home (8 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0115_COMING_HOME` | **Coming-home lights**<br>`car_setting_coming_home` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0116_COMING_HOME_DURATION` | **Coming-home lights duration**<br>`car_setting_coming_home_duration` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0117_COMING_HOME_MODE` | **Coming-home lights mode**<br>`car_setting_coming_home_mode` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0118_COMING_HOME_REQ_RLS` | **Coming-home lights (req. auto headlights)**<br>`car_setting_coming_home_req_rls` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0119_COMING_LEAVING_HOME_OUTPUT` | **Coming/leaving-home lights use…**<br>`car_setting_coming_leaving_home_output` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0256_LEAVING_HOME` | **Leaving-home lights**<br>`car_setting_leaving_home` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0257_LEAVING_HOME_DURATION` | **Leaving-home lights duration**<br>`car_setting_leaving_home_duration` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0258_LEAVING_HOME_REQ_RLS` | **Leaving-home lights (req. auto headlights)**<br>`car_setting_leaving_home_req_rls` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Lights: Daytime Running Lights (DRL) (28 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0088_BULB_CHECK_DAYTIME_RUNNING_LIGHTS_LEFT_LIGHTS` | **Bulb check: daytime running lights (left)**<br>`car_setting_bulb_check_daytime_running_lights_left_lights` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0127_DIAGNOSTICS_DRL` | **Diagnostics Drl**<br>`car_setting_diagnostics_drl` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0147_DRL` | **Daytime running lights**<br>`car_setting_drl` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0148_DRL_BRIGHTNESS` | **Daytime running lights (DRL) brightness**<br>`car_setting_drl_brightness` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0149_DRL_BRIGHTNESS_WHEN_HEADLIGHTS_ARE_ON` | **Daytime running lights (DRL) brightness when headlights are on**<br>`car_setting_drl_brightness_when_headlights_are_on` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0150_DRL_BRIGHTNESS_WHEN_HEADLIGHTS_ARE_ON_LEFT` | **Drl Brightness When Headlights Are On Left**<br>`car_setting_drl_brightness_when_headlights_are_on_left` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0151_DRL_BRIGHTNESS_WHEN_HEADLIGHTS_ARE_ON_RIGHT` | **Drl Brightness When Headlights Are On Right**<br>`car_setting_drl_brightness_when_headlights_are_on_right` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0152_DRL_INDICATOR` | **Drl Indicator**<br>`car_setting_drl_indicator` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0153_DRL_ONLY_IN_AUTO_MODE` | **Daytime running lights on only when switch is set to AUTO**<br>`car_setting_drl_only_in_auto_mode` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0154_DRL_OVERRIDE` | **Drl Override**<br>`car_setting_drl_override` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0155_DRL_VIA` | **Daytime running lights (DRL) use…**<br>`car_setting_drl_via` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0156_DRL_VIA_FOGS` | **Use fog lights as daytime running lights**<br>`car_setting_drl_via_fogs` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0157_DRL_VIA_FRONT_LEFT_TURN_SIGNAL_STEP_1` | **Drl Via Front Left Turn Signal Step 1**<br>`car_setting_drl_via_front_left_turn_signal_step_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0158_DRL_VIA_FRONT_LEFT_TURN_SIGNAL_STEP_2` | **Drl Via Front Left Turn Signal Step 2**<br>`car_setting_drl_via_front_left_turn_signal_step_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0159_DRL_VIA_FRONT_LEFT_TURN_SIGNAL_STEP_3` | **Drl Via Front Left Turn Signal Step 3**<br>`car_setting_drl_via_front_left_turn_signal_step_3` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0160_DRL_VIA_FRONT_LEFT_TURN_SIGNAL_STEP_4` | **Drl Via Front Left Turn Signal Step 4**<br>`car_setting_drl_via_front_left_turn_signal_step_4` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0161_DRL_VIA_FRONT_MARKERS` | **Drl Via Front Markers**<br>`car_setting_drl_via_front_markers` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0162_DRL_VIA_FRONT_RIGHT_TURN_SIGNAL_STEP_1` | **Drl Via Front Right Turn Signal Step 1**<br>`car_setting_drl_via_front_right_turn_signal_step_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0163_DRL_VIA_FRONT_RIGHT_TURN_SIGNAL_STEP_2` | **Drl Via Front Right Turn Signal Step 2**<br>`car_setting_drl_via_front_right_turn_signal_step_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0164_DRL_VIA_FRONT_RIGHT_TURN_SIGNAL_STEP_3` | **Drl Via Front Right Turn Signal Step 3**<br>`car_setting_drl_via_front_right_turn_signal_step_3` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0165_DRL_VIA_FRONT_RIGHT_TURN_SIGNAL_STEP_4` | **Drl Via Front Right Turn Signal Step 4**<br>`car_setting_drl_via_front_right_turn_signal_step_4` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0166_DRL_VIA_LASH_LEFT_BRIGHTNESS` | **Drl Via Lash Left Brightness**<br>`car_setting_drl_via_lash_left_brightness` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0167_DRL_VIA_LASH_RIGHT_BRIGHTNESS` | **Drl Via Lash Right Brightness**<br>`car_setting_drl_via_lash_right_brightness` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0168_DRL_VIA_SEPARATE_LIGHTS_EXPERIMENTAL` | **Drl Via Separate Lights Experimental**<br>`car_setting_drl_via_separate_lights_experimental` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0260_LED_DAYTIME_RUNNING_LIGHTS` | **LED lights**<br>`car_setting_led_daytime_running_lights` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0340_SCANDINAVIAN_DRL` | **Scandinavian DRL: daytime running lights activate taillights and parking lights**<br>`car_setting_scandinavian_drl` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0421_TURN_OFF_DRL_WITH_PARKING_BRAKE` | **Turn off daytime running lights when parking brake is on**<br>`car_setting_turn_off_drl_with_parking_brake` | `0x53` (PARKING_BRAKE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0422_TURN_OFF_DRL_WITH_TURN_SIGNAL` | **Turn off daytime running lights ("wink") when turn signal is on**<br>`car_setting_turn_off_drl_with_turn_signal` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Lights: Exterior (19 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0112_COMFORT_TURN_SIGNAL` | **Lane-change turn signal auto-flasher**<br>`car_setting_comfort_turn_signal` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0113_COMFORT_TURN_SIGNAL_COUNT` | **Lane-change turn signal auto-flasher count**<br>`car_setting_comfort_turn_signal_count` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0114_COMFORT_TURN_SIGNAL_IN_MMI` | **Comfort Turn Signal In Mmi**<br>`car_setting_comfort_turn_signal_in_mmi` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0121_CORNERING_LIGHTS_VIA_FOGS` | **Cornering lights (using fog lights)**<br>`car_setting_cornering_lights_via_fogs` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0122_CORNERING_LIGHTS_VIA_FOGS_LEFT` | **Left cornering light (using fog light)**<br>`car_setting_cornering_lights_via_fogs_left` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0128_DIAGNOSTICS_FOG_LIGHTS` | **Diagnostics Fog Lights**<br>`car_setting_diagnostics_fog_lights` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0129_DIAGNOSTICS_FOG_LIGHTS_REAR` | **Diagnostics Fog Lights Rear**<br>`car_setting_diagnostics_fog_lights_rear` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0130_DIAGNOSTICS_HIGH_BEAMS` | **Diagnostics High Beams**<br>`car_setting_diagnostics_high_beams` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0131_DIAGNOSTICS_LOW_BEAMS` | **Diagnostics Low Beams**<br>`car_setting_diagnostics_low_beams` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0132_DIAGNOSTICS_TAIL_LIGHTS` | **Diagnostics Tail Lights**<br>`car_setting_diagnostics_tail_lights` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0133_DIAGNOSTICS_TURN_SIGNALS` | **Diagnostics Turn Signals**<br>`car_setting_diagnostics_turn_signals` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0180_EMERGENCY_BRAKE_FLASHING_VIA_TURN_SIGNALS` | **Flash hazard lights in emergency stopping**<br>`car_setting_emergency_brake_flashing_via_turn_signals` | `0x03` (BRAKES_ABS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0217_HIGH_BEAM_ASSIST_AUTO` | **High beam assist auto**<br>`car_setting_high_beam_assist_auto` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0240_INSTRUCTION_REQUIRES_HIGHLINE_TAIL_LIGHTS` | **Instruction Requires Highline Tail Lights**<br>`car_setting_instruction_requires_highline_tail_lights` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0356_SIDE_MARKER_BRIGHTNESS` | **Side marker brightness**<br>`car_setting_side_marker_brightness` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0357_SIDE_MARKER_PACE_CAR_LEFT` | **"Pace-car" turn signals (left)**<br>`car_setting_side_marker_pace_car_left` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0358_SIDE_MARKER_PACE_CAR_RIGHT` | **"Pace-car" turn signals (right)**<br>`car_setting_side_marker_pace_car_right` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0423_TURN_OFF_FOGS_WITH_HIGH_BEAM` | **Turn off front fog lights when high beams are on**<br>`car_setting_turn_off_fogs_with_high_beam` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0424_TURN_SIGNAL_CLICK_VOLUME` | **Turn signal click volume**<br>`car_setting_turn_signal_click_volume` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |

---

## Lights: Interior (15 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0015_AMBIENT_CENTRAL_CONSOLE_LIGHTING_MULTICOLOR` | **Ambient Central Console Lighting Multicolor**<br>`car_setting_ambient_central_console_lighting_multicolor` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0016_AMBIENT_COCKPIT_LIGHTING_MULTICOLOR` | **Ambient Cockpit Lighting Multicolor**<br>`car_setting_ambient_cockpit_lighting_multicolor` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0017_AMBIENT_DOOR_LIGHTING_MULTICOLOR` | **Ambient Door Lighting Multicolor**<br>`car_setting_ambient_door_lighting_multicolor` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0018_AMBIENT_LIGHTING_COLOR_CHOICE_VIA_DRIVING_MODE` | **Ambient Lighting Color Choice Via Driving Mode**<br>`car_setting_ambient_lighting_color_choice_via_driving_mode` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0019_AMBIENT_LIGHTING_COLOR_CHOICE_VIA_MENU` | **Ambient Lighting Color Choice Via Menu**<br>`car_setting_ambient_lighting_color_choice_via_menu` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0020_AMBIENT_LIGHTING_MENU` | **Ambient Lighting Menu**<br>`car_setting_ambient_lighting_menu` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0021_AMBIENT_LIGHTING_MENU_ADD_OFF_SWITCH` | **Ambient Lighting Menu Add Off Switch**<br>`car_setting_ambient_lighting_menu_add_off_switch` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0022_AMBIENT_ROOF_LIGHTING_MULTICOLOR` | **Ambient Roof Lighting Multicolor**<br>`car_setting_ambient_roof_lighting_multicolor` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0023_AMBIENT_SPEAKERS_LIGHTING_MULTICOLOR` | **Ambient Speakers Lighting Multicolor**<br>`car_setting_ambient_speakers_lighting_multicolor` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0024_AMBIENT_SUNROOF_LIGHTING_MULTICOLOR` | **Ambient Sunroof Lighting Multicolor**<br>`car_setting_ambient_sunroof_lighting_multicolor` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0025_AMBIENT_TEMPERATURE_DISPLAY` | **Ambient temperature display**<br>`car_setting_ambient_temperature_display` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0196_FADING_INTERIOR_LIGHTS` | **Interior lights gradually fade in/out when exterior lights are turned on/off**<br>`car_setting_fading_interior_lights` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0197_FOOTWELL_LIGHTS_BRIGHTNESS_NO_EXT_LIGHT_PACK` | **Footwell lights brightness (for cars without extended lighting package)**<br>`car_setting_footwell_lights_brightness_no_ext_light_pack` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0198_FOOTWELL_LIGHTS_WITH_INSTRUMENT_LIGHTS` | **Keep interior footwell lights on when driving with headlights on**<br>`car_setting_footwell_lights_with_instrument_lights` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0246_INTERIOR_LIGHTS_DISCO_MODE` | **Interior Lights Disco Mode**<br>`car_setting_interior_lights_disco_mode` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Locking: Automatic (5 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0039_AUTO_LOCK_WHEN_MOVING` | **Auto-lock doors when moving**<br>`car_setting_auto_lock_when_moving` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0042_AUTO_UNLOCK` | **Auto-unlock doors when key is taken out of ignition**<br>`car_setting_auto_unlock` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0043_AUTO_UNLOCK_DOORS_AFTER_CRASH` | **Auto Unlock Doors After Crash**<br>`car_setting_auto_unlock_doors_after_crash` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0044_AUTO_UNLOCK_PARKED` | **Auto-unlock doors when shifting into park (P)**<br>`car_setting_auto_unlock_parked` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0045_AUTO_UNLOCK_WHEN_SMART_KEY_NEAR` | **Auto Unlock When Smart Key Near**<br>`car_setting_auto_unlock_when_smart_key_near` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Locking: Beep & Blink (18 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0012_ALLOW_CONFIG_BEEP_ON_LOCK_UNLOCK_REMOTE` | **Allow configuring beep when locking/unlocking**<br>`car_setting_allow_config_beep_on_lock_unlock_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Enabled / Disabled | `VERIFIED` |
| `FEAT_0071_BEEP_ON_ALARM_ARMED` | **Beep when alarm is armed**<br>`car_setting_beep_on_alarm_armed` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0072_BEEP_ON_ALARM_ARMED_ENGINE_RUNNING` | **Beep On Alarm Armed Engine Running**<br>`car_setting_beep_on_alarm_armed_engine_running` | `0x01` (ENGINE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0073_BEEP_ON_LOCK_KEY` | **Beep when locking with key**<br>`car_setting_beep_on_lock_key` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0074_BEEP_ON_LOCK_REMOTE` | **Beep when locking with remote**<br>`car_setting_beep_on_lock_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0075_BEEP_ON_LOCK_UNLOCK_REMOTE_DURATION_HORN_ONLY` | **Duration of beep when locking/unlocking with remote (horn only)**<br>`car_setting_beep_on_lock_unlock_remote_duration_horn_only` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0076_BEEP_ON_LOCK_UNLOCK_TYPE` | **Beep when locking/unlocking doors comes from the…**<br>`car_setting_beep_on_lock_unlock_type` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0077_BEEP_ON_UNLOCK_REMOTE` | **Beep when unlocking with remote**<br>`car_setting_beep_on_unlock_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0080_BLINK_ON_LOCK_KEY` | **Blink turn signals when locking with key**<br>`car_setting_blink_on_lock_key` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0081_BLINK_ON_LOCK_REMOTE` | **Blink turn signals when locking with remote**<br>`car_setting_blink_on_lock_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0082_BLINK_ON_LOCK_UNLOCK_REMOTE` | **Blink turn signals when locking/unlocking with remote**<br>`car_setting_blink_on_lock_unlock_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0083_BLINK_ON_UNLOCK_KEY` | **Blink turn signals when unlocking with key**<br>`car_setting_blink_on_unlock_key` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0084_BLINK_ON_UNLOCK_REMOTE` | **Blink turn signals when unlocking with remote**<br>`car_setting_blink_on_unlock_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0101_COMFORT_FUNCTION_BLINK` | **Blink turn signals when done closing windows via remote**<br>`car_setting_comfort_function_blink` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0222_HORN_BEEPS_COUNT_LOCK` | **Horn Beeps Count Lock**<br>`car_setting_horn_beeps_count_lock` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0223_HORN_BEEPS_COUNT_UNLOCK` | **Horn Beeps Count Unlock**<br>`car_setting_horn_beeps_count_unlock` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0304_PCS_BEEP` | **Pcs Beep**<br>`car_setting_pcs_beep` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0339_REVERSE_BEEP` | **Reverse gear beep**<br>`car_setting_reverse_beep` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Locking: Doors & Alarm (6 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0011_ALARM` | **Alarm system**<br>`car_setting_alarm` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0092_CENTRAL_LOCKING_BUTTON` | **Central Locking Button**<br>`car_setting_central_locking_button` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0301_PCS_ALARM_LAST_STATE` | **Default distance for Pre-Collision System (PCS) alarm when the PCS switch is turned off and back on**<br>`car_setting_pcs_alarm_last_state` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0302_PCS_ALARM_OFF_WHEN_IGNITION_ON` | **Default distance for Pre-Collision System (PCS) alarm when the ignition is turned on with the PCS switch off**<br>`car_setting_pcs_alarm_off_when_ignition_on` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0303_PCS_ALARM_ON_WHEN_IGNITION_ON` | **Default distance for Pre-Collision System (PCS) alarm when the ignition is turned on with the PCS switch on**<br>`car_setting_pcs_alarm_on_when_ignition_on` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0359_SINGLE_DOOR_LOCK_REMOTE` | **Unlock doors via remote**<br>`car_setting_single_door_lock_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Locking: Smart Key (KESSY) (5 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0172_EASY_ENTRY_EXIT_OVERALL` | **Enable settings for easy entry/exit in MMI**<br>`car_setting_easy_entry_exit_overall` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0173_EASY_ENTRY_EXIT_REQ_MEMORY_SEATS` | **Easy entry/exit (req. memory seats)**<br>`car_setting_easy_entry_exit_req_memory_seats` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0174_EASY_ENTRY_EXIT_STEERING_WHEEL_RETRACT_MENU` | **Easy Entry Exit Steering Wheel Retract Menu**<br>`car_setting_easy_entry_exit_steering_wheel_retract_menu` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0233_INSTRUCTION_EASY_ENTRY_EXIT_B9` | **Instruction Easy Entry Exit B9**<br>`car_setting_instruction_easy_entry_exit_b9` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0251_KEYLESS_ENTRY_IN_INFOTAINMENT` | **Keyless Entry In Infotainment**<br>`car_setting_keyless_entry_in_infotainment` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Mirrors (28 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0027_AUTO_FOLD_MIRROR_PASSENGER` | **Auto fold passenger's side-view mirror (req. power folding mirrors)**<br>`car_setting_auto_fold_mirror_passenger` | `0x52` (PASSENGER_DOOR) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0028_AUTO_FOLD_MIRRORS` | **Auto fold side-view mirrors (req. power folding mirrors)**<br>`car_setting_auto_fold_mirrors` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0029_AUTO_FOLD_MIRRORS_DRIVER_STEP_1` | **Auto fold driver-side mirror (req. power folding mirrors) (step 1 of 2)**<br>`car_setting_auto_fold_mirrors_driver_step_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0030_AUTO_FOLD_MIRRORS_DRIVER_STEP_2` | **Auto fold driver-side mirror (req. power folding mirrors) (step 2 of 2)**<br>`car_setting_auto_fold_mirrors_driver_step_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0031_AUTO_FOLD_MIRRORS_IN_INFOTAINMENT` | **Allow configuring auto-folding mirrors in infotainment**<br>`car_setting_auto_fold_mirrors_in_infotainment` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0032_AUTO_FOLD_MIRRORS_OVERALL` | **Allow auto-folding mirrors**<br>`car_setting_auto_fold_mirrors_overall` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0033_AUTO_FOLD_MIRRORS_PASSENGER_STEP_1` | **Auto fold passenger-side mirror (req. power folding mirrors) (step 1 of 2)**<br>`car_setting_auto_fold_mirrors_passenger_step_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0034_AUTO_FOLD_MIRRORS_PASSENGER_STEP_2` | **Auto fold passenger-side mirror (req. power folding mirrors) (step 2 of 2)**<br>`car_setting_auto_fold_mirrors_passenger_step_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0035_AUTO_FOLD_MIRRORS_REMOTE_MODE` | **Auto fold mirrors via…**<br>`car_setting_auto_fold_mirrors_remote_mode` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0041_AUTO_UNFOLD_MIRRORS` | **Auto unfold side-view mirrors**<br>`car_setting_auto_unfold_mirrors` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0214_HEATED_WINDSHIELD_JETS_AND_MIRRORS` | **Heated Windshield Jets And Mirrors**<br>`car_setting_heated_windshield_jets_and_mirrors` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0236_INSTRUCTION_LOWER_MIRROR_WITH_SWITCH_PASS` | **Note that this works only if your power mirror switch is set to control the passenger-side mirror.**<br>`car_setting_instruction_lower_mirror_with_switch_pass` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0250_JETS_AND_MIRRORS` | **Jets And Mirrors**<br>`car_setting_jets_and_mirrors` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0265_LOWER_DRIVER_MIRROR_IN_REVERSE` | **Lower driver-side mirror when in reverse gear**<br>`car_setting_lower_driver_mirror_in_reverse` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0266_LOWER_DRIVER_MIRROR_IN_REVERSE_STEP_3` | **Lower Driver Mirror In Reverse Step 3**<br>`car_setting_lower_driver_mirror_in_reverse_step_3` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0267_LOWER_MIRROR_IN_REVERSE` | **Lower passenger-side mirror when in reverse gear**<br>`car_setting_lower_mirror_in_reverse` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0268_LOWER_MIRROR_IN_REVERSE_GLOBAL` | **Allow lowering passenger-side mirror when in reverse gear**<br>`car_setting_lower_mirror_in_reverse_global` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0269_LOWER_MIRROR_IN_REVERSE_REQ_MEMORY_SEATS` | **Lower passenger-side mirror when in reverse gear (req. memory seats)**<br>`car_setting_lower_mirror_in_reverse_req_memory_seats` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0271_MEMORY_FOR_LOWERING_DRIVER_MIRROR_IN_REVERSE` | **Memory For Lowering Driver Mirror In Reverse**<br>`car_setting_memory_for_lowering_driver_mirror_in_reverse` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0272_MEMORY_FOR_LOWERING_DRIVER_MIRROR_IN_REVERSE_STEP_1` | **Memory For Lowering Driver Mirror In Reverse Step 1**<br>`car_setting_memory_for_lowering_driver_mirror_in_reverse_step_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0273_MEMORY_FOR_LOWERING_DRIVER_MIRROR_IN_REVERSE_STEP_2` | **Memory For Lowering Driver Mirror In Reverse Step 2**<br>`car_setting_memory_for_lowering_driver_mirror_in_reverse_step_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0274_MEMORY_FOR_LOWERING_MIRROR_IN_REVERSE` | **Remember position when lowering passenger-side mirror in reverse gear**<br>`car_setting_memory_for_lowering_mirror_in_reverse` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0275_MEMORY_FOR_LOWERING_MIRROR_IN_REVERSE_STEP_1` | **Memory For Lowering Mirror In Reverse Step 1**<br>`car_setting_memory_for_lowering_mirror_in_reverse_step_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0276_MEMORY_FOR_LOWERING_MIRROR_IN_REVERSE_STEP_2` | **Memory For Lowering Mirror In Reverse Step 2**<br>`car_setting_memory_for_lowering_mirror_in_reverse_step_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0278_MIRROR_ADJ_IN_DASH` | **Mirror Adj In Dash**<br>`car_setting_mirror_adj_in_dash` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0280_MIRROR_SYNCHRONOUS` | **Synchronous mirror adjustment**<br>`car_setting_mirror_synchronous` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0316_PUDDLE_LIGHTS_WHILE_DRIVER_MIRROR_FOLDING` | **Puddle lights while driver-side mirror is folding**<br>`car_setting_puddle_lights_while_driver_mirror_folding` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0317_PUDDLE_LIGHTS_WHILE_PASS_MIRROR_FOLDING` | **Puddle lights while passenger-side mirror is folding**<br>`car_setting_puddle_lights_while_pass_mirror_folding` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Other (234 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0001_TODO` | **Todo**<br>`car_setting_TODO` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0008_AGM_70_AH_600_CCA_H6` | **AGM 70Ah 600CCA H6**<br>`car_setting_agm_70_ah_600_cca_h6` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0009_AGM_80_AH_700_CCA_H7` | **AGM 80Ah 700CCA H7**<br>`car_setting_agm_80_ah_700_cca_h7` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0010_AGM_80_AH_700_CCA_T7` | **AGM 80Ah 700CCA T7**<br>`car_setting_agm_80_ah_700_cca_t7` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0013_ALLOW_CONFIG_SOUND_ON_LOCK_UNLOCK_REMOTE` | **Allow Config Sound On Lock Unlock Remote**<br>`car_setting_allow_config_sound_on_lock_unlock_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Enabled / Disabled | `VERIFIED` |
| `FEAT_0026_ANTI_KEY_LOCK_FUNCTION` | **Reminder if key is still in the vehicle**<br>`car_setting_anti_key_lock_function` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0038_AUTO_LIGHTS_SENSITIVITY` | **Auto headlights activation threshold**<br>`car_setting_auto_lights_sensitivity` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0040_AUTO_RELOCK_TIME` | **Re-lock doors automatically if you unlock, but don't open a door within…**<br>`car_setting_auto_relock_time` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0046_AUTOMATIC_DRIVEAWAY_AFTER_SHORT_STOP_STEP_1` | **Automatic Driveaway After Short Stop Step 1**<br>`car_setting_automatic_driveaway_after_short_stop_step_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0047_AUTOMATIC_DRIVEAWAY_AFTER_SHORT_STOP_STEP_2` | **Automatic Driveaway After Short Stop Step 2**<br>`car_setting_automatic_driveaway_after_short_stop_step_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0048_AUX_HEATER_UNLOCKED` | **Aux. heater unlocked**<br>`car_setting_aux_heater_unlocked` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0049_BATTERY_105AH_AGM` | **105 Ah AGM**<br>`car_setting_battery_105ah_agm` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0050_BATTERY_110AH` | **110 Ah**<br>`car_setting_battery_110ah` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0051_BATTERY_20AH` | **20 Ah**<br>`car_setting_battery_20ah` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0052_BATTERY_40AH` | **40 Ah**<br>`car_setting_battery_40ah` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0053_BATTERY_40AH_AGM` | **40 Ah AGM**<br>`car_setting_battery_40ah_agm` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0054_BATTERY_46AH` | **46 Ah**<br>`car_setting_battery_46ah` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0055_BATTERY_55AH` | **55 Ah**<br>`car_setting_battery_55ah` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0056_BATTERY_55AH_AGM` | **55 Ah AGM**<br>`car_setting_battery_55ah_agm` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0057_BATTERY_60AH_AGM` | **60 Ah AGM**<br>`car_setting_battery_60ah_agm` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0058_BATTERY_70AH` | **70 Ah**<br>`car_setting_battery_70ah` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0059_BATTERY_70AH_AGM` | **70 Ah AGM**<br>`car_setting_battery_70ah_agm` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0060_BATTERY_70AH_EFB` | **70 Ah EFB**<br>`car_setting_battery_70ah_efb` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0061_BATTERY_80AH` | **80 Ah**<br>`car_setting_battery_80ah` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0062_BATTERY_80AH_AGM` | **80 Ah AGM**<br>`car_setting_battery_80ah_agm` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0063_BATTERY_80AH_EFB` | **80 Ah EFB**<br>`car_setting_battery_80ah_efb` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0064_BATTERY_90AH` | **90 Ah**<br>`car_setting_battery_90ah` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0065_BATTERY_90AH_AGM` | **90 Ah AGM**<br>`car_setting_battery_90ah_agm` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0066_BATTERY_CHARGE_DISPLAY_REQ_INSTR_SUPPORT` | **Battery Charge Display Req Instr Support**<br>`car_setting_battery_charge_display_req_instr_support` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0068_BATTERY_TECHNOLOGY` | **Battery technology**<br>`car_setting_battery_technology` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0069_BATTERY_TECHNOLOGY_AGM` | **AGM**<br>`car_setting_battery_technology_agm` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0070_BATTERY_TECHNOLOGY_WET` | **Wet (lead-acid)**<br>`car_setting_battery_technology_wet` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0078_BLIND_SPOT_INDICATORS_BRIGHTNESS` | **Blind spot indicators brightness**<br>`car_setting_blind_spot_indicators_brightness` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0079_BLINDSPOT_VOLUME` | **Blind Spot Monitoring (BSM) volume**<br>`car_setting_blindspot_volume` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0085_BRAKE_ASSIST_STRENGTH` | **Power brakes strength**<br>`car_setting_brake_assist_strength` | `0x03` (BRAKES_ABS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0086_BRAKE_DISC_DRYING` | **Brake Disc Drying**<br>`car_setting_brake_disc_drying` | `0x03` (BRAKES_ABS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0090_CATEGORY_` | **Category **<br>`car_setting_category_` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0091_CATEGORY_OTHER` | **Other**<br>`car_setting_category_other` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0093_CHANNEL_195` | **Channel 195**<br>`car_setting_channel_195` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0094_CHANNEL_196` | **Channel 196**<br>`car_setting_channel_196` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0095_CHANNEL_197` | **Channel 197**<br>`car_setting_channel_197` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0096_CHANNEL_198` | **Channel 198**<br>`car_setting_channel_198` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0097_COMFORT_CLOSE_KEY` | **Close windows and sunroof by turning and holding key in door lock**<br>`car_setting_comfort_close_key` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0102_COMFORT_FUNCTION_REMOTE` | **Open/close windows and sunroof via long-press on remote**<br>`car_setting_comfort_function_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0104_COMFORT_OPEN_CONVERTIBLE_KEY` | **Open convertible roof by turning and holding key in door lock**<br>`car_setting_comfort_open_convertible_key` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0105_COMFORT_OPEN_CONVERTIBLE_REMOTE` | **Open convertible roof via long-press on remote**<br>`car_setting_comfort_open_convertible_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0106_COMFORT_OPEN_KEY` | **Open windows and sunroof by turning and holding key in door lock**<br>`car_setting_comfort_open_key` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0107_COMFORT_OPEN_REMOTE` | **Open windows and sunroof via long-press on remote**<br>`car_setting_comfort_open_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0111_COMFORT_REAR_WIPING` | **Auto-enable rear wiper when front wipers on and reverse gear engaged**<br>`car_setting_comfort_rear_wiping` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0120_CONTINUOUS` | **Continuous**<br>`car_setting_continuous` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0123_COUNTRY` | **Instrument cluster region (affects ext. lights too)**<br>`car_setting_country` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0124_CRASH_LIGHTS_DOUBLE_IMPULSE` | **Crash Lights Double Impulse**<br>`car_setting_crash_lights_double_impulse` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0125_DEVELOPER_MENU` | **Developer menu screen in MMI via holding MENU for ~10 seconds (req. Discover Pro)**<br>`car_setting_developer_menu` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0126_DIAGNOSTICS_BRAKE_LIGHTS` | **Diagnostics Brake Lights**<br>`car_setting_diagnostics_brake_lights` | `0x03` (BRAKES_ABS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0135_DISABLE_MP3_LEGAL_DISCLAIMER` | **Disable Mp3 Legal Disclaimer**<br>`car_setting_disable_mp3_legal_disclaimer` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Enabled / Disabled | `VERIFIED` |
| `FEAT_0136_DISABLE_NAR_HEADLIGHT_RESTRICTIONS` | **Disable Nar Headlight Restrictions**<br>`car_setting_disable_nar_headlight_restrictions` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Enabled / Disabled | `VERIFIED` |
| `FEAT_0137_DISABLE_US_MARKER_LIGHTS` | **Disable US side marker lights (US models only)**<br>`car_setting_disable_us_marker_lights` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Enabled / Disabled | `VERIFIED` |
| `FEAT_0138_DISPLAY_CYLINDER_SHUT_OFF` | **Display Cylinder Shut Off**<br>`car_setting_display_cylinder_shut_off` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0140_DLNA` | **Dlna**<br>`car_setting_dlna` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0141_DRIVER_AIDS` | **Driver-aids**<br>`car_setting_driver_aids` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0142_DRIVING_PROFILE_SELECTION` | **Driving profile selection**<br>`car_setting_driving_profile_selection` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0143_DRIVING_SCHOOL_MIB1_STEP_1` | **Driving School Mib1 Step 1**<br>`car_setting_driving_school_mib1_step_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0144_DRIVING_SCHOOL_MIB1_STEP_2` | **Driving School Mib1 Step 2**<br>`car_setting_driving_school_mib1_step_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0145_DRIVING_SCHOOL_MIB1_STEP_3` | **Driving School Mib1 Step 3**<br>`car_setting_driving_school_mib1_step_3` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0146_DRIVING_SCHOOL_MIB1_STEP_4` | **Driving School Mib1 Step 4**<br>`car_setting_driving_school_mib1_step_4` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0169_DSR_STRENGTH` | **Driver steering recommendation (DSR) strength**<br>`car_setting_dsr_strength` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0170_DYNAMIC_LIGHT_ASSIST` | **Dynamic Light Assist**<br>`car_setting_dynamic_light_assist` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0171_DYNAMIC_START_UP_ASSIST` | **Dynamic start assist**<br>`car_setting_dynamic_start_up_assist` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0175_ELECTRONIC_DIFF_LOCK` | **Electronic differential lock (if equipped)**<br>`car_setting_electronic_diff_lock` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0176_ELECTRONIC_DIFF_LOCK_STEP_2` | **Electronic Diff Lock Step 2**<br>`car_setting_electronic_diff_lock_step_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0177_ELECTRONIC_DIFF_LOCK_STRENGTH` | **Electronic differential lock strength**<br>`car_setting_electronic_diff_lock_strength` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0178_ELECTRONIC_DIFF_LOCK_STRENGTH_XDS` | **Extended electronic differential lock strength (XDS)**<br>`car_setting_electronic_diff_lock_strength_xds` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0179_EMERGENCY_BRAKE_FLASHING` | **Flash brake lights in emergency stopping**<br>`car_setting_emergency_brake_flashing` | `0x03` (BRAKES_ABS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0181_ENABLED_V1` | **Enabled (Version 1)**<br>`car_setting_enabled_v1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Enabled / Disabled | `VERIFIED` |
| `FEAT_0182_ENABLED_V2` | **Enabled (Version 2)**<br>`car_setting_enabled_v2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Enabled / Disabled | `VERIFIED` |
| `FEAT_0183_ESC_ASR` | **ESC / ASR**<br>`car_setting_esc_asr` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0184_ESC_ASR_BUTTON_BEHAVIOR` | **ESC / ASR button behavior**<br>`car_setting_esc_asr_button_behavior` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0185_ESE` | **Engine Sound Enhancement (ESE)**<br>`car_setting_ese` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0186_EXIDE_43_AH_390_CCA_T4` | **Exide 43Ah 390CCA T4**<br>`car_setting_exide_43_ah_390_cca_t4` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0187_EXIDE_52_AH_500_CCA_T5` | **Exide 52Ah 500CCA T5**<br>`car_setting_exide_52_ah_500_cca_t5` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0188_EXIDE_60_AH_520_CCA_H5` | **Exide 60Ah 520CCA H5**<br>`car_setting_exide_60_ah_520_cca_h5` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0189_EXIDE_60_AH_590_CCA_T6` | **Exide 60Ah 590CCA T6**<br>`car_setting_exide_60_ah_590_cca_t6` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0190_EXIDE_70_AH_600_CCA_H6` | **Exide 70Ah 600CCA H6**<br>`car_setting_exide_70_ah_600_cca_h6` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0191_EXIDE_80_AH_700_CCA_H7` | **Exide 80Ah 700CCA H7**<br>`car_setting_exide_80_ah_700_cca_h7` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0192_EXIDE_80_AH_70_CCA_T7` | **Exide 80Ah 70CCA T7**<br>`car_setting_exide_80_ah_70_cca_t7` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0193_EXIDE_90_AH_800_CCA_H8` | **Exide 90Ah 800CCA H8**<br>`car_setting_exide_90_ah_800_cca_h8` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0194_EXIDE_90_AH_800_CCA_T8` | **Exide 90Ah 800CCA T8**<br>`car_setting_exide_90_ah_800_cca_t8` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0195_EXIDE_90_AH_950_CCA_H8` | **Exide 90Ah 950CCA H8**<br>`car_setting_exide_90_ah_950_cca_h8` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0200_FUEL_CONSUMPTION_POSITION_0` | **Fuel consumption (position 0)**<br>`car_setting_fuel_consumption_position_0` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0201_FUEL_CONSUMPTION_POSITION_1` | **Fuel consumption (position 1)**<br>`car_setting_fuel_consumption_position_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0202_FUEL_CONSUMPTION_POSITION_2` | **Fuel consumption (position 2)**<br>`car_setting_fuel_consumption_position_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0203_FUEL_CONSUMPTION_POSITION_3` | **Fuel consumption (position 3)**<br>`car_setting_fuel_consumption_position_3` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0204_FUEL_CONSUMPTION_POSITION_4` | **Fuel consumption (position 4)**<br>`car_setting_fuel_consumption_position_4` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0205_FUEL_TANK_CAPACITY_CALIBRATION` | **Fuel Tank Capacity Calibration**<br>`car_setting_fuel_tank_capacity_calibration` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0208_GENERAL_LED_UP_TO_6W` | **General Led Up To 6W**<br>`car_setting_general_led_up_to_6W` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0209_HALDEX_SETUP` | **Haldex AWD system setup**<br>`car_setting_haldex_setup` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0210_HAZARD_LIGHTS_AFTER_CRASH` | **Hazard Lights After Crash**<br>`car_setting_hazard_lights_after_crash` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0211_HEADLIGHT_CLEANING` | **Headlight cleaning**<br>`car_setting_headlight_cleaning` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0215_HIDDEN_MENU_CAR_SETUP` | **Hidden (green) menu in dash screen via holding CAR + SETUP (req. restart)**<br>`car_setting_hidden_menu_car_setup` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0216_HIGH` | **High**<br>`car_setting_high` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0219_HILL_HOLD` | **Hill hold assist (if equipped)**<br>`car_setting_hill_hold` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0220_HILL_HOLD_RELEASE` | **Hill hold assist release**<br>`car_setting_hill_hold_release` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0221_HILL_START_ASSIST_MODE` | **Hill start assist disengagement**<br>`car_setting_hill_start_assist_mode` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0224_HORN_WITH_IGN_OFF` | **Horn works even when ignition is off**<br>`car_setting_horn_with_ign_off` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0226_INDIVIDUALLY_ADJUSTABLE_SPEED_LIMIT` | **Individually adjustable speed limit**<br>`car_setting_individually_adjustable_speed_limit` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0230_INSTRUCTION_AUTOMATIC_DRIVEAWAY_AFTER_SHORT_STOP` | **Instruction Automatic Driveaway After Short Stop**<br>`car_setting_instruction_automatic_driveaway_after_short_stop` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0231_INSTRUCTION_BATTERY_CHARGE_DISPLAY_MK7` | **Instruction Battery Charge Display Mk7**<br>`car_setting_instruction_battery_charge_display_mk7` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0232_INSTRUCTION_DRIVING_SCHOOL_MIB1` | **Instruction Driving School Mib1**<br>`car_setting_instruction_driving_school_mib1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0237_INSTRUCTION_MAY_NOT_WORK` | **This customization may fail to save on some cars. If it does, that means your car doesn't support it.**<br>`car_setting_instruction_may_not_work` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0238_INSTRUCTION_MAY_NOT_WORK_TRY_A_FEW_TIMES` | **This setting is still experimental and it may fail to save. Feel free to try a few times, and if it still doesn't work, rest assured that we know about it and are working on it.**<br>`car_setting_instruction_may_not_work_try_a_few_times` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0239_INSTRUCTION_REQ_INFOTAINMENT_REBOOT` | **Please note that this customization requires infotainment reboot.**<br>`car_setting_instruction_req_infotainment_reboot` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0241_INSTRUCTION_REQUIRES_SENSORS` | **Note that this setting only works if the car has the required sensors (most S and RS cars do).**<br>`car_setting_instruction_requires_sensors` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0242_INSTRUCTION_SETTINGS_WITH_STEPS` | **Note that you need to enable all steps for this to work.**<br>`car_setting_instruction_settings_with_steps` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0243_INSTRUCTION_TRANSMISSION_FLUILD_TEMP` | **Typical transmission fluid temperature is around 82 - 94 °C (180 - 200 °F).**<br>`car_setting_instruction_transmission_fluild_temp` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0245_INSTRUMENT_LIGHTS_AFTER_CRASH` | **Instrument Lights After Crash**<br>`car_setting_instrument_lights_after_crash` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0247_INTERVAL` | **Interval**<br>`car_setting_interval` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0249_JETS` | **Jets**<br>`car_setting_jets` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0253_LAP_COUNTER` | **Lap Counter**<br>`car_setting_lap_counter` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0259_LEAVING_SOUND_REQ_REBOOT` | **Leaving Sound Req Reboot**<br>`car_setting_leaving_sound_req_reboot` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0261_LED_LOW_POWER` | **LED low power**<br>`car_setting_led_low_power` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0262_LIGHT_SENSOR_HEADLIGHTS` | **Light Sensor Headlights**<br>`car_setting_light_sensor_headlights` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0263_LOW` | **Low**<br>`car_setting_low` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0264_LOW_POWER_MODE` | **Vehicle low-power mode**<br>`car_setting_low_power_mode` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0270_MEDIUM` | **Medium**<br>`car_setting_medium` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0277_MICROPHONE_SENSITIVITY` | **Microphone sensitivity**<br>`car_setting_microphone_sensitivity` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0281_NAVIGATION_COMPASS_DISPLAY` | **Navigation compass display**<br>`car_setting_navigation_compass_display` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0282_NOISE_VIBRATION_REDUCTION` | **Noise Vibration Reduction**<br>`car_setting_noise_vibration_reduction` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0283_NOT_DEFINED` | **Not defined**<br>`car_setting_not_defined` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0286_OIL_TEMP_POSITION_0` | **Oil temperature (position 0)**<br>`car_setting_oil_temp_position_0` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0287_OIL_TEMP_POSITION_1` | **Oil temperature (position 1)**<br>`car_setting_oil_temp_position_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0288_OIL_TEMP_POSITION_2` | **Oil temperature (position 2)**<br>`car_setting_oil_temp_position_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0289_OIL_TEMP_POSITION_3` | **Oil temperature (position 3)**<br>`car_setting_oil_temp_position_3` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0290_OIL_TEMP_POSITION_4` | **Oil temperature (position 4)**<br>`car_setting_oil_temp_position_4` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0291_ONLINE_TRAFFIC_UPDATES` | **Online Traffic Updates**<br>`car_setting_online_traffic_updates` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0293_PARKING_LIGHTS` | **"Euro" parking lights when ignition off, turn signal on**<br>`car_setting_parking_lights` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0294_PARKING_LIGHTS_WITH_TERM_15` | **Parking lights only when ignition is on**<br>`car_setting_parking_lights_with_term_15` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0295_PARTIALLY` | **Partially**<br>`car_setting_partially` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0296_PASSIVE_ENTRY_REAR_LEFT_DOOR` | **Passive Entry Rear Left Door**<br>`car_setting_passive_entry_rear_left_door` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0297_PASSIVE_ENTRY_REAR_RIGHT_DOOR` | **Passive Entry Rear Right Door**<br>`car_setting_passive_entry_rear_right_door` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0298_PASSIVE_EXIT_REAR_LEFT_DOOR` | **Passive Exit Rear Left Door**<br>`car_setting_passive_exit_rear_left_door` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0299_PASSIVE_EXIT_REAR_RIGHT_DOOR` | **Passive Exit Rear Right Door**<br>`car_setting_passive_exit_rear_right_door` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0300_PCS` | **Pcs**<br>`car_setting_pcs` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0305_PCS_DRIVER_AIDS_LAST_STATE` | **Pre-Collision System (PCS) driver aids: remember last state**<br>`car_setting_pcs_driver_aids_last_state` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0306_PCS_OPERATION_LAST_STATE` | **Pre-Collision System (PCS) sensitivity: remember last state**<br>`car_setting_pcs_operation_last_state` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0307_PCS_REACTION_TIME` | **Pre-Collision System (PCS) reacts…**<br>`car_setting_pcs_reaction_time` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0308_PCS_REAR_VEHICLE_DETECTION` | **Pre-Collision System (PCS) brake when vehicle is detected from behind**<br>`car_setting_pcs_rear_vehicle_detection` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0309_PCS_SENSITIVITY` | **Pre-Collision System (PCS) sensitivity**<br>`car_setting_pcs_sensitivity` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0312_POWER_STEERING_DEFAULT_MODE` | **Power steering default mode**<br>`car_setting_power_steering_default_mode` | `0x44` (STEERING_ASSIST) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0313_POWER_STEERING_WEIGHT_PRESET` | **Power steering weight preset**<br>`car_setting_power_steering_weight_preset` | `0x44` (STEERING_ASSIST) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0314_POWER_STEERING_WHEN_ENGINE_NOT_RUNNING` | **Power Steering When Engine Not Running**<br>`car_setting_power_steering_when_engine_not_running` | `0x01` (ENGINE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0315_PUDDLE_LIGHTS_DRIVER_SIDE` | **Puddle lights driver side**<br>`car_setting_puddle_lights_driver_side` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0320_REAR_HATCH_AUTO_UP_COVER` | **Rear Hatch Auto Up Cover**<br>`car_setting_rear_hatch_auto_up_cover` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0324_REAR_VIEW_CAMERA` | **Rear view camera**<br>`car_setting_rear_view_camera` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0327_REFUEL_QUANTITY_MFD` | **Refuel quantity in MFD**<br>`car_setting_refuel_quantity_mfd` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0328_REMEMBER_RECIRCULATING_AIR_STATE` | **Remember recirculating air state**<br>`car_setting_remember_recirculating_air_state` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0329_REMOTE_LIMIT_RANGE_LOCK` | **Remote Limit Range Lock**<br>`car_setting_remote_limit_range_lock` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0330_REMOTE_LIMIT_RANGE_OVERALL` | **Remote Limit Range Overall**<br>`car_setting_remote_limit_range_overall` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0331_REMOTE_LIMIT_RANGE_PANIC_BUTTON` | **Remote Limit Range Panic Button**<br>`car_setting_remote_limit_range_panic_button` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0332_REMOTE_LIMIT_RANGE_REAR_LID` | **Remote Limit Range Rear Lid**<br>`car_setting_remote_limit_range_rear_lid` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0333_REMOTE_LIMIT_RANGE_UNLOCK` | **Remote Limit Range Unlock**<br>`car_setting_remote_limit_range_unlock` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0334_REMOTE_WHEN_IN_GEAR` | **Remote When In Gear**<br>`car_setting_remote_when_in_gear` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0335_REMOTE_WITH_IGNITION` | **Enable remote control buttons when ignition is on**<br>`car_setting_remote_with_ignition` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0338_RESTRICT_VIDEO_SPEED` | **Video in motion restriction speed**<br>`car_setting_restrict_video_speed` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0341_SDS_IF_EQUIPPED` | **Sds If Equipped**<br>`car_setting_sds_if_equipped` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0354_SHIFT_SUGGESTION_ECONOMY` | **Display gear shift suggestions (Economy)**<br>`car_setting_shift_suggestion_economy` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0360_SLIDE` | **Slide**<br>`car_setting_slide` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0361_SMART_REMOTE_WITH_IGNITION` | **Enable smart key buttons when ignition is on**<br>`car_setting_smart_remote_with_ignition` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0362_SOUND_ON_LOCK_KEY` | **Sound On Lock Key**<br>`car_setting_sound_on_lock_key` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0363_SOUND_ON_LOCK_REMOTE` | **Sound On Lock Remote**<br>`car_setting_sound_on_lock_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0364_SOUND_ON_LOCK_UNLOCK_ADAPT_ENABLED` | **Sound On Lock Unlock Adapt Enabled**<br>`car_setting_sound_on_lock_unlock_adapt_enabled` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Enabled / Disabled | `VERIFIED` |
| `FEAT_0365_SOUND_ON_UNLOCK_KEY` | **Sound On Unlock Key**<br>`car_setting_sound_on_unlock_key` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0366_SOUND_ON_UNLOCK_REMOTE` | **Sound On Unlock Remote**<br>`car_setting_sound_on_unlock_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0367_SPEAKER_VOLUME` | **Speaker volume**<br>`car_setting_speaker_volume` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0368_SPEED_DIGITAL_DISPLAY` | **Show digital speed in dashboard (BC)**<br>`car_setting_speed_digital_display` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0369_SPEEDOMETER_CALIBRATION` | **Speedometer calibration**<br>`car_setting_speedometer_calibration` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0370_SPORT_DISPLAY_VIRTUAL_INSTRUMENTS` | **Sport Display Virtual Instruments**<br>`car_setting_sport_display_virtual_instruments` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0372_START_SCREEN` | **Start screen logo**<br>`car_setting_start_screen` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0373_START_SCREEN_INFOTAINMENT` | **Start screen logo (infotainment)**<br>`car_setting_start_screen_infotainment` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0381_STATIC_SPEED_LIMIT` | **Static speed limit**<br>`car_setting_static_speed_limit` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0382_STEERING_DIRECTION` | **Steering Direction**<br>`car_setting_steering_direction` | `0x44` (STEERING_ASSIST) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0383_STRONG` | **Strong**<br>`car_setting_strong` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0388_SURROUND_AND_SUBWOOFER_MENU_INFOTAINMENT` | **Surround And Subwoofer Menu Infotainment**<br>`car_setting_surround_and_subwoofer_menu_infotainment` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0389_TAILLIGHT_PATTERN_EU` | **Taillight Pattern Eu**<br>`car_setting_taillight_pattern_eu` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0390_TAILLIGHT_PATTERN_US` | **Taillight Pattern Us**<br>`car_setting_taillight_pattern_us` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0391_TAILLIGHTS_ANIMATION` | **Taillights Animation**<br>`car_setting_taillights_animation` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0392_THEME_INFOTAINMENT` | **Theme Infotainment**<br>`car_setting_theme_infotainment` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0394_TILT` | **Tilt**<br>`car_setting_tilt` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0395_TORQUE_LIMITER_INTERACTION` | **Torque limiter interaction**<br>`car_setting_torque_limiter_interaction` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0405_TRACTION_CONTROL_BTN_ESC_STEP_1` | **Traction Control Btn Esc Step 1**<br>`car_setting_traction_control_btn_esc_step_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0406_TRACTION_CONTROL_BTN_ESC_STEP_2` | **Traction Control Btn Esc Step 2**<br>`car_setting_traction_control_btn_esc_step_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0414_TRAILER_ASSIST_STEP_1` | **Trailer Assist Step 1**<br>`car_setting_trailer_assist_step_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0415_TRAILER_ASSIST_STEP_2` | **Trailer Assist Step 2**<br>`car_setting_trailer_assist_step_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0416_TRAILER_ASSIST_STEP_3` | **Trailer Assist Step 3**<br>`car_setting_trailer_assist_step_3` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0417_TRAILER_ASSIST_STEP_4` | **Trailer Assist Step 4**<br>`car_setting_trailer_assist_step_4` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0418_TRAILER_ASSIST_STEP_5` | **Trailer Assist Step 5**<br>`car_setting_trailer_assist_step_5` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0425_TYPE1` | **Type 1**<br>`car_setting_type1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0426_TYPE2` | **Type 2**<br>`car_setting_type2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0432_UPSHIFT_INDICATOR` | **Upshift Indicator**<br>`car_setting_upshift_indicator` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0433_UPSHIFT_INDICATOR_LAP_COUNTER` | **Upshift Indicator Lap Counter**<br>`car_setting_upshift_indicator_lap_counter` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0435_US_MARKER_LIGHTS` | **Turn on side marker lights with headlights (US models only)**<br>`car_setting_us_marker_lights` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0436_VALUE_0` | **Value 0**<br>`car_setting_value_0` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0437_VALUE_1` | **Value 1**<br>`car_setting_value_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0438_VALUE_2` | **Value 2**<br>`car_setting_value_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0439_VALUE_3` | **Value 3**<br>`car_setting_value_3` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0440_VALUE_4` | **Value 4**<br>`car_setting_value_4` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0441_VALUE_5` | **Value 5**<br>`car_setting_value_5` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0442_VALUE_6` | **Value 6**<br>`car_setting_value_6` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0443_VALUE_7` | **Value 7**<br>`car_setting_value_7` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0444_VARTA_43_AH_390_CCA_T4` | **Varta 43Ah 390CCA T4**<br>`car_setting_varta_43_ah_390_cca_t4` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0445_VARTA_52_AH_500_CCA_T5` | **Varta 52Ah 500CCA T5**<br>`car_setting_varta_52_ah_500_cca_t5` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0446_VARTA_60_AH_520_CCA_H5` | **Varta 60Ah 520CCA H5**<br>`car_setting_varta_60_ah_520_cca_h5` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0447_VARTA_60_AH_590_CCA_T6` | **Varta 60Ah 590CCA T6**<br>`car_setting_varta_60_ah_590_cca_t6` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0448_VARTA_70_AH_600_CCA_H6` | **Varta 70Ah 600CCA H6**<br>`car_setting_varta_70_ah_600_cca_h6` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0449_VARTA_80_AH_700_CCA_H7` | **Varta 80Ah 700CCA H7**<br>`car_setting_varta_80_ah_700_cca_h7` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0450_VARTA_80_AH_70_CCA_T7` | **Varta 80Ah 70CCA T7**<br>`car_setting_varta_80_ah_70_cca_t7` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0451_VARTA_90_AH_800_CCA_H8` | **Varta 90Ah 800CCA H8**<br>`car_setting_varta_90_ah_800_cca_h8` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0452_VARTA_90_AH_800_CCA_T8` | **Varta 90Ah 800CCA T8**<br>`car_setting_varta_90_ah_800_cca_t8` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0453_VARTA_90_AH_950_CCA_H8` | **Varta 90Ah 950CCA H8**<br>`car_setting_varta_90_ah_950_cca_h8` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0454_VIRTUAL_COCKPIT_COLOR_1` | **Virtual instrument cluster theme - color 1**<br>`car_setting_virtual_cockpit_color_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0455_VIRTUAL_COCKPIT_COLOR_CHANGE` | **Virtual Cockpit Color Change**<br>`car_setting_virtual_cockpit_color_change` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0456_VIRTUAL_COCKPIT_COLOR_CHANGE_MENU` | **Virtual Cockpit Color Change Menu**<br>`car_setting_virtual_cockpit_color_change_menu` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0458_VOICE_RECOGNITION` | **Voice recognition**<br>`car_setting_voice_recognition` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0459_WARN_NAV_DEST_AT_SPEED` | **Display warning about using navigation when moving**<br>`car_setting_warn_nav_dest_at_speed` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0460_WARN_ON_HILL_DESCENT` | **Warn On Hill Descent**<br>`car_setting_warn_on_hill_descent` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0461_WARN_ON_KEY_IN_IGNITION` | **Ding when key is left in ignition**<br>`car_setting_warn_on_key_in_ignition` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0462_WARN_VOICE_DEST_AT_SPEED` | **Display warning about using nav voice control when moving**<br>`car_setting_warn_voice_dest_at_speed` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0464_WEAK` | **Weak**<br>`car_setting_weak` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0466_WIRELESS_CARPLAY_STEP_1` | **Wireless Carplay Step 1**<br>`car_setting_wireless_carplay_step_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0467_WIRELESS_CARPLAY_STEP_2` | **Wireless Carplay Step 2**<br>`car_setting_wireless_carplay_step_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0468_WLAN_STEP_1` | **Wlan Step 1**<br>`car_setting_wlan_step_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0469_WLAN_STEP_2` | **Wlan Step 2**<br>`car_setting_wlan_step_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0470_WLAN_STEP_3` | **Wlan Step 3**<br>`car_setting_wlan_step_3` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0471_YES_IMMEDIATELY` | **Yes, turn on immediately**<br>`car_setting_yes_immediately` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0472_YES_SOFTLY` | **Yes, turn on gradually**<br>`car_setting_yes_softly` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Parking Sensors (3 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0321_REAR_PARK_ASSIST_FREQ` | **Rear parking sensor beep tone**<br>`car_setting_rear_park_assist_freq` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0322_REAR_PARK_ASSIST_VOL` | **Rear parking sensor beep volume**<br>`car_setting_rear_park_assist_vol` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0323_REAR_PARK_ASSIST_VOL_CONV_OPEN` | **Rear parking sensor beep volume when convertible top is open**<br>`car_setting_rear_park_assist_vol_conv_open` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Seats & Steering Wheel (3 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0348_SEAT_HEATER_TEMPERATURE_ADJUSTMENT_STAGE_1` | **Seat Heater Temperature Adjustment Stage 1**<br>`car_setting_seat_heater_temperature_adjustment_stage_1` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0349_SEAT_HEATER_TEMPERATURE_ADJUSTMENT_STAGE_2` | **Seat Heater Temperature Adjustment Stage 2**<br>`car_setting_seat_heater_temperature_adjustment_stage_2` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |
| `FEAT_0350_SEAT_HEATER_TEMPERATURE_ADJUSTMENT_STAGE_3` | **Seat Heater Temperature Adjustment Stage 3**<br>`car_setting_seat_heater_temperature_adjustment_stage_3` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | Numerical | Range / Percentage / Value steps | `VERIFIED` |

---

## Service Tools (16 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `TOOL_EPB_SERVICE` | **Electronic Parking Brake (EPB) Retract / Close**<br>`epb_electronic_parking_brake_service` | `0x53` (PARKING_BRAKE (Tx: 0x752, Rx: 0x7BC)) | UDS (ISO 14229) | Procedure | Open Pistons, Close Pistons, Calibrate Thickness | `VERIFIED` |
| `TOOL_DPF_REGENERATION` | **DPF Regeneration (Service / Emergency)**<br>`dpf_diesel_particulate_filter_regeneration` | `0x01` (ENGINE (Tx: 0x7E0, Rx: 0x7E8)) | UDS (ISO 14229) | Procedure | Start Stationary Regen, Start Driving Regen | `VERIFIED` |
| `TOOL_BATTERY_REGISTRATION` | **Battery Registration (New Battery Coding)**<br>`battery_registration_adaptation` | `0x19` (CAN_GATEWAY (Tx: 0x710, Rx: 0x77A) or BATTERY_REG (0x61)) | UDS / KWP2000 | Structured Parameters | Capacity: 40-110 Ah; Tech: Fleece/AGM, EFB, Wet; Mfr: VTA, JCB, MLA, TU3 | `VERIFIED` |
| `TOOL_SERVICE_RESET` | **Service Indicator Reset (Oil & Inspection)**<br>`service_indicator_wiv_reset` | `0x17` (INSTRUMENT_CLUSTER (Tx: 0x714, Rx: 0x77E)) | UDS / KWP2000 | Procedure | Reset Oil Service, Reset Inspection Service | `VERIFIED` |
| `FEAT_0067_BATTERY_REG` | **Battery registration**<br>`car_setting_battery_reg` | `0x19` (CAN_GATEWAY) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0336_REQ_BRAKE_PEDAL_WHEN_RELEASING_EPB` | **Require brake pedal when releasing parking brake**<br>`car_setting_req_brake_pedal_when_releasing_epb` | `0x53` (PARKING_BRAKE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0371_START_DPF` | **Start Dpf**<br>`car_setting_start_dpf` | `0x01` (ENGINE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0396_TPMS_IN_MMI_STEP_1` | **Tpms In Mmi Step 1**<br>`car_setting_tpms_in_mmi_step_1` | `0x65` (TIRE_PRESSURE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0397_TPMS_IN_MMI_STEP_2` | **Tpms In Mmi Step 2**<br>`car_setting_tpms_in_mmi_step_2` | `0x65` (TIRE_PRESSURE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0398_TPMS_IN_MMI_STEP_3` | **Tpms In Mmi Step 3**<br>`car_setting_tpms_in_mmi_step_3` | `0x65` (TIRE_PRESSURE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0399_TPMS_IN_MMI_STEP_4` | **Tpms In Mmi Step 4**<br>`car_setting_tpms_in_mmi_step_4` | `0x65` (TIRE_PRESSURE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0400_TPMS_IN_MMI_STEP_5` | **Tpms In Mmi Step 5**<br>`car_setting_tpms_in_mmi_step_5` | `0x65` (TIRE_PRESSURE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0401_TPMS_INDIRECT_STEP_2` | **Tpms Indirect Step 2**<br>`car_setting_tpms_indirect_step_2` | `0x65` (TIRE_PRESSURE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0402_TPMS_INDIRECT_STEP_3` | **Tpms Indirect Step 3**<br>`car_setting_tpms_indirect_step_3` | `0x65` (TIRE_PRESSURE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0403_TPMS_SENSITIVITY` | **Tpms Sensitivity**<br>`car_setting_tpms_sensitivity` | `0x65` (TIRE_PRESSURE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0404_TPMS_SYSTEM` | **TPMS system**<br>`car_setting_tpms_system` | `0x65` (TIRE_PRESSURE) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Trunk (4 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0292_OPEN_CLOSE_POWER_TRUNK_REMOTE` | **Open Close Power Trunk Remote**<br>`car_setting_open_close_power_trunk_remote` | `0x6D` (TRUNK) | UDS | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0310_POP_TRUNK_REMOTE` | **Pop trunk via remote**<br>`car_setting_pop_trunk_remote` | `0x6D` (TRUNK) | UDS | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0419_TRUNK_CLOSING_DURATION` | **Trunk Closing Duration**<br>`car_setting_trunk_closing_duration` | `0x6D` (TRUNK) | UDS | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0420_TRUNK_LID_REMOTE` | **Open trunk lid with remote**<br>`car_setting_trunk_lid_remote` | `0x6D` (TRUNK) | UDS | MultipleChoice | Yes / No | `VERIFIED` |

---

## Windows & Sunroof (14 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0014_ALLOW_RAIN_CLOSING` | **Allow rain closing**<br>`car_setting_allow_rain_closing` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Enabled / Disabled | `VERIFIED` |
| `FEAT_0098_COMFORT_CLOSE_SUNROOF_KEY` | **Close sunroof by turning and holding key in door lock**<br>`car_setting_comfort_close_sunroof_key` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0099_COMFORT_CLOSE_WINDOWS_REMOTE` | **Close windows via long-press on remote**<br>`car_setting_comfort_close_windows_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0100_COMFORT_CLOSE_WINDOWS_REMOTE_SINGLE_PRESS` | **Comfort Close Windows Remote Single Press**<br>`car_setting_comfort_close_windows_remote_single_press` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0103_COMFORT_FUNCTION_SUNROOF` | **Open/close sunroof via long-press on remote or key**<br>`car_setting_comfort_function_sunroof` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0108_COMFORT_OPEN_SUNROOF_KEY` | **Open sunroof by turning and holding key in door lock**<br>`car_setting_comfort_open_sunroof_key` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0109_COMFORT_OPEN_SUNROOF_REMOTE` | **Open sunroof via long-press on remote**<br>`car_setting_comfort_open_sunroof_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0110_COMFORT_OPEN_WINDOWS_REMOTE` | **Open windows via long-press on remote**<br>`car_setting_comfort_open_windows_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0279_MIRROR_HEATING_WITH_REAR_WINDOW_HEATER` | **Activate side mirror heaters when rear window defroster is on**<br>`car_setting_mirror_heating_with_rear_window_heater` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0384_SUNROOF_ACTION_VIA_KEY` | **Sunroof action when opening via holding down the driver side key for 1.5 seconds**<br>`car_setting_sunroof_action_via_key` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0385_SUNROOF_ACTION_VIA_REMOTE` | **Sunroof action when opening via remote**<br>`car_setting_sunroof_action_via_remote` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0386_SUNROOF_RAIN_CLOSING` | **Auto-close sunroof when rain is detected (must have rain sensor)**<br>`car_setting_sunroof_rain_closing` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0387_SUNROOF_RAIN_CLOSING_IN_MMI` | **Rain closing menu in MMI**<br>`car_setting_sunroof_rain_closing_in_mmi` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0465_WINDOW_LOWERING_DOOR_OPEN` | **Window Lowering Door Open**<br>`car_setting_window_lowering_door_open` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

## Wipers & Washer (8 features)

| ID | Feature Name | ECU | Protocol | Value Type | Allowed Values | Confidence |
|---|---|---|---|---|---|---|
| `FEAT_0199_FRONT_WIPERS_TEAR_WIPING` | **Additional 'tear' wipe after windshield washer use**<br>`car_setting_front_wipers_tear_wiping` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0212_HEADLIGHT_WASHER` | **Headlight Washer**<br>`car_setting_headlight_washer` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0213_HEADLIGHT_WASHERS_IF_EQUIPPED` | **Headlight washers (if equipped)**<br>`car_setting_headlight_washers_if_equipped` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0284_NUM_FRONT_WASHER_ACTIVE_WO_HEADLIGHT_WASHER_ACTIVE` | **Activate headlight washers once every … times the windshield washer is used**<br>`car_setting_num_front_washer_active_wo_headlight_washer_active` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Enabled / Disabled | `VERIFIED` |
| `FEAT_0319_RAIN_SENSOR_WIPERS` | **Automatic wipers (using rain sensor)**<br>`car_setting_rain_sensor_wipers` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0325_REAR_WIPER_CONTINUOUS` | **Rear Wiper Continuous**<br>`car_setting_rear_wiper_continuous` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0326_REAR_WIPER_TEAR_WIPING` | **Additional 'tear' wipe after rear window washer use**<br>`car_setting_rear_wiper_tear_wiping` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |
| `FEAT_0463_WASHER_FLUID_WARNING` | **Washer fluid warning**<br>`car_setting_washer_fluid_warning` | `0x09` (CENTRAL_ELECTRICS) | UDS / KWP2000 | MultipleChoice | Yes / No | `VERIFIED` |

---

