---
description: Copy the shared java-spring-style rule files into this project's .claude/rules/
---

Copy the shared rule files from this plugin into the current project, so they also load
through the path-triggered `.claude/rules/` mechanism.

Do these steps:

1. Find the plugin root. It is the directory that holds `rules/naming.md`, `rules/java-style.md`,
   `rules/frontend-style.md`, and `rules/testing.md`. Look in `${CLAUDE_PLUGIN_ROOT}` first. If that
   variable is not set, search under `~/.claude/plugins/` for a `java-spring-style` directory that
   contains a `rules/` folder.
2. Create `.claude/rules/` in the current project if it does not exist.
3. Copy each file from the plugin `rules/` directory into `.claude/rules/`, keeping the same name.
4. After each copy, insert this line directly below the closing `---` of the frontmatter, if it is
   not already present:

   `<!-- Managed by java-spring-style. Do not edit here. Edit the source repo, then re-run /style-sync. -->`

5. Do NOT touch any other file in `.claude/rules/`. Project-local rule files live beside the
   synced ones and are not managed by this command.
6. Report which files you copied, which you overwrote, and which project-local files you left alone.

Warn the user if a synced file has local edits that this command will overwrite. Show the diff and
ask before you overwrite it. A local edit means the shared rule needs a change in the source repo,
not a change here.
