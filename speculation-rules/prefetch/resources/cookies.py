
def main(request, response):
  def getCookie(key):
    key = key.encode("utf-8")
    if key in request.cookies:
      return f'"{request.cookies[key].value.decode("utf-8")}"'
    else:
      return "undefined"

  Purpose = request.headers.get("Purpose", b"").decode("utf-8")
  SecPurpose = request.headers.get("Sec-Purpose", b"").decode("utf-8")

  cookie_count = int(
      request.cookies[b"count"].value) if b"count" in request.cookies else 0
  response.set_cookie("count", f"{cookie_count+1}",
                      secure=True, samesite="None")
  response.set_cookie(
      "type", "prefetch" if SecPurpose.startswith("prefetch") else "navigate")

  headers = [(b"Content-Type", b"text/html")]

  content = f'''
  <!DOCTYPE html>
  <meta name="timeout" content="long">
  <script src="/common/dispatcher/dispatcher.js"></script>
  <script src="utils.sub.js"></script>
  <script>
  window.requestHeaders = {{
    purpose: "{Purpose}",
    sec_purpose: "{SecPurpose}"
  }};

  window.requestCookies = {{
    count: {getCookie("count")},
    type:  {getCookie("type")}
  }};

  const uuid = new URLSearchParams(location.search).get('uuid');
  window.executor = new Executor(uuid);
  </script>
  '''
  return headers, content
