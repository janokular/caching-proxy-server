## Caching proxy server
### How the caching proxy server works?
```
+-----------------+                 +-----------------+                 +-----------------+
|                 |--------1------->|                 |--------4------->|                 |
|     client      |                 |  cache server   |                 |  origin server  |
|                 |<-------7--------|                 |<-------5--------|                 |
+-----------------+                 +-----------------+                 +-----------------+
                                        |    ʌ    |
                                        2    |    6
                                        |    3    |
                                        v    |    v
                                    +-----------------+
                                    |                 |
                                    |  cache storage  |
                                    |                 |
                                    +-----------------+

# 1 Client requests item
# 2 Cache server checks if it’s stored in the cache
# 3 The item is not found
# 4 The cache server requests the item from the origin server
# 5 The origin server sends the item back
# 6 The cache server saves a copy of the item
# 7 The cache server sends the client the item
```

### Application details
```
# Starting the caching proxy server
caching_proxy.py --port <number> --origin <url>


# Example
caching_proxy.py --port 3000 --origin http://dummyjson.com

# If the client makes the request to `http://localhost:3000/products`
curl http://localhost:3000/products

# The caching proxy server forwards the request to `http://dummyjson.com/products`
# It return the response along with headers and caches the response inside the cache storage
...

# If the response is from the cache
X-Cache: HIT

# If the response is from the origin server
X-Cache: MISS


# Clear the cache storage
caching_proxy.py --clear-cache
```
