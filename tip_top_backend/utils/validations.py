"""
Validate function: this function verity that exist only a object with is_last equal true
"""


def validate_is_last(obj, context):
    """Check is_last."""
    if obj:
        if context['request'].method != 'PUT':
            return False
        elif context['request'].data['id'] != obj.id and context['request'].data['is_last']:
            return False
    return True
