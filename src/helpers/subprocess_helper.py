import string
import subprocess

class SubprocessHelper:
    def popen(*args: str, timeout: int = None) -> subprocess.Popen:
        def __args_transform(arg: str):
            template: string.Template = string.Template(arg)
            
            return template.substitute({
                #"PATH": path
            })
        
        #args_map = map(__args_transform, args)
        execution_args: list[str] = list(args)
        execution_subprocess: subprocess.Popen = subprocess.Popen(execution_args)
        
        if (timeout != None and timeout >= 0):
            execution_subprocess.wait(timeout)
        elif (timeout != None and timeout < 0):
            execution_subprocess.wait()
        else:
            return execution_subprocess
        
        return None
