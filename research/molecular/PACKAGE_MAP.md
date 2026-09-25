# Molecular Package Map & Anatomy

**Target Package**: `com.prizmos.carista`  
**Version**: `10.0` (code `1000099`)  
**SDK Requirements**: minSdk `32`, targetSdk `36`  

## 1. Split APK Architecture

| Split Name | File Name | Size (Bytes) | Role / Content Description |
|---|---|---|---|
| `base` | `com.prizmos.carista.apk` | 40,338,343 | Application core, bytecode (classes.dex, classes2.dex), resources, assets, AndroidManifest.xml |
| `config.arm64_v8a` | `config.arm64_v8a.apk` | 41,013,872 | Native binaries for 64-bit ARM architecture (libCarista.so, librealm-jni.so) |
| `config.xxhdpi` | `config.xxhdpi.apk` | 142,277 | Device screen density resources (xxhdpi 480dpi drawables and raster assets) |

## 2. Component Summary by Feature Area

| Feature Area | Activities | Services | Receivers | Total Components |
|---|---|---|---|---|
| **Core / General UI** | 55 | 1 | 15 | 71 |
| **Service Tools** | 9 | 16 | 2 | 27 |
| **Customizations / Coding** | 10 | 0 | 0 | 10 |
| **Garage & Vehicle Management** | 8 | 0 | 0 | 8 |
| **Account & Authentication** | 5 | 0 | 2 | 7 |
| **Connection / Transport** | 4 | 0 | 0 | 4 |
| **Live Data** | 2 | 0 | 0 | 2 |
| **Billing & Subscriptions** | 2 | 0 | 0 | 2 |
| **DTC Diagnostics** | 1 | 0 | 0 | 1 |
| **AutoScan / Discovery** | 1 | 0 | 0 | 1 |
| **Telemetry & Analytics** | 0 | 0 | 1 | 1 |

## 3. Activities & Entry Points

