### Checklist for adding a new court

1. update [court_names.yaml](https://github.com/nationalarchives/ds-caselaw-utils/blob/main/src/ds_caselaw_utils/data/court_names.yaml) (utils)

2. update [neutral_citation_regex.yaml](https://github.com/nationalarchives/ds-caselaw-utils/blob/main/src/ds_caselaw_utils/data/neutral_citation_regex.yaml) (utils)

3. add the URL chunks (courts, subcourts) to the [editor ui converters](https://github.com/nationalarchives/ds-caselaw-editor-ui/blob/main/judgments/converters.py)

4. add the URL chunks (courts, subcourts) to the [public ui converters](https://github.com/nationalarchives/ds-caselaw-public-ui/blob/main/judgments/converters.py)

5. deploy all the things (utils, editor, public), not forgetting to bump
   the version of utils in all those things.

#### if you're adding a new name for an old court

1. ensure the new court has an `extra_params` with the URL of the old court

2. ensure the old court entry has both selectable and listable set to `false`.

3. set mappings in [search_parameters](https://github.com/nationalarchives/ds-caselaw-custom-api-client/blob/main/src/caselawclient/search_parameters.py) in the caselaw client to ensure searches for one URL term hit the other.
