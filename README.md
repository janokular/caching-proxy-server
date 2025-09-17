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

1. Client requests item
2. Cache server checks if it’s stored in the cache
3. The item is not found
4. The cache server requests the item from the origin server
5. The origin server sends the item back
6. The cache server saves a copy of the item
7. The cache server sends the client the item
```

### Application details
```
# Starting the caching proxy server
caching_proxy.py --port <number> --origin <url>

# Clear the cache storage
caching_proxy.py --clear-cache
```

### Example
#### Starting the server
If the client makes the request to `http://localhost:3000/forms/post`\
The caching proxy server forwards the request to `https://httpbin.org/forms/post`\
It return the response along with headers and stores the response inside the cache storage
```
caching_proxy.py --port 3000 --origin https://httpbin.org
```

#### Response from the origin server
If the response is from the origin server `X-Cache: MISS`
```
curl -i http://localhost:3000/forms/post
```
```
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.11.2
Date: Wed, 20 Aug 2025 10:35:56 GMT
Date: Wed, 20 Aug 2025 10:35:56 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 1397
Connection: keep-alive
Server: gunicorn/19.9.0
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
X-Cache: MISS

<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
  <!-- Example form from HTML5 spec http://www.w3.org/TR/html5/forms.html#writing-a-form's-user-interface -->
  <form method="post" action="/post">
   <p><label>Customer name: <input name="custname"></label></p>
   <p><label>Telephone: <input type=tel name="custtel"></label></p>
   <p><label>E-mail address: <input type=email name="custemail"></label></p>
   <fieldset>
    <legend> Pizza Size </legend>
    <p><label> <input type=radio name=size value="small"> Small </label></p>
    <p><label> <input type=radio name=size value="medium"> Medium </label></p>
    <p><label> <input type=radio name=size value="large"> Large </label></p>
   </fieldset>
   <fieldset>
    <legend> Pizza Toppings </legend>
    <p><label> <input type=checkbox name="topping" value="bacon"> Bacon </label></p>
    <p><label> <input type=checkbox name="topping" value="cheese"> Extra Cheese </label></p>
    <p><label> <input type=checkbox name="topping" value="onion"> Onion </label></p>
    <p><label> <input type=checkbox name="topping" value="mushroom"> Mushroom </label></p>
   </fieldset>
   <p><label>Preferred delivery time: <input type=time min="11:00" max="21:00" step="900" name="delivery"></label></p>
   <p><label>Delivery instructions: <textarea name="comments"></textarea></label></p>
   <p><button>Submit order</button></p>
  </form>
  </body>
</html>
```

#### Response from the cache
If the response is from the cache `X-Cache: HIT`
```
curl -i http://localhost:3000/forms/post
```
```
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.11.2
Date: Wed, 20 Aug 2025 10:36:00 GMT
X-Cache: HIT

<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
  <!-- Example form from HTML5 spec http://www.w3.org/TR/html5/forms.html#writing-a-form's-user-interface -->
  <form method="post" action="/post">
   <p><label>Customer name: <input name="custname"></label></p>
   <p><label>Telephone: <input type=tel name="custtel"></label></p>
   <p><label>E-mail address: <input type=email name="custemail"></label></p>
   <fieldset>
    <legend> Pizza Size </legend>
    <p><label> <input type=radio name=size value="small"> Small </label></p>
    <p><label> <input type=radio name=size value="medium"> Medium </label></p>
    <p><label> <input type=radio name=size value="large"> Large </label></p>
   </fieldset>
   <fieldset>
    <legend> Pizza Toppings </legend>
    <p><label> <input type=checkbox name="topping" value="bacon"> Bacon </label></p>
    <p><label> <input type=checkbox name="topping" value="cheese"> Extra Cheese </label></p>
    <p><label> <input type=checkbox name="topping" value="onion"> Onion </label></p>
    <p><label> <input type=checkbox name="topping" value="mushroom"> Mushroom </label></p>
   </fieldset>
   <p><label>Preferred delivery time: <input type=time min="11:00" max="21:00" step="900" name="delivery"></label></p>
   <p><label>Delivery instructions: <textarea name="comments"></textarea></label></p>
   <p><button>Submit order</button></p>
  </form>
  </body>
</html>
```
