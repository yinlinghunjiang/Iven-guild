import asyncio
import functools


def to_async(func):
    """
    This is a decorator that can be used to convert a function to an async function.

    Warnings:
        When using this decorator, the type hint of the function will be lost.

    Args:
        func: The function to convert.

    Returns: The converted function.

    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.get_running_loop().run_in_executor(
            None, functools.partial(func, *args, **kwargs)
        )

    return wrapper
