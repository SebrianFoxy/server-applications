import logging

# Определяем числовое значение для уровня TRACE
TRACE_LEVEL = 5
logging.addLevelName(TRACE_LEVEL, "TRACE")

# Создаем метод trace для логирования сообщений на уровне TRACE


def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACE_LEVEL):
        self._log(TRACE_LEVEL, message, args, **kwargs)


# Добавляем метод trace к объекту Logger
logging.Logger.trace = trace
