def casify(text: str, case_type: str = 'title') -> str:
    """Format text to specific case types. Accepts regular cased strings, snake case, and kebab case"""

    if case_type == 'title':  # This Is An Example
        return text.title().replace('_', ' ').replace('-', ' ')
    elif case_type == 'pascal':  # ThisIsAnExample
        return text.title().replace('_', '').replace('-', '').replace(' ', '')
    elif case_type == 'camel':  # thisIsAnExample
        return text[0].lower() + text.title().replace('_', '').replace('-', '').replace(' ', '')[1:]
    elif case_type == 'skewer' or case_type == 'kebab':  # this-is-an-example
        return text.lower().replace('_', '-').replace(' ', '-')
    elif case_type == 'skewer_upper' or case_type == 'kebab_upper':  # THIS-IS-AN-EXAMPLE
        return text.upper().replace('_', '-').replace(' ', '-')
    elif case_type == 'snake':  # this_is_an_example
        return text.lower().replace(' ', '_').replace('-', '_')
    elif case_type == 'snake_upper':  # THIS_IS_AN_EXAMPLE
        return text.upper().replace(' ', '_').replace('-', '_')
    else:
        raise ValueError('invalid case type')

def join_words(li: list, oxford_comma: bool = True) -> str:
	"""Join a list of words by comma with an 'and' for the last item."""
	
	if not li:  # Empty list
		return ''
	elif len(li) == 1:  # Single item in list
		return li[0]
	else:  
		return f"{', '.join(li[:-1])}{', and' if oxford_comma else ' and'} {li[-1]}"
    
def codeblock(text: str, large: bool = True) -> str:
    """Wraps text in a discord codeblock (ie: ```x``` and `x`)"""

    return f"```{text}```" if large else f"`{text}`"