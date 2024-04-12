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

## Documentation on use in practice

(12 April 2024)

### Availability

We use [Django Waffle](https://waffle.readthedocs.io/en/stable/) for feature flags. They’re available in the Public and Editor UIs.

### Creating and modifying flags

Log into the admin interface – /django for the PUI, or /admin for the EUI. In the admin interface you’ll see a subsection named ‘django-waffle’. Pick ‘flags’ to edit an existing flag, or the + icon next to ‘flags’ to make a new one.

Pick a name – the convention is to use ‘snake_case’. Ensure “testing” is on. You can set “Everyone” if you want to ensure no-one/everyone sees the flag. Hit ‘save’.

The options are generally well explained in the interface.

### Activating a testing flag

Visit any URL with a parameter of `?dwft_history_timeline=1` to turn testing on for that user; `=0` to turn it off.

### Using flags in HTML templates

[Documentation](https://waffle.readthedocs.io/en/stable/usage/templates.html)

This is the only way we’ve used flags so far.

```
{% load waffle_tags %}
{% flag "flag_name" %}
    flag_name is active!
{% else %}
    flag_name is inactive
{% endflag %}
```

### Using flags in Python views:

[Documentation](https://waffle.readthedocs.io/en/stable/usage/views.html)

Inside a view, you can access the flag status via `waffle.flag_is_active(request, 'flag_name')`

### Labs

The Editor interface has a way to turn on features for yourself at [/labs](https://editor.staging.caselaw.nationalarchives.gov.uk/labs).

(judgments/views/labs.py)[https://github.com/nationalarchives/ds-caselaw-editor-ui/blob/main/judgments/views/labs.py] has a list of the current experiments.
