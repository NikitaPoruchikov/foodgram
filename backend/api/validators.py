from rest_framework.exceptions import ValidationError

from .validation_messages import ERROR_MESSAGES


def validate_cooking_time(value):
    if value < 1:
        raise ValidationError(ERROR_MESSAGES['invalid_cooking_time'])
    return value


def validate_image(value):
    if not value:
        raise ValidationError(ERROR_MESSAGES['empty_image'])
    return value


def validate_tags(value):
    if not value:
        raise ValidationError(ERROR_MESSAGES['no_tags'])
    if len(set(value)) != len(value):
        raise ValidationError(ERROR_MESSAGES['duplicate_tags'])
    return value


def validate_ingredients(value):
    if not value:
        raise ValidationError(ERROR_MESSAGES['empty_ingredients'])
    ingredient_ids = [item['ingredient'].id for item in value]
    if len(ingredient_ids) != len(set(ingredient_ids)):
        raise ValidationError(ERROR_MESSAGES['duplicate_ingredients'])
    return value
