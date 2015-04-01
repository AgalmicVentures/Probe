# Probe

Probe is a server status microservice in Python 3 built on CherryPy. It provides information about
the configuration and status of its host.

## API's

### `/json/hardware`
Returns metadata about the hardware configuration of the host:

    {
        "bootTime": "2015-04-01 16:13:36",
        "cpuCores": 8,
        "isMac": true,
        "ram": 34359738368
    }

### `/json/status`
Returns the status of the host:

    {
        "cpuPercent": 6.2,
        "network": {
            "bytesReceived": 1263493884,
            "bytesSent": 28357683,
            "droppedIn": 0,
            "droppedOut": 0,
            "errorIn": 0,
            "errorOut": 0,
            "packetsReceived": 995334,
            "packetsSent": 378404
        },
        "swapMemory": {
            "free": 0,
            "in": 8954613760,
            "out": 0,
            "percent": 0,
            "total": 0,
            "used": 0
        },
        "time": "2015-04-01 18:56:09",
        "uptime": 9753,
        "virtualMemory": {
            "available": 26116472832,
            "free": 24501407744,
            "percent": 24.0,
            "total": 34359738368,
            "used": 9848811520
        }
    }