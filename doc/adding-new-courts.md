New courts should be added to ds-caselaw-utils' [court_names.yaml](https://github.com/nationalarchives/ds-caselaw-utils/blob/main/src/ds_caselaw_utils/data/court_names.yaml)

If you have an old court, ensure that the new court has an `extra_params` with the URL of the old court
and that there is an old court entry with both selectable and listable set to `false`.

You'll also need to set mappings in [search_parameters](https://github.com/nationalarchives/ds-caselaw-custom-api-client/blob/main/src/caselawclient/search_parameters.py) in the caselaw client to ensure searches for one URL term hit the other.

Currently you'll also need to modify the URLs in both the [editor](https://github.com/nationalarchives/ds-caselaw-editor-ui/blob/main/judgments/converters.py) and [public](https://github.com/nationalarchives/ds-caselaw-public-ui/blob/main/judgments/converters.py) `converters.py` to include
the court and subcourts too.

Remember to deploy everything.
