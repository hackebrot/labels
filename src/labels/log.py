import logging

import click


class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        ctx = click.get_current_context()
        setattr(record, "cmd", ctx.command.name)
        return True


def create_logger() -> logging.Logger:
    logger = logging.getLogger("labels")
    logger.setLevel(logging.NOTSET)
    logger.propagate = False
    logger.addFilter(ContextFilter())

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s %(name)s %(cmd)s: %(message)s")
    handler.setFormatter(formatter)

    del logger.handlers[:]
    logger.addHandler(handler)
    return logger