| Activity Class | Exported | Feature Area | Deep Links / Actions |
|---|---|---|---|
| `ConnectActivity` (`com.prizmos.carista.ConnectActivity`) | `true` | Connection / Transport | `pushscheme://com.prizmos.carista/ConnectActivity` |
| `LogInActivity` (`com.prizmos.carista.LogInActivity`) | `true` | Account & Authentication | `None` |
| `AuthorizeActivity` (`com.prizmos.carista.AuthorizeActivity`) | `true` | Account & Authentication | `None` |
| `RegisterActivity` (`com.prizmos.carista.RegisterActivity`) | `false` | Core / General UI | `None` |
| `ForgottenPasswordActivity` (`com.prizmos.carista.ForgottenPasswordActivity`) | `false` | Core / General UI | `None` |
| `FeatureDetailsActivity` (`com.prizmos.carista.FeatureDetailsActivity`) | `false` | Core / General UI | `None` |
| `MainActivity` (`com.prizmos.carista.screens.operation.main.MainActivity`) | `false` | Core / General UI | `None` |
| `GenericToolActivity` (`com.prizmos.carista.GenericToolActivity`) | `false` | Service Tools | `None` |
| `CheckCodesActivity` (`com.prizmos.carista.screens.operation.checkcodes.CheckCodesActivity`) | `false` | DTC Diagnostics | `None` |
| `RestoreActivity` (`com.prizmos.carista.screens.operation.restore.RestoreActivity`) | `false` | Core / General UI | `None` |
| `EvoFirmwareUpdateActivity` (`com.prizmos.carista.screens.operation.evofirmwareupdate.EvoFirmwareUpdateActivity`) | `false` | Core / General UI | `None` |
| `SettingReportActivity` (`com.prizmos.carista.SettingReportActivity`) | `false` | Customizations / Coding | `None` |
| `ShowSettingCategoriesActivity` (`com.prizmos.carista.screens.operation.showsettingcategories.ShowSettingCategoriesActivity`) | `false` | Customizations / Coding | `None` |
| `ShowSettingsActivity` (`com.prizmos.carista.screens.operation.showsettings.ShowSettingsActivity`) | `false` | Customizations / Coding | `None` |
| `ChangeSettingActivity` (`com.prizmos.carista.screens.operation.changesetting.ChangeSettingActivity`) | `false` | Customizations / Coding | `None` |
| `PricingActivity` (`com.prizmos.carista.PricingActivity`) | `false` | Core / General UI | `None` |
| `CollectDebugInfoActivity` (`com.prizmos.carista.screens.operation.collectdebuginfo.CollectDebugInfoActivity`) | `false` | Core / General UI | `None` |
| `FullScanActivity` (`com.prizmos.carista.screens.operation.fullscan.FullScanActivity`) | `false` | AutoScan / Discovery | `None` |
| `UploadLogActivity` (`com.prizmos.carista.UploadLogActivity`) | `false` | Core / General UI | `None` |
| `BetaEligibilityActivity` (`com.prizmos.carista.BetaEligibilityActivity`) | `false` | Core / General UI | `None` |
| `TextEditActivity` (`com.prizmos.carista.TextEditActivity`) | `false` | Core / General UI | `None` |
| `ShowAvailableToolsActivity` (`com.prizmos.carista.screens.operation.showavailabletools.ShowAvailableToolsActivity`) | `false` | Service Tools | `None` |
| `ShowLiveDataActivity` (`com.prizmos.carista.screens.operation.showlivedata.ShowLiveDataActivity`) | `false` | Live Data | `None` |
| `TpmsActivity` (`com.prizmos.carista.screens.operation.tpms.TpmsActivity`) | `false` | Service Tools | `None` |
| `LiveDataActivity` (`com.prizmos.carista.screens.operation.livedata.LiveDataActivity`) | `false` | Live Data | `None` |
| `PlaygroundActivity` (`com.prizmos.carista.PlaygroundActivity`) | `false` | Core / General UI | `None` |
| `ShowEcuListActivity` (`com.prizmos.carista.ShowEcuListActivity`) | `false` | Core / General UI | `None` |
| `ShowEcuActivity` (`com.prizmos.carista.ShowEcuActivity`) | `false` | Core / General UI | `None` |
| `InputDataIdActivity` (`com.prizmos.carista.InputDataIdActivity`) | `false` | Core / General UI | `None` |
| `ChangeBitwiseRawValueActivity` (`com.prizmos.carista.ChangeBitwiseRawValueActivity`) | `false` | Core / General UI | `None` |
| `ChangeDecimalRawValueActivity` (`com.prizmos.carista.ChangeDecimalRawValueActivity`) | `false` | Core / General UI | `None` |
| `ServiceIndicatorActivity` (`com.prizmos.carista.screens.operation.serviceindicator.ServiceIndicatorActivity`) | `false` | Service Tools | `None` |
| `NotificationRationaleActivity` (`com.prizmos.carista.NotificationRationaleActivity`) | `false` | Core / General UI | `None` |
| `FreezeFrameDataActivity` (`com.prizmos.carista.screens.operation.freezeframe.FreezeFrameDataActivity`) | `false` | Core / General UI | `None` |
| `GarageActivity` (`com.prizmos.carista.GarageActivity`) | `false` | Garage & Vehicle Management | `None` |
| `GarageHistoryActivity` (`com.prizmos.carista.screens.garage.history.GarageHistoryActivity`) | `false` | Garage & Vehicle Management | `None` |
| `DiagnosticsHistoryActivity` (`com.prizmos.carista.screens.garage.history.diagnose.DiagnosticsHistoryActivity`) | `false` | Garage & Vehicle Management | `None` |
| `FuelConsumptionActivity` (`com.prizmos.carista.screens.garage.fuelconsumption.FuelConsumptionActivity`) | `false` | Garage & Vehicle Management | `None` |
| `ServiceToolsHistoryActivity` (`com.prizmos.carista.screens.garage.history.service.ServiceToolsHistoryActivity`) | `false` | Service Tools | `None` |
| `CustomizationsHistoryActivity` (`com.prizmos.carista.CustomizationsHistoryActivity`) | `false` | Customizations / Coding | `None` |
| `FuelConsumptionInputActivity` (`com.prizmos.carista.screens.garage.fuelconsumption.input.FuelConsumptionInputActivity`) | `false` | Garage & Vehicle Management | `None` |
| `NameVehicleActivity` (`com.prizmos.carista.NameVehicleActivity`) | `false` | Garage & Vehicle Management | `None` |
| `SelectVehicleActivity` (`com.prizmos.carista.SelectVehicleActivity`) | `false` | Garage & Vehicle Management | `None` |
| `ConfirmVehicleActivity` (`com.prizmos.carista.ConfirmVehicleActivity`) | `false` | Garage & Vehicle Management | `None` |
| `MoreActivity` (`com.prizmos.carista.MoreActivity`) | `false` | Core / General UI | `None` |
| `OtpVerificationActivity` (`com.prizmos.carista.OtpVerificationActivity`) | `false` | Core / General UI | `None` |
| `IntroScreenActivity` (`com.prizmos.carista.screens.intro.IntroScreenActivity`) | `true` | Core / General UI | `None` |
| `FacebookActivity` (`com.facebook.FacebookActivity`) | `false` | Core / General UI | `None` |
| `CreateNewPasswordActivity` (`com.prizmos.carista.CreateNewPasswordActivity`) | `false` | Core / General UI | `None` |
| `WebViewActivity` (`com.prizmos.carista.WebViewActivity`) | `false` | Core / General UI | `None` |
| `AppSettingsActivity` (`com.prizmos.carista.screens.moremenu.appsettings.AppSettingsActivity`) | `false` | Customizations / Coding | `None` |
| `ThemeSettingsActivity` (`com.prizmos.carista.screens.moremenu.appsettings.theme.ThemeSettingsActivity`) | `false` | Customizations / Coding | `None` |
| `LanguageSettingsActivity` (`com.prizmos.carista.screens.moremenu.appsettings.language.LanguageSettingsActivity`) | `false` | Customizations / Coding | `None` |
| `AccountActivity` (`com.prizmos.carista.AccountActivity`) | `false` | Account & Authentication | `None` |
| `ConnectToVehicleActivity` (`com.prizmos.carista.connect.ConnectToVehicleActivity`) | `false` | Connection / Transport | `None` |
| `CustomTabActivity` (`com.facebook.CustomTabActivity`) | `true` | Core / General UI | `@7F1419CE://, fbconnect://cct.com.prizmos.carista` |
| `UnlockSettingActivity` (`com.prizmos.carista.UnlockSettingActivity`) | `false` | Customizations / Coding | `None` |
| `Enable2faActivity` (`com.prizmos.carista.Enable2faActivity`) | `false` | Core / General UI | `None` |
| `Validate2faActivity` (`com.prizmos.carista.Validate2faActivity`) | `false` | Core / General UI | `None` |
| `AiDiagnosticsActivity` (`com.prizmos.carista.screens.aidiagnostics.AiDiagnosticsActivity`) | `false` | Core / General UI | `None` |
| `ConnectInstructionsActivity` (`com.prizmos.carista.screens.connectinstructions.ConnectInstructionsActivity`) | `false` | Connection / Transport | `None` |
| `AdditionalAccountInfoActivity` (`com.prizmos.carista.AdditionalAccountInfoActivity`) | `false` | Account & Authentication | `None` |
| `BetaIntroductionActivity` (`com.prizmos.carista.BetaIntroductionActivity`) | `true` | Core / General UI | `None` |
| `ContentControlActivity` (`com.prizmos.carista.ContentControlActivity`) | `false` | Core / General UI | `None` |
| `UnitSystemActivity` (`com.prizmos.carista.screens.moremenu.appsettings.unitsystem.UnitSystemActivity`) | `false` | Customizations / Coding | `None` |
| `EmissionTestsActivity` (`com.prizmos.carista.screens.operation.emissiontests.EmissionTestsActivity`) | `false` | Core / General UI | `None` |
| `DeviceDefectiveActivity` (`com.prizmos.carista.screens.devicedefective.DeviceDefectiveActivity`) | `false` | Connection / Transport | `None` |
| `PrivacyAndTermsActivity` (`com.prizmos.carista.screens.moremenu.privacyandterms.PrivacyAndTermsActivity`) | `false` | Core / General UI | `None` |
| `CaristaLinkActivity` (`com.prizmos.carista.screens.caristalink.CaristaLinkActivity`) | `true` | Core / General UI | `http://, https://` |
| `CarHealthCheckActivity` (`com.prizmos.carista.screens.operation.carhealthcheck.CarHealthCheckActivity`) | `false` | Core / General UI | `None` |
| `BatteryHealthSummaryActivity` (`com.prizmos.carista.screens.operation.batteryhealth.BatteryHealthSummaryActivity`) | `false` | Service Tools | `None` |
| `BatteryHealthDataActivity` (`com.prizmos.carista.screens.operation.batteryhealth.viewdata.BatteryHealthDataActivity`) | `false` | Service Tools | `None` |
| `ScreenshotActivity` (`com.prizmos.carista.ScreenshotActivity`) | `false` | Core / General UI | `None` |
| `RequestActivity` (`zendesk.support.request.RequestActivity`) | `false` | Core / General UI | `None` |
| `RequestListActivity` (`zendesk.support.requestlist.RequestListActivity`) | `false` | Core / General UI | `None` |
| `ViewArticleActivity` (`zendesk.support.guide.ViewArticleActivity`) | `false` | Core / General UI | `None` |
| `HelpCenterActivity` (`zendesk.support.guide.HelpCenterActivity`) | `false` | Core / General UI | `None` |
| `MessagingActivity` (`zendesk.classic.messaging.MessagingActivity`) | `false` | Core / General UI | `None` |
| `ProxyBillingActivity` (`com.android.billingclient.api.ProxyBillingActivity`) | `false` | Billing & Subscriptions | `None` |
| `ProxyBillingActivityV2` (`com.android.billingclient.api.ProxyBillingActivityV2`) | `false` | Billing & Subscriptions | `None` |
| `NotificationOpenedActivityHMS` (`com.onesignal.NotificationOpenedActivityHMS`) | `true` | Core / General UI | `None` |
| `NotificationOpenedActivity` (`com.onesignal.notifications.activities.NotificationOpenedActivity`) | `true` | Core / General UI | `None` |
| `NotificationOpenedActivityAndroid22AndOlder` (`com.onesignal.notifications.activities.NotificationOpenedActivityAndroid22AndOlder`) | `true` | Core / General UI | `None` |
| `RefinerSurveyActivity` (`io.refiner.ui.RefinerSurveyActivity`) | `false` | Core / General UI | `None` |
| `AutocompleteActivity` (`com.google.android.libraries.places.widget.AutocompleteActivity`) | `false` | Core / General UI | `None` |
| `BasicPlaceAutocompleteActivity` (`com.google.android.libraries.places.widget.BasicPlaceAutocompleteActivity`) | `false` | Core / General UI | `None` |
| `PlaceAutocompleteActivity` (`com.google.android.libraries.places.widget.PlaceAutocompleteActivity`) | `false` | Core / General UI | `None` |
| `PlacesLightboxActivity` (`com.google.android.libraries.places.widget.internal.photoviewer.PlacesLightboxActivity`) | `false` | Core / General UI | `None` |
| `PermissionsActivity` (`com.onesignal.core.activities.PermissionsActivity`) | `false` | Core / General UI | `None` |
| `HiddenActivity` (`androidx.credentials.playservices.HiddenActivity`) | `false` | Service Tools | `None` |
| `IdentityCredentialApiHiddenActivity` (`androidx.credentials.playservices.IdentityCredentialApiHiddenActivity`) | `false` | Service Tools | `None` |
| `CustomTabMainActivity` (`com.facebook.CustomTabMainActivity`) | `false` | Core / General UI | `None` |
| `SignInHubActivity` (`com.google.android.gms.auth.api.signin.internal.SignInHubActivity`) | `false` | Account & Authentication | `None` |
| `GoogleApiActivity` (`com.google.android.gms.common.api.GoogleApiActivity`) | `false` | Core / General UI | `None` |
| `CarAppPermissionActivity` (`androidx.car.app.CarAppPermissionActivity`) | `false` | Core / General UI | `None` |
| `PlayCoreDialogWrapperActivity` (`com.google.android.play.core.common.PlayCoreDialogWrapperActivity`) | `false` | Core / General UI | `None` |
| `LicenseActivity` (`com.pairip.licensecheck.LicenseActivity`) | `false` | Core / General UI | `None` |

