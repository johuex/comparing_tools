# Comparing different tools

## Web API server & skeleton

All Web API servers & skeletons are tested by [WRK](https://github.com/wg/wrk) benchmark tool.

Default command for verification:
`wrk -t12 -c400 -d30s http://localhost:{port}/`
* t12 -- 12 threads
* c400 -- 400 connections
* 30s -- test in 30 seconds

### Python
| Tool | Description | Benchmark values, req/sec | Comparing with min|
|---|---|---|---|
| `Flask + gunicorn` | 8 workers (processes) | 18774 | + 955% |
| `aiohttp` | default, 1 thread | 12600 | + 641 % |
| `aiohttp + gunicorn` | 1 worker (process) | 23037 | + 1172% |
| `aiohttp + gunicorn` | 8 workers (processes) | 94071 | + 4789% |
| `FastAPI + uvicorn` | 1 worker (process) | 1964 | 0 |
| `FastAPI + uvicorn` | 8 workers (processes) | 9518 | + 484 % |
| `starlette + uvicorn` | 1 worker (process) | 3814 | + 194% |
| `starlette + uvicorn` | 8 worker (processes) | 15080 | + 804% |



### Golang
| Tool | Description | Benchmark values | Comparing, %|
|---|---|---|---|
| `some tool` | nil | 0 | 0 |

### C++
| Tool | Description | Benchmark values | Comparing, %|
|---|---|---|---|
| `some tool` | null | 0 | 0 |


## HTTP adapters

### Python
| Tool | Description | Benchmark values | Comparing, %|
|---|---|---|---|
| `requests + threads` | 8 threads | 0 | 0 |
| `aiohttp` | None | 0 | 0 |

### Go
| Tool | Description | Benchmark values | Comparing, %|
|---|---|---|---|
| `some tool` | null | 0 | 0 |

### C++
| Tool | Description | Benchmark values | Comparing, %|
|---|---|---|---|
| `some tool` | null | 0 | 0 |

## DB adapters

### Python
| Tool | Description | Benchmark values | Comparing, %|
|---|---|---|---|
| `psycopg` | 8 workers in WSGI | 0 | 0 |
| `asyncpg` | None | 0 | 0 |

### Golang
| Tool | Description | Benchmark values | Comparing, %|
|---|---|---|---|
| `some tool` | null | 0 | 0 |

### C++
| Tool | Description | Benchmark values | Comparing, %|
|---|---|---|---|
| `some tool` | null | 0 | 0 |
