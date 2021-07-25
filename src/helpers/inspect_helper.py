import inspect

class InspectHelper:
    def get_function_name(context = 1) -> None:
        stack: list[inspect.FrameInfo] = inspect.stack(context)
        caller: inspect.FrameInfo = stack[1]

        return caller.function