## 4. Native Binaries & JNI Libraries

| Library | Architecture | Size (Bytes) | Role in Diagnostic Stack |
|---|---|---|---|
| `AndroidManifest.xml` | `arm64-v8a` | 1,176 | Realm local database persistence engine |
| `stamp-cert-sha256` | `arm64-v8a` | 32 | Realm local database persistence engine |
| `libandroidx.graphics.path.so` | `arm64-v8a` | 10,096 | Realm local database persistence engine |
| `libCarista.so` | `arm64-v8a` | 29,984,992 | Core C++ OBD2/UDS/TP2.0 protocol engine, parameter database, routine controllers |
| `libdatastore_shared_counter.so` | `arm64-v8a` | 7,112 | Realm local database persistence engine |
| `librealm-jni.so` | `arm64-v8a` | 8,915,088 | Realm local database persistence engine |

## 5. Assets & Encrypted Bundles

| Asset Path | Size (Bytes) | Magic Header | Role / Verification |
|---|---|---|---|
| `1TrbQPfd7xYPDryL` | 207,591 | `0x0049415002000000` | Static asset |
| `5bgvDyZWg6hkxFFq` | 153,739 | `0x0049415002000000` | Static asset |
| `6MenowszWNfnvb6a` | 354,786 | `0x0049415002000000` | Static asset |
| `7C5MBOBd0PhPaa4D` | 159,983 | `0x0049415002000000` | Static asset |
| `7yOwujq4i9HdNipM` | 248,557 | `0x0049415002000000` | Static asset |
| `A9tABTPD9aKkvZUc` | 150,732 | `0x0049415002000000` | Static asset |
| `Dak4BY3C0ljDnDw1` | 283,938 | `0x0049415002000000` | Static asset |
| `DEUgkyVSTcYbP5d2` | 268,658 | `0x0049415002000000` | Static asset |
| `dptro4s2eyMgAsiP` | 155,384 | `0x0049415002000000` | Static asset |
| `EmeHpsFHkxc9qDcL` | 157,368 | `0x0049415002000000` | Static asset |
| `FHb79TQgYf5zo9PS` | 155,965 | `0x0049415002000000` | Static asset |
| `FHCuFw3ZIlnP7MtG` | 156,406 | `0x0049415002000000` | Static asset |
| `G6bUqOQdHdi2OyfG` | 155,311 | `0x0049415002000000` | Static asset |
| `gI1sG9Ko06stVEex` | 118,660 | `0x0049415002000000` | Static asset |
| `hDZhZmbyheBPU91Q` | 155,964 | `0x0049415002000000` | Static asset |
| `help_center_article_style.css` | 8,231 | `0x2f2a3d3d3d3d3d3d` | Static asset |
| `hLPxNj2a6qOa1NFo` | 210,374 | `0x0049415002000000` | Static asset |
| `hTzJdMXedZUctgKE` | 151,225 | `0x0049415002000000` | Static asset |
| `HYDEdcgpZXLjIITW` | 250,100 | `0x0049415002000000` | Static asset |
| `I4p6E3VR3Ut8QetQ` | 285,585 | `0x0049415002000000` | Static asset |
| `JOKKzfWuormYc7TI` | 245,660 | `0x0049415002000000` | Static asset |
| `nFmnqUWBzBvV64Xj` | 152,663 | `0x0049415002000000` | Static asset |
| `PHf7Rqd0EFLJ5qX4` | 270,457 | `0x0049415002000000` | Static asset |
| `PL1DZGYLln2s8YF0` | 159,187 | `0x0049415002000000` | Static asset |
| `PublicSuffixDatabase.list` | 132,737 | `0x000206022a2e3030` | Static asset |
| `pXiD9OWHt3eOOKNT` | 166,765 | `0x0049415002000000` | Static asset |
| `pxIjn61XWbdlZKv2` | 160,976 | `0x0049415002000000` | Static asset |
| `QvztvemRypB816KB` | 150,963 | `0x0049415002000000` | Static asset |
| `qxn7jsJPp9cOBjWV` | 210,475 | `0x0049415002000000` | Static asset |
| `R4O6xDwPW9bkRlV4` | 159,239 | `0x0049415002000000` | Static asset |
| `RcKwOiWVw1bR4q9R` | 152,669 | `0x0049415002000000` | Static asset |
| `sHhqwtQy8HAeYjEi` | 245,580 | `0x0049415002000000` | Static asset |
| `V9kmXpjp2jz4Wrwz` | 158,359 | `0x0049415002000000` | Static asset |
| `WyoMVpic6IDmgnES` | 161,832 | `0x0049415002000000` | Static asset |
| `yyFHTYb7krl2HQJd` | 208,391 | `0x0049415002000000` | Static asset |
| `z50XDfY4JF8r9Dmv` | 148,686 | `0x0049415002000000` | Static asset |
| `dexopt/baseline.prof` | 17,644 | `0x70726f0030313000` | Static asset |
| `dexopt/baseline.profm` | 2,180 | `0x70726d0030303200` | Static asset |

