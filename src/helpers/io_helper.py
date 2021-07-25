import contextlib
import io
import json
import typing

class IoHelper:
    @contextlib.contextmanager
    def open(file: str, mode: typing.Any, buffering: int = -1, encoding: typing.Optional[str] = None, errors: typing.Optional[str] = None, newline: typing.Optional[str] = None, closefd: bool = True, opener: typing.Optional[typing.Any] = None, error: bool = True) -> typing.Generator[io.TextIOWrapper, None, None]:
        try:
            with (open(file, mode, buffering, encoding, errors, newline, closefd, opener)) as fp:
                yield fp
        except Exception as e:
            if (error):
                raise e
            else:
                yield None
    
    def get_json(file: str, error: bool = True, **kw) -> typing.Any:
        try:
            with (IoHelper.open(file, "r", error = error)) as fp:
                object: typing.Any = json.load(fp, **kw)

                fp.close()
                return object
        except Exception as e:
            if (error):
                raise e
            else:
                return None
