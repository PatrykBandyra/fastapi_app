import functools


def greetings(func=None, *, arg=None):
    # 1. Decorator arguments are applied to itself as partial arguments
    if func is None:
        return functools.partial(greetings, arg=arg)
    # 2. logic with the arguments

    # 3. Handles the actual decorating
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result_string = func(*args, **kwargs)
        result_string = result_string.lower()
        result_string = result_string.title()
        result_string = 'Hello ' + result_string
        return result_string
    return wrapper


def is_palindrome(func=None, *, arg=None):
    if func is None:
        return functools.partial(greetings, arg=arg)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        def _is_palindrome(s):
            return s == s[::-1]

        result_string = func(*args, **kwargs)
        check_str = result_string.lower()
        alphanumeric_filter = filter(str.isalnum, check_str)
        alphanumeric_string = ''.join(alphanumeric_filter)
        print(alphanumeric_string)
        if _is_palindrome(alphanumeric_string):
            return result_string + ' - is palindrome'
        else:
            return result_string + ' - is not palindrome'
    return wrapper


def format_output(*dec_args):
    def decorator(func):
        def wrapper(*args, **kwargs):
            formatted_dict = dict()
            result_dict = func(*args, **kwargs)
            for i in range(len(dec_args)):
                temp_keys = dec_args[i].split('__')
                target_value = ''
                for key in temp_keys:
                    try:
                        target_value += f' {result_dict[key]}'
                    except KeyError:
                        raise ValueError
                target_value = target_value.strip()
                formatted_dict[dec_args[i]] = target_value
            return formatted_dict
        return wrapper
    return decorator


def add_instance_method(cls):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)

        setattr(cls, func.__name__, wrapper)
        return func
    return decorator


def add_class_method(cls):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        return func
    return decorator


class A:
    pass


@add_instance_method(A)
def hello(name):
    print(f'Hello, {name}')


@add_class_method(A)
def bye(name):
    print(f'Bye, {name}')


if __name__ == '__main__':
    a = A()
    a.hello('Patryk')
    A.bye('Patryk')
