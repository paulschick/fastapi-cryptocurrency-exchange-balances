# FastAPI Cryptocurrency Exchange Balances

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple FastAPI project for fetching balances from cryptocurrency exchanges.
Redis is used as a short-term cache, and the API has a `force` option which causes
it to refresh the balances in the cache.

I will add usage notes, I built this mainly for the purpose of learning the technologies
that were used (Python Docker images, FastAPI, Redis).

**TODO**: change python image to use Alpine
