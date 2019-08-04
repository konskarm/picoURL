from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models


class URLMapping(models.Model):
    """The URL Mapping model.
    The min length validator can be removed, if we consider that in the future we may need
    to have a dynamic size for the short_codes.
    """
    short_code = models.CharField(
        max_length=12,
        primary_key=True,
        validators=[
            RegexValidator(
                regex="[a-zA-Z0-9_-]*",
                message="Short code must contain only alphanumeric or _,- characters. ",
                code="invalid_short_code"
            ),
            MinLengthValidator(
                limit_value=10,
                message="Short code must contain at least 10 characters."
            )
        ])
    original_url = models.URLField(max_length=2000, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    times_used = models.BigIntegerField(default=0)
