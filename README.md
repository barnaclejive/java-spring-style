# java-spring-style

Portable code style rules for Java + Spring Boot + Thymeleaf projects, packaged as a
Claude Code plugin.

## Install

```bash
# in Claude Code
/plugin marketplace add barnaclejive/java-spring-style
/plugin install java-spring-style@java-spring-style
```

Then, in each project that follows these conventions:

```bash
/style-sync          # copies rules/ into the project's .claude/rules/
```

and paste the block from [CLAUDE-snippet.md](CLAUDE-snippet.md) into the project `CLAUDE.md`.

## What is in it

| Skill | Rule file | Covers |
|---|---|---|
| `naming-style` | `rules/naming.md` | Variable names match the class name, no abbreviations, `{Source}To{Target}` converter methods |
| `java-style` | `rules/java-style.md` | No `var`, `final` everywhere, 140-character lines, record and accessor formatting, logger declaration, log-level discipline, magic strings, member ordering |
| `thymeleaf-style` | `rules/frontend-style.md` | No hardcoded user-facing strings, parameterized i18n messages, the never-concatenate ladder, Bootstrap-first styling, semantic headings |
| `testing-style` | `rules/testing.md` | JUnit 5 + Mockito scaffolding, AssertJ, test naming, fixtures |

## Why both skills and rule files

Claude Code has two ways to load this content, and neither one is guaranteed to fire:

- **Skills** load when the task matches the skill `description`, or on an explicit `/skill-name`.
- **`.claude/rules/*.md`** load when an edited file matches the `paths:` frontmatter.

The two cover different moments, so the plugin ships both. The `CLAUDE.md` snippet is the
backstop: it is the only content loaded on every prompt, so it names the non-negotiables and
tells Claude to load the detail before finishing a change.

## About the examples

The rules use concrete class names from an illustrative subscription-billing domain
(`SubscriptionDetailDto`, `BillingPeriod`, `ServiceRegionService`, `CatalogItemStatus`, and
similar). No such project exists. The names are deliberately long and unabbreviated, because a
rule about long, unabbreviated names cannot be demonstrated with `FooDto`. Read them as
illustrations of the shape, not as references to real code.

## Editing the rules

`rules/` is the single source of truth. `skills/` is generated from it.

```bash
# edit rules/java-style.md, then
python3 build.py
git add rules skills && git commit
```

`build.py` swaps the `paths:` frontmatter of a rule file for the `name:` / `description:`
frontmatter a skill needs. The body is copied verbatim, so the two cannot drift.
Skill descriptions live in the `SKILLS` map at the top of `build.py`.

## Project-local rules

Anything specific to one codebase — a house UI style guide, domain conventions, shared
utilities — belongs in that project's own `.claude/rules/` file with its own `paths:`
frontmatter. `/style-sync` only writes the four files above and leaves everything else alone.

## License

MIT
