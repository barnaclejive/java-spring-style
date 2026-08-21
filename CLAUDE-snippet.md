# CLAUDE.md snippet

Paste this into the `CLAUDE.md` of any project that follows these conventions.

Keep it short. `CLAUDE.md` is the only file loaded on every prompt, so it carries the
non-negotiables and the pointer. The detail lives in the skills and the rule files, which
load on demand.

```markdown
## Code Style Rules

This project follows the shared conventions in the **java-spring-style** plugin
(github.com/barnaclejive/java-spring-style). The skills are `naming-style`, `java-style`,
`thymeleaf-style`, and `testing-style`. Copies of the same rules live in `.claude/rules/`
and load when you edit a matching path. Run `/style-sync` to refresh those copies.

**Neither loading path is guaranteed to fire.** Before you finish any code change, load the
skill for the file type you touched, or read the matching file in `.claude/rules/`, and compare
your change against it. These rules carry the same weight as this file.

The non-negotiables, in short:

- Name every variable after its full class name. No abbreviations, no generic names.
- Java: never `var`, `final` everywhere, 140-character lines, `LoggerFactory.getLogger(getClass())`,
  never `log.warn`.
- Templates: no hardcoded user-facing strings and no fallback text. Every string comes from
  `messages.properties`.
- Never build a string with `+`. Use `#{key(args)}` for text, `@{...}` for URLs, `|...|` for
  identifiers.
- Never leave production code that only tests exercise. Delete the code and its tests together.
```

Add any project-local rules as separate files in `.claude/rules/` with their own `paths:`
frontmatter. `/style-sync` never touches them.
