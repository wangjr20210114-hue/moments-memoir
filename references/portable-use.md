# Portable use

This package keeps its core instructions in plain Markdown and its deterministic helpers in standard-library Python so it can be adapted beyond Codex.

## Agent Skills compatible products

Import the entire `moments-memoir` folder. Keep the relative paths between `SKILL.md`, `references/`, `scripts/` and `assets/`. The product may ignore `agents/openai.yaml`; that file is only interface metadata.

## Products with custom agents but no folder import

Use `SKILL.md` as the main instruction, attach the reference Markdown files as knowledge, and expose the Python scripts as local tools when supported. Preserve the authentication boundary and progress contract exactly.

## Products without local code execution

Run the one-click exporter directly on the user's computer. Then give the agent the completed export directory or a privacy-reviewed subset. Such a product can perform editorial and design work, but it cannot safely claim to have run local WeChat extraction itself.

Do not assume a platform can access local WeChat files, open a visible terminal, publish privately or generate images. Detect the available capabilities and degrade to a local export plus uploaded archive instead of weakening the user's privacy.
