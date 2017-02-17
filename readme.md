# Mongstore

HTTP wrapper for mongodb. Extends regular http API with per-objects/per-collection permissions and JSON schemas.

Features list:

1. REST API for collections
   - list of objs with pagination
   - POST, PUT, GET objs
   - /resource/_id
   - /resource/_schema
   - /resource
2. JSON schema driven validation
3. Per-obj permissions, Per-collection permissions, Default User schema, Groups
4. Code style == PEP-8
5. Full test coverage
