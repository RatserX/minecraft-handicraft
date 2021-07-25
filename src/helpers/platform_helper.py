import sys

class PlatformHelper:
    def is_aix():
        return (sys.platform.startswith("aix"))
    
    def is_freebsd():
        return (sys.platform.startswith("freebsd"))
    
    def is_linux():
        return (sys.platform.startswith("linux"))
    
    def is_osx():
        return (sys.platform.startswith("darwin"))
    
    def is_windows():
        return (sys.platform.startswith("cygwin") or sys.platform.startswith("win32"))
