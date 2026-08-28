# Schema-v0.5 scenario freeze

- Generated task files: 84
- Directory: `data/scenarios_v05/`
- Aggregate manifest SHA-256:
  `e16319a791ab4600f88a33f7957e66eec18be262649caac03845c161119044b9`
- Hash construction: sort task JSON files by name, compute each file's SHA-256,
  join `filename:lowercase_hash` records with LF, then SHA-256 the UTF-8 joined
  string.

The paid launcher independently recomputes and records this aggregate in every
`launch_manifest.json`. Any change to a task file therefore produces a visibly
different experiment manifest. A repository commit/tag should still be made
immediately before paid execution.

This freeze includes the pre-gap flight-belief repair, semantically valid
aligned-branch close options, and scored hidden-user interventions. The blinded
independent-audit packets were regenerated from this exact scenario set; response
sheets were reset to blank because no earlier audit answers may be carried
across a scenario revision.
