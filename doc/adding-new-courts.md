### Checklist for adding a new court

1. update [court_names.yaml](https://github.com/nationalarchives/ds-caselaw-utils/blob/main/src/ds_caselaw_utils/data/court_names.yaml) (utils)

2. In the PUI create a jinja template in the [templates/content/courts](https://github.com/nationalarchives/ds-caselaw-public-ui/tree/main/ds_judgements_public_ui/templates/content/courts) folder with the name of the `param` of the new court.

#### If there are new neutral citations:

3. update [neutral_citation_regex.yaml](https://github.com/nationalarchives/ds-caselaw-utils/blob/main/src/ds_caselaw_utils/data/neutral_citation_regex.yaml) (utils)

4. add a test to [test_neutral.py](https://github.com/nationalarchives/ds-caselaw-utils/blob/main/src/ds_caselaw_utils/tests/test_neutral.py)'s `good_neutral_urls` (utils), test with `poetry run pytest`

5. add the regex to the [Marklogic search helper](https://github.com/nationalarchives/ds-caselaw-marklogic/blob/main/src/main/ml-modules/root/judgments/search/helper.xqy)

6. deploy all the things (utils, marklogic, ingester, editor, public), not forgetting to bump the version of utils in the last three.

#### if you're adding a new name for an old court

1. ensure the new court has an `extra_params` with the URL of the old court

2. ensure the old court entry has both selectable and listable set to `false`.

3. set mappings in [search_parameters](https://github.com/nationalarchives/ds-caselaw-custom-api-client/blob/main/src/caselawclient/search_parameters.py) in the caselaw client to ensure searches for one URL term hit the other.
