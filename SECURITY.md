# Security

This project is a reference implementation.

Before production use:

- authenticate and authorize asset operations
- validate file size and media types
- scan uploaded content
- isolate untrusted asset parsers
- encrypt data in transit and at rest
- store secrets in a secret manager
- apply rate limits
- add dependency and container scanning
- avoid exposing internal error details
