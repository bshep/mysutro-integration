# Sutro GraphQL API: Command Reference

This document provides an overview of possible GraphQL queries and mutations ("commands") you can send to the Sutro service to retrieve or manipulate data. The actual schema is defined in `schemaOut2.txt`.

## Common Query Commands

Below are typical queries you might use to retrieve data from the Sutro service:

### 1. Get Device Status
```graphql
query GetDeviceStatus($deviceId: ID!) {
  device(id: $deviceId) {
    id
    name
    status
    lastReading {
      timestamp
      ph
      orp
      temperature
      ...
    }
  }
}
```

### 2. List All Devices
```graphql
---
# Sutro GraphQL API: Full Command Reference

This document provides a comprehensive, up-to-date reference for all GraphQL queries and mutations ("commands") available in the Sutro API, based on the current schema. Each command lists its arguments and a brief description. Deprecated actions are noted.

---

## Queries

### cartridgeHistory
**Args:** `deviceId: Int!`
> Gets all cartridges used by a device.

### checkMoveSutroSession
**Args:** `id: Int!`
> Get the move Sutro session by id.

### chemicals
**Args:** `params: ChemicalQueryParams`, `upc: String` (deprecated)
> Query the chemical products database. Filter by params or UPC.

### chemicalsUsed
**Args:** `poolId: ID`, `sinceSetup: Boolean`, `startDate: DateTime`, `userEmail: String!`
> Get chemical amounts used in a time range.

### defaultPoolProfile
**Args:** none
> Get the default pool profile.

### getCurrentTestTimes
**Args:** `deviceId: ID`, `userEmail: String`
> Get current test intervals for a device or user.

### getDevicesNeedingNewCartridges
**Args:** `activeSubscriptionOnly: Boolean`, `cartridgeCountMax: Int`, `cartridgeCountMin: Int`, `cartridgeCountNewerThan: DateTime`, `onlineOnly: Boolean`, `page: Int`, `pageSize: Int`, `poolStore: String`, `sssDevicesOnly: Boolean`
> List devices needing new cartridges, with filters.

### getPool
**Args:** `poolId: Int!`
> Get a pool and all connected data by pool id.

### getRechargePaymentMethods
**Args:** `email: String!`
> Get Recharge payment methods for a user.

### getRecurringTestTimes
**Args:** `deviceId: ID`, `userEmail: String`
> Get most up-to-date test intervals for a device or user.

### history
**Args:** `deviceId: ID`, `deviceSerial: String`, `endDate: DateTime`, `limit: Int`, `startDate: DateTime`, `types: [HistoryType]`
> Get historical info linked to a device.

### home
**Args:** `homeId: ID`
> Get a home by id (or primary home if not provided).

### manualReadingsInLastDay
**Args:** `deviceId: Int!`, `readingType: ReadingTypeQuery!`
> Count manual readings for a device in the last 24 hours.

### me
**Args:** none
> Query properties and associations of the currently logged-in user.

### poolProfiles
**Args:** `profileType: PoolType`
> List available pool profiles by type.

### poolStoreUsers
**Args:** `poolStores: [String]`
> List users associated with given pool stores.

### sanitizers
**Args:** `profileType: PoolType`
> List available sanitizers by pool type.

### searchMesData
**Args:** `getHistory: Boolean`, `includedFields: [MesSearchFieldType]`, `page: Int`, `pageSize: Int`, `queryString: String!`
> Search MES data with filters.

### selectPrimaryPoolStore
**Args:** `page: Int`, `poolId: ID`, `search: String`, `tokenId: String`
> Select the primary pool store from Sutro Central.

### user
**Args:** `email: String`, `id: ID`, `rechargeSubscriptionEmail: String`
> Query properties and associations of any user by id or email.

### users
**Args:** `activeSubscriptionOnly: Boolean`, `includedFields: [UserSearchFieldType]`, `includedUserTypes: [UserSearchUserType]`, `page: Int`, `pageSize: Int`, `queryString: String`, `readingsEnabled: Boolean`, `subscriptionClass: String`, `updatedSince: DateTime`
> List all users with filters.

### webhookListeners
**Args:** none
> List all registered webhook listeners for the user.

---

## Mutations

### Device & Hardware Actions
- **associateDevice**: `serialNumber: String!` — Associate a device with the current user.
- **toggleTakeReadings**: `deviceSerial: String!` — Pause or resume readings on a device.
- **resetDeviceHealth**: `deviceSerial: String!`, `closeCalibrationSessions: Boolean!`, `closeServiceSessions: Boolean!` — Reset device health to "good" and optionally close sessions.
- **resetAutoretractRetry**: `deviceId: ID` — Reset a device's autoretract retry count.
- **rmaHardware**: `deviceSerial: String`, `hubSerial: String`, `reason: String!` — Mark a device or hub as returned (RMA).
- **refreshHardwareStatus**: `deviceId: ID` — Refresh the status of the user's hub and device.
- **doReadinessCheck**: none — Start a readiness check session for the device.
- **createCalibrationSession**: `deviceId: Int` — Open a new calibration session for the device.
- **passCalibration**: `deviceSerial: String`, `sessionId: Int` — Force a calibration session to pass.
- **forceStopCalibration**: `deviceSerial: String!` — Force a calibration session to stop and timeout.
- **deleteCalibrationSession**: `deviceSerial: String!` — Permanently delete a calibration session.
- **createServiceModeSessionReadinessCheck**: `deviceId: Int` — Open a new service session with readiness check.
- **passServiceMode**: `deviceSerial: String`, `sessionId: Int` — Force a service session to pass.
- **deleteServiceSession**: `deviceSerial: String!` — Permanently delete a service session.
- **finishServiceModeSession**: `deviceId: Int` — Finish a service session.
- **setDeviceNeedsService**: `deviceId: Int` — Set device health to needs_service.
- **updateWebhookListener**: `listenerId: Int!`, `name: String`, `webhookUrl: String`, `bearerToken: String` — Update a webhook listener.
- **createWebhookListener**: `name: String!`, `webhookUrl: String!`, `bearerToken: String` — Create a new webhook listener.
- **getWebhookRegistrationToken**: `deviceSerial: String!` — Generate a token for registering a webhook listener.
- **dissociateDevicesAndHubs**: `devices: [String]`, `hubs: [String]` — Dissociate devices and hubs.
- **rmaHardware**: `deviceSerial: String`, `hubSerial: String`, `reason: String!` — Mark a device or hub as RMA'd.
- **registerCartridge**: `serialNumber: String!`, `deviceId: Int` — Register a cartridge to a device.

### Pool & Profile Actions
- **updatePool**: `params: UpdatePoolOptions!`, `poolId: ID` — Set or change pool and pool profile details.
- **storePoolDetails**: `gallons: Int`, `saltwater: Boolean`, `type: PoolType` — (Deprecated) Set or change pool details.
- **openPool**: `poolId: Int`, `sutroEmail: String!` — Open a closed pool.
- **closePool**: `sutroEmail: String!`, `willReopenOn: DateTime!` — Close a pool.
- **syncPoolSutroCentral**: `poolId: Int!` — Sync a pool to Sutro Central.
- **createPool**: `homeId: ID!`, `type: String!`, `gallons: Float!`, `saltwater: Boolean`, `name: String`, `sanitizer: PoolProfileSanitizer!`, `options: [PoolProfileOption]` — Create a new pool.
- **editPool**: `poolId: ID!`, `params: UpdatePoolOptions!` — Edit an existing pool.
- **dissociatePool**: `poolId: ID!` — Dissociate a pool from a user.

### Chemical Actions
- **assignChemical**: `params: AssignChemicalParams` — Assign a chemical to the user's chemical profile by UPC and optional role.
- **unassignChemical**: `poolId: ID`, `role: AssignableChemicalType!` — Unassign a chemical from a specific role in the chemical profile.
- **addChemical**: `chemicalUpc: String!`, `profileBucket: ProfileBucket` — (Deprecated) Add a chemical by UPC to a profile bucket.
- **setChemical**: `chemicalId: String!`, `profileBucket: ProfileBucket!` — (Deprecated) Assign a chemical by ID to a profile bucket.
- **importChemicals**: `csv: Upload!`, `excludeImageLookup: Boolean`, `headerRows: Int` — Import chemical data from a CSV file.

### User & Account Actions
- **signup**: `firstName: String!`, `lastName: String!`, `email: String!`, `password: String!`, `phone: String!`, `language: Language`, `type: SutroUserType` — Sign up a new user.
- **login**: `email: String!`, `password: String!`, `language: Language` — Log in an existing user.
- **poolmasterUserSignup**: `firstName: String!`, `lastName: String!`, `email: String!`, `phone: String!` — Sign up a new PoolMaster user (no password).
- **updateUserPassword**: `password: String!` — Change the password of the current user.
- **requestPasswordReset**: `email: String!`, `language: Language` — Request a password reset for a user.
- **resetUserPassword**: `password: String!`, `token: String!`, `language: Language` — Reset a user's password.
- **editUserProfile**: `email: String`, `firstName: String`, `lastName: String`, `phone: String` — Update the profile details of the current user.

### Recommendations & Readings
- **completeRecommendation**: `recommendationId: ID!`, `completedAt: DateTime` — Mark a recommendation as completed or incomplete.
- **setProblemCompletion**: `readingId: ID!`, `problemIndex: Int!`, `completedAt: NaiveDateTime` — (Deprecated) Mark a treatment recommendation as completed.
- **setRecurringTestTimes**: `hours: [Int]!`, `userEmail: String`, `deviceId: ID`, `bypassHourSpaceCheck: Boolean` — Set recurring test times for a device or user.
- **setTemporaryTestTimes**: `hours: [Int]!`, `userEmail: String`, `deviceId: ID`, `bypassHourSpaceCheck: Boolean` — Set temporary test times for a device or user (for today only).

### Notifications & Messaging
- **addFcmToken**: `token: String!` — Add an FCM token to the current user.
- **deleteFcmToken**: `token: String!` — Delete an FCM token for the current user.
- **sendNotification**: `params: SendNotificationParams!` — Send a notification or data message to specific users/devices.
- **multicastNotification**: `userGroup: MulticastUserGroup!`, `notificationType: NotificationType!`, `title: String`, `body: String`, `dataMessageType: String`, `dataMessagePayload: String`, `inactiveMinutes: Int` — Send a notification to a group of users.

### Subscription & Payment Actions
- **setupCustomerSubscription**: `params: SetupCustomerSubscriptionParams!` — Set up a subscription for a user.
- **setupCustomerPaymentAndShipments**: `params: SetupCustomerPaymentAndShipmentsParams!` — Set up payment and shipments for a user.
- **updateRechargeCustomer**: `rechargeSubscriptionEmail: String!`, `rechargeSubscriptionId: String` — Update a Recharge subscription for a user.
- **linkRechargeSubscription**: `sutroUserEmail: String!`, `rechargeSubscriptionEmail: String!`, `overwriteIfExists: Boolean` — Link a Recharge subscription to a Sutro user.
- **cancelSubscription**: `rechargeEmail: String`, `reason: String!`, `comments: String`, `sendEmail: Boolean!` — Cancel a subscription.
- **reactivateSubscription**: `rechargeEmail: String!`, `rechargeSubscriptionId: String!` — Reactivate a cancelled subscription.
- **giveFreeMonths**: `sutroUserEmail: String`, `rechargeSubscriptionEmail: String`, `freeMonths: Int`, `lastRechargeOrderDate: DateTime` — Give a user free months of subscription time.
- **linkPaymentMethod**: `params: LinkPaymentMethodParams!` — Link a payment method to a Recharge customer.
- **deletePaymentMethod**: `rechargePaymentMethodId: String!` — Delete a Recharge payment method.
- **updateCustomerSubscriptionType**: `externalVariantId: String!`, `price: String!`, `rechargeEmail: String!`, `rechargeSubscriptionId: ID` — Change a customer's subscription type.
- **updateCustomerAddress**: `params: UpdateCustomerAddressParams!` — Change a customer's address.

### Firmware & Release Actions
- **uploadHubFirmware**: `file: Upload!`, `firmwareVersion: String!` — Upload a new hub firmware version.
- **uploadMonitorFirmware**: `file: Upload!`, `firmwareVersion: String!` — Upload a new monitor firmware version.
- **createFirmwareRelease**: `releaseGroup: ReleaseGroupType!`, `hubVersion: String!`, `monitorVersion: String!`, `monitorFirst: Boolean!` — Create a new firmware release for a group.
- **getLatestRelease**: `releaseGroup: ReleaseGroupType!` — Get the latest firmware release for a group.
- **changeReleaseGroup**: `email: String!`, `releaseGroup: ReleaseGroupType!`, `deviceId: ID` — Change the release group for a user's hardware.

### Miscellaneous Actions
- **addSubscriptionRule**: `pattern: String!`, `exempt: Boolean!` — Add a subscription rule for email patterns.
- **importMesData**: `csv: Upload!` — Import MES data from a CSV file.
- **importPoolStoreData**: `csv: Upload!`, `poolStoreName: String!` — Import pool store data from a CSV file.
- **associateHub**: `email: String!`, `serialNumber: String!`, `poolId: Int` — Associate a hub with a user.
- **poolmasterSetup**: `deviceSerialNumber: String!`, `hubSerialNumber: String!`, `userEmail: String!` — Associate a device, hub, and user.
- **log**: `message: String!` — Log messages from the app.

---

> For each action, refer to the schema for required arguments and possible return values. Some actions are deprecated and should be replaced with their newer alternatives as noted.

## Notes
- Replace variables (e.g., `$deviceId`, `$from`, `$to`) with actual values.
- The exact fields and types may vary; refer to the schema for all available fields and types.
- Use introspection queries or tools like GraphiQL to explore the full schema.

---

*This documentation is auto-generated based on the available GraphQL schema. For more details, see `schema.graphql`.*
  - Args: `deviceSerial: String!`, `sessionId: String` (optional)
- **deleteServiceSession**: Permanently delete a service session.
  - Args: `deviceSerial: String!`
- **finishServiceModeSession**: Finish a service session.
  - Args: none
- **cancelServiceModeSession**: Cancel a service session.
  - Args: none
- **finishReconnect**: Finish the reconnection step in a service session.
  - Args: none

### Pool & Profile Actions
- **updatePool**: Set or change pool and pool profile details.
  - Args: `params: UpdatePoolOptions!`
- **setPoolProfile**: Set or change the pool profile for a user.
  - Args: `id: ID!`, `email: String!`
- **closePool**: Close a pool (pauses shipments, cancels subscription, etc.).
  - Args: `sutroEmail: String!`, `willReopenOn: DateTime!`
- **openPool**: Open a closed pool (resumes shipments, subscription, etc.).
  - Args: `sutroEmail: String!`
- **storePoolDetails**: (Deprecated) Set or change pool details.
  - Args: `gallons: Int`, `saltwater: Boolean`, `type: PoolType`

### Chemical Actions
- **assignChemical**: Assign a chemical to the user's chemical profile by UPC and optional role.
  - Args: `upc: String!`, `role: AssignableChemicalType` (optional)
- **unassignChemical**: Unassign a chemical from a specific role in the chemical profile.
  - Args: `role: AssignableChemicalType!`
- **addChemical**: (Deprecated) Add a chemical by UPC to a profile bucket.
  - Args: `chemicalUpc: String!`, `profileBucket: ProfileBucket`
- **setChemical**: (Deprecated) Assign a chemical by ID to a profile bucket.
  - Args: `chemicalId: String!`, `profileBucket: ProfileBucket!`
- **importChemicals**: Import chemical data from a CSV file.
  - Args: `csv: Upload!`, `excludeImageLookup: Boolean`, `headerRows: Int`

### User & Account Actions
- **signup**: Sign up a new user.
  - Args: `firstName: String!`, `lastName: String!`, `email: String!`, `password: String!`, `phone: String!`
- **login**: Log in an existing user.
  - Args: `email: String!`, `password: String!`
- **poolmasterUserSignup**: Sign up a new PoolMaster user (no password).
  - Args: `firstName: String!`, `lastName: String!`, `email: String!`, `phone: String!`
- **updateUserProfile**: Update the profile details of the current user.
  - Args: `email: String`, `firstName: String`, `lastName: String`, `phone: String`
- **updateUserPassword**: Change the password of the current user.
  - Args: `password: String!`
- **requestPasswordReset**: Request a password reset for a user.
  - Args: `email: String!`
- **resetUserPassword**: Reset a user's password.
  - Args: `password: String!`, `token: String!`

### Recommendations & Readings
- **analyzeReading**: Analyze a reading and get recommendations (one-off, not saved).
  - Args: `params: AnalyzeReadingParams!`
- **getRawRecommendation**: Get raw recommendations for a reading (one-off, not saved).
  - Args: `params: AnalyzeReadingParams!`
- **setProblemCompletion**: (Deprecated) Mark a treatment recommendation as completed.
  - Args: `readingId: ID!`, `problemIndex: Int!`, `completedAt: NaiveDateTime`
- **completeRecommendation**: Mark a recommendation as completed or incomplete.
  - Args: `recommendationId: ID!`, `completedAt: DateTime`

### Notifications & Messaging
- **addFcmToken**: Add an FCM token to the current user.
  - Args: `token: String!`
- **deleteFcmToken**: Delete an FCM token for the current user.
  - Args: `token: String!`
- **sendNotification**: Send a notification or data message to specific users/devices.
  - Args: `params: SendNotificationParams!`
- **multicastNotification**: Send a notification or data message to a group of users.
  - Args: `userGroup: MulticastUserGroup!`, `notificationType: NotificationType!`, `title: String`, `body: String`, `dataMessageType: String`, `dataMessagePayload: String`, `inactiveMinutes: Int`

### Subscription & Payment Actions
- **setupCustomerSubscription**: Set up a subscription for a user.
  - Args: `params: SetupCustomerSubscriptionParams!`
- **setupCustomerPaymentAndShipments**: Set up payment and shipments for a user.
  - Args: `params: SetupCustomerPaymentAndShipmentsParams!`
- **updateRechargeSubscription**: Update a Recharge subscription for a user.
  - Args: `sutroUserEmail: String`, `rechargeSubscriptionEmail: String`
- **linkRechargeSubscription**: Link a Recharge subscription to a Sutro user.
  - Args: `sutroUserEmail: String!`, `rechargeSubscriptionEmail: String!`, `overwriteIfExists: Boolean`
- **cancelSubscription**: Cancel a subscription.
  - Args: `rechargeEmail: String`, `reason: String!`, `comments: String`, `sendEmail: Boolean!`
- **reactivateSubscription**: Reactivate a cancelled subscription.
  - Args: `subscriptionId: String!`, `rechargeEmail: String!`
- **giveFreeMonths**: Give a user free months of subscription time.
  - Args: `sutroUserEmail: String`, `rechargeSubscriptionEmail: String`, `freeMonths: Int`, `lastRechargeOrderDate: DateTime`
- **linkPaymentMethod**: Link a payment method to a Recharge customer.
  - Args: `params: LinkPaymentMethodParams!`
- **deletePaymentMethod**: Delete a Recharge payment method.
  - Args: `rechargePaymentMethodId: String!`
- **updateCustomerSubscriptionType**: Change a customer's subscription type.
  - Args: `rechargeEmail: String!`, `externalVariantId: String!`, `price: String!`
- **updateCustomerAddress**: Change a customer's address.
  - Args: `params: UpdateCustomerAddressParams!`

### Firmware & Release Actions
- **uploadHubFirmware**: Upload a new hub firmware version.
  - Args: `file: Upload!`, `firmwareVersion: String!`
- **uploadMonitorFirmware**: Upload a new monitor firmware version.
  - Args: `file: Upload!`, `firmwareVersion: String!`
- **createFirmwareRelease**: Create a new firmware release for a group.
  - Args: `releaseGroup: ReleaseGroupType!`, `hubVersion: String!`, `monitorVersion: String!`, `monitorFirst: Boolean!`
- **getLatestRelease**: Get the latest firmware release for a group.
  - Args: `releaseGroup: ReleaseGroupType!`
- **changeReleaseGroup**: Change the release group for a user's hardware.
  - Args: `email: String!`, `releaseGroup: ReleaseGroupType!`

### Miscellaneous Actions
- **addSubscriptionRule**: Add a subscription rule for email patterns.
  - Args: `pattern: String!`, `exempt: Boolean!`
- **importMesData**: Import MES data from a CSV file.
  - Args: `csv: Upload!`
- **importPoolStoreData**: Import pool store data from a CSV file.
  - Args: `csv: Upload!`, `poolStoreName: String!`
- **associateHub**: Associate a hub with a user.
  - Args: `email: String!`, `serialNumber: String!`
- **poolmasterSetup**: Associate a device, hub, and user.
  - Args: `deviceSerialNumber: String!`, `hubSerialNumber: String!`, `userEmail: String!`
- **dissociateDevicesAndHubs**: Dissociate devices and hubs.
  - Args: `devices: [String]`, `hubs: [String]`
- **setupCustomerSubscription**: Set up a subscription for a user.
  - Args: `params: SetupCustomerSubscriptionParams!`
- **log**: Log messages from the app.
  - Args: `message: String!`

> For each action, refer to the schema for required arguments and possible return values. Some actions are deprecated and should be replaced with their newer alternatives as noted.

## Notes
- Replace variables (e.g., `$deviceId`, `$from`, `$to`) with actual values.
- The exact fields and types may vary; refer to the schema for all available fields and types.
- Use introspection queries or tools like GraphiQL to explore the full schema.

---

*This documentation is auto-generated based on the available GraphQL schema. For more details, see `schemaOut2.txt`.*
