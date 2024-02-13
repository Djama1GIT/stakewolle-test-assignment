# Stakewolle Test Assignment

## Technical Specification

A simple RESTful API service for a referral system needs to be developed.

### Functional requirements:
- User registration and authentication (JWT, OAuth 2.0) ✅
- Authenticated users should be able to create or delete their referral code. Only 1 code can be active at a time ✅
- When creating a code, its expiration date must be set ✅
- Ability to retrieve a referral code by the referrer's email address ✅
- Ability to register as a referral using a referral code ✅
- Retrieve information about referrals based on the referrer's ID ✅
- UI documentation (Swagger/ReDoc) ✅

### Optional tasks:
- <strike>Use clearbit.com/platform/enrichment to obtain additional user information during registration;</strike>❌
- Use emailhunter.co to verify the specified email address ⌛
- Cache referral codes using in-memory database ✅
- Readme.md file with project description and instructions for deployment and testing ⌛

### Stack:
- Use any modern web framework ✅
- Use a relational database and migrations (Sqlite, <u><b>PostgreSQL</b></u>, MySQL) ✅
- Host the project on GitHub ✅

### Project requirements:
- Code cleanliness and readability;
- All I/O bound operations should be asynchronous;
- The project should be well-structured;
- The project should be easy to deploy, handle non-standard situations, be resilient to incorrect user actions, etc.