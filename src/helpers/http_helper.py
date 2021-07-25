import contextlib
import requests
import tqdm
import typing
import urllib.parse

class HttpHelper:
    @contextlib.contextmanager
    def request(url: str, params: typing.Any = None, method: str = "GET", **kwargs) -> typing.Generator[requests.models.Response, None, None]:
        method_upper: str = method.upper()

        if (not "headers" in kwargs):
            kwargs["headers"] = {
                "Accept-Language": "en-US;en,q=0.5",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
            }
        
        if (method_upper == "GET"):
            with requests.get(url, params = params, **kwargs) as response:
                yield response
        elif (method_upper == "POST"):
            with requests.post(url, params = params, **kwargs) as response:
                yield response
        elif (method_upper == "PUT"):
            with requests.put(url, params = params, **kwargs) as response:
                yield response
        else:
            yield None
    
    def get_json(url: str, **kw):
        with HttpHelper.request(url) as response:
            object: typing.Any = response.json(**kw)

            response.close()
            return object
    
    def stream_download(url: str, file: str, **kwargs) -> None:
        with open(file, "wb") as stream:
            with HttpHelper.request(url, stream = True, **kwargs) as response:
                content_length: str = response.headers.get("Content-Length", 0)
                unquote_url: str = urllib.parse.unquote(response.url)
                unquote_url_split: list[str] = unquote_url.split("/")

                total: int = int(content_length)
                desc: str = unquote_url_split[-1]

                with tqdm.tqdm.wrapattr(stream, "write", desc = desc, miniters = 1, total = total) as fout:
                    for buffer in response.iter_content(4096):
                        fout.write(buffer)
                
                response.close()
            
            stream.close()
