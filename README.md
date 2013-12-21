A simple tool to wait for a systemd unit to enter a specific state.

# Usage

```
usage: systemd-wait [-h] [-q] [--user] unit [STATE ...]

positional arguments:
  unit                  Unit for which to wait
  STATE ...             States for which to wait. Any combination of {
                          active,
                          reloading,
                          inactive,
                          failed,
                          activating,
                          deactivating
                        }

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Don't print resulting state
  --user                Connect to user service manager
```
