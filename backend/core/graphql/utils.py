from graphene.utils.str_converters import to_snake_case


def localized_field_resolver(obj, info, **kwargs):
    """
    Custom resolver to return the user language value from localized fields
    """
    attr = getattr(obj, to_snake_case(info.field_name))

    if attr is None:
        return None

    if info.context.user.is_authenticated:
        return attr.get(info.context.user.language)
    else:
        return attr.get()
