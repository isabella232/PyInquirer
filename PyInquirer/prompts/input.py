# -*- coding: utf-8 -*-
"""
`input` type question
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import inspect
from prompt_toolkit.styles import merge_styles
from prompt_toolkit import PromptSession

from prompt_toolkit.validation import Validator, ValidationError
from PyInquirer.constants import DEFAULT_STYLE

# use std prompt-toolkit control


def question(message,
             qmark="?",
             default='',
             style=None,
             validate=None,
             **kwargs):

    # TODO style defaults on detail level
    kwargs['style'] = merge_styles([DEFAULT_STYLE, style])

    if validate:
        if inspect.isclass(validate) and issubclass(validate, Validator):
            kwargs['validator'] = validate()
        elif callable(validate):
            class _InputValidator(Validator):
                def validate(self, document):
                    verdict = validate(document.text)
                    if verdict is not True:
                        if verdict is False:
                            verdict = 'invalid input'
                        raise ValidationError(
                            message=verdict,
                            cursor_position=len(document.text))
            kwargs['validator'] = _InputValidator()

    def get_prompt_tokens():
        return [
            ("class:qmark", qmark),
            ("class:question", ' {} '.format(message)),
            ("class:answer", default),
        ]

    return PromptSession(get_prompt_tokens, **kwargs).app
