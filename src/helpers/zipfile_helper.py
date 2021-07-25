import typing
import zipfile

class ZipfileHelper:
    def extract(file: str, path: str = None, member: str = None, pwd: bytes = None):
        with zipfile.ZipFile(file, "r") as zf:
            zf.extract(member, path, pwd)
            zf.close()
    
    def extractall(file: str, path: str = None, members: typing.Iterable[str] = None, pwd: bytes = None):
        with zipfile.ZipFile(file, "r") as zf:
            zf.extractall(path, members, pwd)
            zf.close()
