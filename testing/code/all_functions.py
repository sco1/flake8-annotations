"""Check for correct parsing of function types & decorators."""


def public_fun():
    pass


def public_fun_return_annotated() -> None:
    pass


def _protected_fun():
    pass


def __private_fun():
    pass


def __special_fun__():
    pass


async def async_public_fun():
    pass


async def async_public_fun_return_annotated() -> None:
    pass


async def _async_protected_fun():
    pass


async def __async_private_fun():
    pass


async def __async_special_fun__():
    pass


class Foo:
    @some_decorator
    def decorated_noncallable_method(self):
        pass

    @some_decorator()
    def decorated_callable_method(self):
        pass

    @some_decorator
    async def decorated_noncallable_async_method(self):
        pass

    @some_decorator()
    async def decorated_callable_async_method(self):
        pass

    @classmethod
    def decorated_classmethod(cls):
        pass

    @staticmethod
    def decorated_staticmethod():
        pass

    @classmethod
    async def decorated_async_classmethod(cls):
        pass

    @staticmethod
    async def decorated_async_staticmethod():
        pass

    @some_decorator
    @classmethod
    def decorated_noncallable_classmethod(cls):
        pass

    @some_decorator()
    @classmethod
    def decorated_callable_classmethod(cls):
        pass

    @some_decorator
    @staticmethod
    def decorated_noncallable_staticmethod():
        pass

    @some_decorator()
    @staticmethod
    def decorated_callable_staticmethod():
        pass

    @some_decorator
    @classmethod
    async def decorated_noncallable_async_classmethod(cls):
        pass

    @some_decorator()
    @classmethod
    async def decorated_callable_async_classmethod(cls):
        pass

    @some_decorator
    @staticmethod
    async def decorated_noncallable_async_staticmethod():
        pass

    @some_decorator()
    @staticmethod
    async def decorated_callable_async_staticmethod():
        pass
