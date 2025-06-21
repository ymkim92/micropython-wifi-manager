# State

| State          | Entry Function          | Exit Function        | Description (optional)                          |
| -------------- | ----------------------- | -------------------- | ----------------------------------------------- |
| `INIT`         | `OnEntryInit()`         | `OnExitInit()`       | Initial state, performs system/init setup       |
| `CONNECTING`   | `OnEntryConnecting()`   | `OnExitConnecting()` | Attempting to connect using saved config        |
| `AP_MODE`      | `OnEntryAPMode()`       | *(none)*             | Starts AP mode for user configuration           |
| `RECONNECTING` | `OnEntryReconnecting()` | *(none)*             | Attempts connection using newly received config |
| `CONNECTED`    | `OnEntryConnected()`    | *(none)*             | Device is successfully connected                |
| `FAILED`       | `OnEntryFailed()`       | *(none)*             | Connection attempts have failed                 |

---

# Event

| Event                 | Triggered From        | Description                            |
| --------------------- | --------------------- | -------------------------------------- |
| `ConnectRequestEvent` | External trigger      | system requests connection             |
| `ConnectedEvent`      | After connect attempt | Connection was successful              |
| `ConnectFailedEvent`  | After connect attempt | Connection attempt failed              |
| `ConfigReceivedEvent` | In AP mode            | User submitted new Wi-Fi configuration |

# Action

| Action Name                      | Description                                             |
| -------------------------------- | ------------------------------------------------------- |
| `OnActionConnectToSaved()`       | Initiates connection using saved Wi-Fi credentials      |
| `OnActionStartAP()`              | Switches device to AP mode for user setup               |
| `OnActionNotifyConnected()`      | Notifies system that connection succeeded               |
| `OnActionConnectWithNewConfig()` | Connects using user-supplied credentials (from AP mode) |
| `OnActionLogError()`             | Logs error or takes failure handling actions            |

---

# Guard

| Guard Name              | Description                                            |
| ----------------------- | ------------------------------------------------------ |
| `GuardHasSavedConfig()` | Returns true if valid saved Wi-Fi configuration exists |


# FSM Diagram

```plantuml
@startuml
state INIT : +entry/OnEntryInit()\n+exit/OnExitInit()
state CONNECTING : +entry/OnEntryConnecting()\n+exit/OnExitConnecting()
state AP_MODE : +entry/OnEntryAPMode()
state RECONNECTING : +entry/OnEntryReconnecting()
state CONNECTED : +entry/OnEntryConnected()
state FAILED : +entry/OnEntryFailed()

[*] --> INIT

INIT --> CONNECTING : ConnectRequestEvent\n[GuardHasSavedConfig()]\n/ OnActionConnectToSaved()
INIT --> AP_MODE : ConnectRequestEvent\n[!GuardHasSavedConfig()]\n/ OnActionStartAP()

CONNECTING --> CONNECTED : ConnectedEvent\n/ OnActionNotifyConnected()
CONNECTING --> AP_MODE : ConnectFailedEvent\n/ OnActionStartAP()

AP_MODE --> RECONNECTING : ConfigReceivedEvent\n/ OnActionConnectWithNewConfig()

RECONNECTING --> CONNECTED : ConnectedEvent\n/ OnActionNotifyConnected()
RECONNECTING --> FAILED : ConnectFailedEvent\n/ OnActionLogError()
@enduml
```