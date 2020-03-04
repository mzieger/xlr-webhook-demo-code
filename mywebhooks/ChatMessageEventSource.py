import json

global input
global config
global CI

# create the output event, given some data
def chat_message_event(data):
    return CI("mywebhooks.ChatMessageEvent", {
        'user': data['user'] if 'user' in data else None,
        'topic': data['topic'] if 'topic' in data else None,
        'message': data['message'] if 'message' in data else None
    })

# make sure all the properties of the chat message are present
def checkMessage(msg):
    return msg.user is not None and \
        msg.topic is not None and \
        msg.message is not None

# format message for logging
def formatMessage(msg):
    return '[#' + str(msg.topic) + '] ' + str(msg.user) + ': ' + str(msg.message)

# True iff 'topics' is not configured, empty, or if the topic's message is one of the 'topics'.
def topicFilter(msg):
    return config.topics is None or \
        len(config.topics) == 0 or \
        msg.topic in config.topics

# True iff 'ignoredUsers' is not configured, eepty, or if the user is NOT one of the 'ignoredUsers'.
def userFilter(msg):
    return config.ignoredUsers is None or \
        len(config.ignoredUsers) == 0 or \
        not (msg.user in config.ignoredUsers)

# True iff 'badWords' is not configured, empty, or if the message does not contain any of the 'badWords'.    
def badWordFilter(msg):
    if config.badWords is None or len(config.badWords) == 0:
        return True
    else:
        ok = True
        for bad in config.badWords:
            if bad in msg.message:
                ok = False
                break
        return ok

# supports both GET and POST HTTP endpoint for Webhooks event sources:
message_data = json.loads(input.content) if str(config.eventSource.method) == "POST" else input.parameters

# create the ChatMessageEvent
output = chat_message_event(message_data)

# check all properties of the message
if not checkMessage(output):
    print('Malformed chat message: ' + str(message_data))
    output = None
else:
    # apply the filters. if any of them fails, do not publish any event:
    if not topicFilter(output) or not userFilter(output) or not badWordFilter(output):
        print('Ignored! ' + formatMessage(output))
        output = None
    else:
        print(formatMessage(output))