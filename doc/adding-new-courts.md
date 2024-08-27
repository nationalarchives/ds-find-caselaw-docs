### Checklist for adding a new court

1. update [court_names.yaml](https://github.com/nationalarchives/ds-caselaw-utils/blob/main/src/ds_caselaw_utils/data/court_names.yaml) (utils)

2. update [neutral_citation_regex.yaml](https://github.com/nationalarchives/ds-caselaw-utils/blob/main/src/ds_caselaw_utils/data/neutral_citation_regex.yaml) (utils)

3. add a test to [test_neutral.py]'s `good_neutral_urls` (https://github.com/nationalarchives/ds-caselaw-utils/blob/main/src/ds_caselaw_utils/test_neutral.py) (utils), test with `poetry run pytest`

4. add the URL chunks (courts, subcourts) to the [editor ui judgments/converters.py](https://github.com/nationalarchives/ds-caselaw-editor-ui/blob/main/judgments/converters.py)

5. add the URL chunks (courts, subcourts) to the [public ui judgments/converters.py](https://github.com/nationalarchives/ds-caselaw-public-ui/blob/main/judgments/converters.py)

6. add the regex to the [Marklogic search helper](https://github.com/nationalarchives/ds-find-caselaw-docs/blob/main/doc/adding-new-courts.md)

7. deploy all the things (utils, marklogic, editor, public), not forgetting to bump
   the version of utils in the last two.

#### if you're adding a new name for an old court

1. ensure the new court has an `extra_params` with the URL of the old court

2. ensure the old court entry has both selectable and listable set to `false`.

3. set mappings in [search_parameters](https://github.com/nationalarchives/ds-caselaw-custom-api-client/blob/main/src/caselawclient/search_parameters.py) in the caselaw client to ensure searches for one URL term hit the other.
