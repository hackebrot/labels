import logging

import click


class ContextFilter(logging.Filter):
    """Logging filter to add the click command to the record."""

    def filter(self, record: logging.LogRecord) -> bool:
        ctx = click.get_current_context(silent=True)
        if not ctx:
            return False

        setattr(record, "cmd", ctx.command.name)
        return True


def create_logger() -> logging.Logger:
    """Create a Logger with a formatter for the click command."""

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
