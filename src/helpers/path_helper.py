import glob
import os
import shutil
import typing

class PathHelper:
    def glob(*paths: str, recursive: bool = False, isdir: bool = True, isfile: bool = False, islink: bool = False, ismount: bool = False) -> list[str]:
        parsed_paths: list[str] = []
        pathname: str = os.path.join(*paths)
        glob_paths: list[str] = glob.glob(pathname, recursive = recursive)
        glob_paths_length: int = len(glob_paths)

        for i in range(glob_paths_length):
            glob_path: str = glob_paths[i]

            if (
                (isdir and os.path.isdir(glob_path)) or
                (isfile and os.path.isfile(glob_path)) or
                (islink and os.path.islink(glob_path)) or
                (ismount and os.path.ismount(glob_path))
            ):
                parsed_paths.append(glob_path)
        
        return parsed_paths
    
    def get_directory_glob(*paths: str, recursive: bool = False) -> str:
        parsed_paths: list[str] = PathHelper.glob(*paths, recursive = recursive)
        
        return parsed_paths[0] if (len(parsed_paths) > 0) else None
    
    def get_directory_path(p: str):
        path_split: typing.Tuple[str,str] = os.path.split(p)
        paths: list[str] = list(path_split)

        path_head: str = os.path.join(*paths[:-1])
        directory: str = os.path.normpath(path_head)

        return directory
    
    def get_file_extension(p: str):
        path_split: typing.Tuple[str,str] = os.path.split(p)
        paths: list[str] = list(path_split)

        path_tail: str = paths[-1]
        path_tail_split: list[str] = path_tail.split(".")
        path_tail_split_length: int = len(path_tail_split)

        if (path_tail_split_length > 1):
            extensions: list[str] = path_tail_split[1:]
            extension: str = ".".join(extensions)

            return extension
        else:
            return ""
    
    def get_file_glob(*paths: str, recursive: bool = False) -> str:
        parsed_paths: list[str] = PathHelper.glob(*paths, recursive = recursive, isdir = False, isfile = True)
        
        return parsed_paths[0] if (len(parsed_paths) > 0) else None
    
    def get_file_path(p: str, directory: bool = False, extension: bool = False):
        path_split: typing.Tuple[str,str] = os.path.split(p)
        paths: list[str] = list(path_split)
        
        path_tail: str = paths[1]
        file: str = path_tail
        
        if (not extension):
            file_split: list[str] = file.split(".")
            file = file_split[0]

        if (directory):
            path_head: str = paths[0]
            file = os.path.join(path_head, file)
        
        return file
    
    def get_link_path(paths: str, recursive: bool = False) -> str:
        parsed_paths: list[str] = PathHelper.glob(*paths, recursive = recursive, isdir = False, islink = True)
        
        return parsed_paths[0] if (len(parsed_paths) > 0) else None
    
    def get_mount_path(paths: str, recursive: bool = False) -> str:
        parsed_paths: list[str] = PathHelper.glob(*paths, recursive = recursive, isdir = False, ismount = True)
        
        return parsed_paths[0] if (len(parsed_paths) > 0) else None
    
    def clear(path: str, follow_symlinks = False) -> bool:
        try:
            for dir_entry in os.scandir(path):
                dir_entry_path: str = dir_entry.path

                if (dir_entry.is_dir(follow_symlinks = follow_symlinks)):
                    shutil.rmtree(dir_entry_path)
                else:
                    os.remove(dir_entry_path)
            
            return True
        except (OSError, TypeError):
            return False
    
    def copy(src: str, dst: str) -> str:
        if (os.path.isdir(src)):
            return shutil.copytree(src, dst)
        else:
            return shutil.copy2(src, dst)
    
    def exists(*paths: str) -> bool:
        path: str = os.path.join(*paths)

        return os.path.exists(path)
    
    def join(*paths: str, normalize: bool = False) -> str:
        path: str = os.path.join(*paths)
        
        if (normalize):
            return os.path.normpath(path)
        else:
            return path
    
    def remove(path: str = "", force: bool = False) -> bool:
        try:
            if (os.path.isdir(path)):
                shutil.rmtree(path) if (force) else os.rmdir(path)
            else:
                os.remove(path)
            
            return True
        except (OSError, TypeError):
            return False
    
    def rename(src: str, dst: str) -> bool:
        try:
            os.rename(src, dst)
            return True
        except FileNotFoundError:
            return False
