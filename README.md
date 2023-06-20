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
| `FastAPI + uvicorn` | 8 workers (processes) | 9518 | + 484% |
| `starlette + uvicorn` | 1 worker (process) | 3814 | + 194% |
| `starlette + uvicorn` | 8 worker (processes) | 15080 | + 804% |



### Golang
For default use all 16 threads
| Tool | Description | Benchmark values, req/sec | Comparing, %|
|---|---|---|---|
| `net/http` | - | 285423 | + 774% |
| `fasthttp` | - | 414538 | + 1124% |
| `gin` | ReleaseMode + Logs + JSON Answer | 65424 | + 177% |
| `echo` | with Logger middleware | 36848 | 0% |
| `echo` | without Logger middleware | 326130 | + 885% |
| `fiber` | - | 508505 | + 1380% |
| `aero` | - | 342943 | + 930% |

### C++
| Tool | Description | Benchmark values | Comparing, %|
|---|---|---|---|
| `some tool` | null | - | - |

### Conclusion



## HTTP adapters

In this section benchmark consists of 10000 requests to 1-thread aiohttp server on local machine.

### Python
| Tool | Description | Benchmark values, sec | Comparing, %|
|---|---|---|---|
| `requests + threads` | 8 threads in ThreadPoolExecutor | 2.35 | + 1305% |
| `aiohttp` | 1 asynchronous thread | 0.18  | 0 % |

### Go
| Tool | Description | Benchmark values | Comparing, %|
|---|---|---|---|
| `some tool` | null | - | - |

### C++
| Tool | Description | Benchmark values | Comparing, %|
|---|---|---|---|
| `some tool` | null | - | - |

## DB adapters

### Python
| Tool | Description | Benchmark values, sec | Comparing, %|
|---|---|---|---|
| `psycopg` | 8 workers in ThreadPool | 2.25 | 0 |
| `asyncpg` | 1 asynchronous thread | 18.93 | + 841% |

### Golang
| Tool | Description | Benchmark values | Comparing, %|
|---|---|---|---|
| `some tool` | null | - | - |

### C++
| Tool | Description | Benchmark values | Comparing, %|
|---|---|---|---|
| `some tool` | null | - | - |