## 6. Permissions & Hardware Security Profile

| Permission | Protection Level |
|---|---|
| `android.permission.INTERNET` | `normal` |
| `android.permission.ACCESS_NETWORK_STATE` | `normal` |
| `android.permission.BLUETOOTH` | `normal` |
| `android.permission.BLUETOOTH_ADMIN` | `normal` |
| `android.permission.FOREGROUND_SERVICE` | `normal` |
| `android.permission.VIBRATE` | `normal` |
| `com.android.vending.BILLING` | `normal` |
| `android.permission.ACCESS_COARSE_LOCATION` | `normal` |
| `android.permission.ACCESS_FINE_LOCATION` | `normal` |
| `android.permission.BLUETOOTH_SCAN` | `normal` |
| `android.permission.BLUETOOTH_CONNECT` | `normal` |
| `android.permission.POST_NOTIFICATIONS` | `normal` |
| `android.permission.FOREGROUND_SERVICE_CONNECTED_DEVICE` | `normal` |
| `android.permission.CAMERA` | `normal` |
| `com.prizmos.carista.permission.C2D_MESSAGE` | `normal` |
| `android.permission.WAKE_LOCK` | `normal` |
| `com.google.android.c2dm.permission.RECEIVE` | `normal` |
| `android.permission.RECEIVE_BOOT_COMPLETED` | `normal` |
| `com.sec.android.provider.badge.permission.READ` | `normal` |
| `com.sec.android.provider.badge.permission.WRITE` | `normal` |
| `com.htc.launcher.permission.READ_SETTINGS` | `normal` |
| `com.htc.launcher.permission.UPDATE_SHORTCUT` | `normal` |
| `com.sonyericsson.home.permission.BROADCAST_BADGE` | `normal` |
| `com.sonymobile.home.permission.PROVIDER_INSERT_BADGE` | `normal` |
| `com.anddoes.launcher.permission.UPDATE_COUNT` | `normal` |
| `com.majeur.launcher.permission.UPDATE_BADGE` | `normal` |
| `com.huawei.android.launcher.permission.CHANGE_BADGE` | `normal` |
| `com.huawei.android.launcher.permission.READ_SETTINGS` | `normal` |
| `com.huawei.android.launcher.permission.WRITE_SETTINGS` | `normal` |
| `android.permission.READ_APP_BADGE` | `normal` |
| `com.oppo.launcher.permission.READ_SETTINGS` | `normal` |
| `com.oppo.launcher.permission.WRITE_SETTINGS` | `normal` |
| `me.everything.badger.permission.BADGE_COUNT_READ` | `normal` |
| `me.everything.badger.permission.BADGE_COUNT_WRITE` | `normal` |
| `com.google.android.gms.permission.AD_ID` | `normal` |
| `android.permission.ACCESS_ADSERVICES_ATTRIBUTION` | `normal` |
| `android.permission.ACCESS_ADSERVICES_AD_ID` | `normal` |
| `android.permission.ACCESS_WIFI_STATE` | `normal` |
| `android.permission.USE_BIOMETRIC` | `normal` |
| `android.permission.USE_FINGERPRINT` | `normal` |
| `com.google.android.finsky.permission.BIND_GET_INSTALL_REFERRER_SERVICE` | `normal` |
| `android.permission.ACCESS_ADSERVICES_CUSTOM_AUDIENCE` | `normal` |
| `android.permission.ACCESS_ADSERVICES_TOPICS` | `normal` |
| `com.prizmos.carista.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION` | `normal` |
| `com.android.vending.CHECK_LICENSE` | `normal` |

