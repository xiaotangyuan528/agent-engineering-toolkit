# End-to-end acceptance

Run in a fresh Codex profile and preserve the CLI events, app-server discovery result, output files and model identifier. Record PASS, FAIL, BLOCKED or NOT TESTED for each case.

1. Install from the candidate GitHub ref using the Marketplace command and install the plugin. Confirm the manifest version and all five enabled IDs via app-server `skills/list`.
2. Start a fresh session for each explicitly named skill. Require evidence that Codex read the installed skill. For architecture, module design and review, use the scenarios in examples/prompts.md and include an existing design for review.
3. In a fresh session ask “帮我设计一份技术文档。” with no skill name. Verify that it asks one question and does not draft. Answer with an object, then provide the type, audience and purpose as requested. Check the event trace for the Router and architecture skill reads.
4. In separate sessions, request the overall distributed KV architecture, RocksDB MemTable implementation and review of an existing design without naming skills. Verify the matching specialist is read and used. A suitable output without a recorded skill read proves only output quality.
5. For implementation, give a real checkout path and a fixed Commit while launching the agent from a different directory. Verify root, branch, SHA, dirty status and cited symbols against Git. Run a second case with a dirty file to confirm that it is not attributed to the fixed commit.
6. Save the output to Markdown. Convert using the installed skill's script. Reopen DOCX and validate text and styles. Where an Office renderer is available, export and inspect the pages.

Model-driven selection may vary. Never count pasted skill instructions or supplied source text as evidence of autonomous tool execution.
