# Schema-v0.5 scenario freeze

- Generated task files: 84
- Directory: `data/scenarios_v05/`
- Aggregate manifest SHA-256:
  `c3571b13d50e5176f4c75723b593b1e005c873773607dd967058635be89f048e`
- Hash construction: sort task JSON files by name, compute each file's SHA-256,
  join `filename:lowercase_hash` records with LF, then SHA-256 the UTF-8 joined
  string.

The paid launcher independently recomputes and records this aggregate in every
`launch_manifest.json`. Any change to a task file therefore produces a visibly
different experiment manifest. A repository commit/tag should still be made
immediately before paid execution.
