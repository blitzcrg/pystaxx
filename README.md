# pystaxx
Utility for pulling IOCs from an [Anomali STAXX](https://www.anomali.com/platform/staxx) server formatted as JSON (default) or CSV. Accepts any properly formatted STAXX query (read the [STAXX user guide](https://update.anomali.com/staxx/docs/Anomali_STAXX_Installation_&_Administration_Guide_v2.2.pdf)).
```
usage: pystaxx.py [-h] [-f {j,c}] [-p PATH] [-n NAME] query

positional arguments:
  query                 A valid Anomali STAXX API query.

optional arguments:
  -h, --help            show this help message and exit
  -f {j,c}, --format {j,c}
                        Output file format. Default is 'j' (JSON).
  -p PATH, --path PATH  Output path. Defaults to working directory.
  -n NAME, --name NAME  Output filename. Defaults to 'iocs'.
```
