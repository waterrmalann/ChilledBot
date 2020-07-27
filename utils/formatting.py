def casify(text, case_type='pascal'):
    if case_type == 'pascal':
        return text.title().replace('_', ' ').replace('-', ' ')
    elif case_type == 'camel':
        tex = casify(text, case_type = 'pascal')
        if len(text.split(' ')) > 1: return text[0].lower() + tex[1:]
        else: return tex
    else:
        raise ValueError('Inappropriate argument value. Use a proper case type.')

