# required to decrypt password properties. Can only be used by packaged scripts.
from com.xebialabs.deployit.util import PasswordEncrypter

# the 'events.WebhookEndpoint' instance.
global endpoint
# the `mywebhooks.UrlParameterTokenAuthentication` instance. Holds the `parameter` and `token` properties
global config
# the HTTP headers. Python dictionary
global headers
# the URL parameters. Python dictionary. Each value is an array of strings.
global params
# the HTTP request body. Only available when endpoint.method == "POST"
global payload

# let's get the PasswordEncrypter instance
pe = PasswordEncrypter.getInstance()


# find the URL parameter named `config.parameter` and return its values, or an empty array if not found
def getTokens():
    return params[config.parameter] if config.parameter in params else []

# True if one of the values of the `config.parameter` URL parameter is the decrypted `config.token`.
authenticated = pe.ensureDecrypted(config.token) in getTokens()