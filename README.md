# Probe

Probe is a server status microservice in Python 3 built on CherryPy. It provides information about
the configuration and status of its host.

## API's

### `/json/status`
Returns the status of the host:

    {
        "battery": null,
        "cpuPercent": 0.0,
        "cpuStats": {
            "contextSwitches": 5488987545,
            "interrupts": 1518314732,
            "softInterrupts": 612327022,
            "syscalls": 0
        },
        "cpuTimes": {
            "idle": 63356063.21,
            "nice": 249.94,
            "system": 69785.35,
            "user": 209150.38
        },
        "diskIoCounters": {
            "readBytes": 81790133248,
            "readCount": 611528,
            "readTime": 502056,
            "writeBytes": 533914533888,
            "writeCount": 15838132,
            "writeTime": 47048748
        },
        "entropyAvailable": 822,
        "network": {
            "bytesReceived": 36782677828,
            "bytesSent": 78145677942,
            "droppedIn": 0,
            "droppedOut": 0,
            "errorIn": 0,
            "errorOut": 0,
            "packetsReceived": 56417513,
            "packetsSent": 70042342
        },
        "swapMemory": {
            "free": 0,
            "in": 0,
            "out": 0,
            "percent": 0,
            "total": 0,
            "used": 0
        },
        "time": "2018-02-19 17:55:07",
        "uptime": 3185738,
        "virtualMemory": {
            "available": 118081093632,
            "free": 11270242304,
            "percent": 12.6,
            "total": 135070191616,
            "used": 16359809024
        }
    }