import inspect


def template_func(fn):
    def decorator(*args, **kwargs):
        if _called_from_template(inspect.stack()):
            return fn
        return fn(*args, **kwargs)
    return decorator


def _called_from_template(stack):
    frame = stack[2]

    module_name = frame[0].f_globals.get('__name__')
    func_name = frame[3]

    return (module_name, func_name) == ('django.template.base', 'resolve')
