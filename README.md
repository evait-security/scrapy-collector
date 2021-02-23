# scrapy-collector

A collection of website spiders. At this time, we only have one spider (mailcollect).

## Installation / Usage

### For users

- Install scrapy from your distro's packaging or look at https://github.com/scrapy/scrapy
- Download the spiders you want to use:
  - download manually from https://github.com/evait-security/scrapy-collector/tree/main/scrapy_collector/spiders/
  - or use svn: `svn export https://github.com/evait-security/scrapy-collector/trunk/scrapy_collector/spiders/`
- `scrapy runspider <path-to-spider> <options>` (see examples below)

### For developers

Familiarize yourself with scrapy.

`git clone git@github.com:evait-security/scrapy-collector.git`

`cd scrapy-collector/`

`pipenv shell` (or your prefered way to initiate a virtualenv)

`pipenv install` (pip users: `python -m pip install -r requirements.txt`)

`cd scrapy scrapy_collector/`

`scrapy crawl <spider> <options>` (see examples below)

---

## Spiders

### mailcollect

Tries to collect email addresses from a given domain. Will follow internal links, including subdomains. Does not filter collected mail addresses from other domains, all found addresses are included in the results. Optionally outputs the crawled paths.

| Options                     |                                                                                                                                                                  |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-a target=<target-domain>` | The domain to be crawled. Subdomains will be included automatically (if they are linked within the page)                                                         |
| `-a show-paths=true`        | Optional. Include the crawled paths in the output file                                                                                                           |
| `-O outfile.json`           | Write results to outfile, in JSON format. Other formats are available too (see https://docs.scrapy.org/en/latest/topics/feed-exports.html#serialization-formats) |

#### Usage examples:

`scrapy runspider mailcollect.py -a target=<target-domain> -O outfile.json`

`scrapy runspider mailcollect.py -a target=<target-domain> -O outfile.json -a show-paths=true`

---
