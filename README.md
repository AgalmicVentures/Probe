# Probe

Probe is a server status microservice in Python 3 built on CherryPy. It provides information about
the configuration and status of its host.

## API's

### `/json/status`
Returns the status of the host

    {
      "battery": {
        "percent": 100,
        "pluggedIn": true,
        "secsleft": -2
      },
      "bootTime": "2018-04-03T18:27:12Z",
      "cpuCores": 8,
      "cpuFrequencyMhz": {
        "current": 3100,
        "max": 3100,
        "min": 3100
      },
      "cpuPercent": 2.4,
      "cpuStats": {
        "contextSwitches": 349244,
        "interrupts": 717613,
        "softInterrupts": 314539200,
        "syscalls": 886756
      },
      "cpuTimes": {
        "idle": 831135.67,
        "nice": 0.0,
        "system": 26969.3,
        "user": 71396.73
      },
      "diskIoCounters": {
        "readBytes": 34888589312,
        "readCount": 1967279,
        "readTime": 721062,
        "writeBytes": 21125185536,
        "writeCount": 1328397,
        "writeTime": 1189483
      },
      "entropyAvailable": null,
      "hostname": "mbp-ch-0.local",
      "isMac": true,
      "network": {
        "bytesReceived": 5606532096,
        "bytesSent": 497655808,
        "dropsIn": 0,
        "dropsOut": 0,
        "errorsIn": 0,
        "errorsOut": 0,
        "packetsReceived": 5373893,
        "packetsSent": 2844076
      },
      "swapMemory": {
        "free": 924581888,
        "in": 18807443456,
        "out": 152272896,
        "percent": 13.9,
        "total": 1073741824,
        "used": 149159936
      },
      "time": "2018-04-06 01:23:17",
      "uptime": 197765,
      "virtualMemory": {
        "available": 4984897536,
        "free": 1352744960,
        "percent": 71.0,
        "total": 17179869184,
        "used": 12080500736
      }
    }