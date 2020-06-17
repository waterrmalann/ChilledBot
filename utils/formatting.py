def casify(text, case_type='normal'):
    if case_type == 'normal':
        if '-' in text or '_' in text:
            text = text.replace('-', ' ')
            text = text.replace('_', ' ')
        tokens = text.split(' ')
        return ' '.join(i.strip().capitalize() for i in tokens if i.strip())
    else:
        return text.title()

