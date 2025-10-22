from .core import init, run, shutdown, ApplicationCreateInfo

def main(create_info: ApplicationCreateInfo) -> None:
    init(create_info)
    run()
    shutdown()

__all__ = [
    "main",
    "ApplicationCreateInfo"
]