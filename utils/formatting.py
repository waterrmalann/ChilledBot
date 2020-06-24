def casify(text, case_type='normal'):
    if case_type == 'normal':
        if '-' in text: text = text.replace('-', ' ')
        if '_' in text: text = text.replace('_', ' ')
        tokens = text.split(' ')
        return ' '.join(i.strip().capitalize() for i in tokens if i.strip())
    else:
        return text.title()

