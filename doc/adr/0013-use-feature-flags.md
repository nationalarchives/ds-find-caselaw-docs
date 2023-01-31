# 13. Use feature flags

Date: 2023-01-31

## Status

Accepted

## Context

We have a need to test new features with editors, for user research, feedback and building confidence in our decisions.
At the moment we can only do this by making sure that `main` is in the state we wish to test, and deploying the branch
to staging.

This means that it is occasionally necessary to freeze staging in order to run tests, and that in turn means that other
development work or urgent fixes becomes stalled. It is also impossible to test multiple new features in various
combinations at the same time.

Potential workarounds which have been discussed include an entire separate test environment, but this still suffers the
same problem of only being able to test a single state, and requiring additional workload to keep any test branch up to
date with urgent fixes. Another alternative is the dynamic provisioning of a new test environment for each feature
branch, but this will likely involve significant overhead. The third discussed option, making use of feature flags to
selectively enable functionality as needed based on various criteria, offers an elegant solution.

## Decision

We will implement feature flagging in Public UI and Editor UI, which will allow us to selectively enable or disable functionality as needed. This may include dynamically via URL parameters, on a user-by-user basis, by user groups, or as a percentage of users.

## Consequences

- We will be able to test combinations of features as needed
- There is no need for an additional testing environment
- Features can be deployed to production and tested against real data and in a real workflow
- Additional work will be needed to implement feature flipping logic
- Additional work may be needed to support both old and new behaviours concurrently
- It will be necessary to remove old feature flags once features have reached full adoption
- Team members running testing will need training on how to opt users into features
