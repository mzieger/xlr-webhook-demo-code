curl -v 'http://localhost:5516/webhooks/test_endpoint_get?token=wr0ng'
curl -v -X GET 'http://localhost:5516/webhooks/test_endpoint_get?wrong=tok3n'
curl -v -X GET 'http://localhost:5516/webhooks/test_endpoint_get?token=tok3n'


curl -v \
    -X POST \
    -H 'Content-type: application/json' \
    'http://localhost:5516/webhooks/test_endpoint_post?token=tok3n' \
    -d '{"user": "me", "topic": "commands", "message": "Hello\nWorld"}'
