from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    """
    Here we will generate a unique token to be sent as part of URL.
    """

    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(user.email) + str(timestamp) + str(user.is_active)
        )


account_activation_token = TokenGenerator()
