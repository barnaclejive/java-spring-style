# java-spring-style

Portable code style rules for Java + Spring Boot + Thymeleaf projects. The rules are plain
markdown files. Any coding agent that can read a URL or clone a repository can use them. The
repository is also packaged as a Claude Code plugin.

Repository: https://github.com/barnaclejive/java-spring-style

**Coding agents: start at [Instructions for coding agents](#instructions-for-coding-agents).**

## Instructions for coding agents

When a prompt or a project instruction file names this repository, read this section. It tells
you when the rules apply, which files to read, and how to apply them.

### When the rules apply

The rules apply when both of these conditions are true:

1. The task writes, changes, reviews, or refactors code in a Java, Spring Boot, or Thymeleaf project.
2. The prompt or the project refers to this repository in one of these ways:
   - The prompt names this repository, by URL or by the name `java-spring-style`.
   - The project instruction file (`CLAUDE.md`, `AGENTS.md`, `.cursorrules`, or similar) names
     this repository.
   - The project has files in `.claude/rules/` that contain the line `Managed by java-spring-style`.

The rules are binding on every code edit in that project. They carry the same weight as the
project instruction file. If the project instruction file states an explicit exception to a rule,
the exception wins. In every other case, the rule wins.

### Which rule files to read

The rules live in four files under `rules/`. Each file covers one set of file types. Find every
file type that the task touches, then read each rule file in the table for that type. Read the
whole file. The four files total about 620 lines. If the task spans several types, or if you are
not sure, read all four.

| The task touches | Read |
|---|---|
| Java production code (`src/main/java/**`) | `rules/naming.md`, `rules/java-style.md` |
| Java tests (`src/test/java/**`) | `rules/naming.md`, `rules/java-style.md`, `rules/testing.md` |
| Thymeleaf templates (`src/main/resources/templates/**`) | `rules/naming.md`, `rules/frontend-style.md` |
| JavaScript (`src/main/resources/static/js/**`) | `rules/naming.md`, `rules/frontend-style.md` |
| SCSS or CSS (`src/main/resources/static/css/**`) | `rules/frontend-style.md` |
| Message bundles (`messages*.properties`) | `rules/frontend-style.md` |

If the project uses a different directory layout, pick the row by file type, not by path.

Each rule file starts with a `paths:` block between two `---` lines. The block lists the globs
that Claude Code uses to load the file. The rules start after the second `---` line.

### How to read the files

Read the files from the raw URLs:

- https://raw.githubusercontent.com/barnaclejive/java-spring-style/main/rules/naming.md
- https://raw.githubusercontent.com/barnaclejive/java-spring-style/main/rules/java-style.md
- https://raw.githubusercontent.com/barnaclejive/java-spring-style/main/rules/frontend-style.md
- https://raw.githubusercontent.com/barnaclejive/java-spring-style/main/rules/testing.md

If you cannot read URLs, clone the repository and read the same files from disk:

```bash
git clone --depth 1 https://github.com/barnaclejive/java-spring-style /tmp/java-spring-style
cat /tmp/java-spring-style/rules/*.md
```

If the raw URLs and the HTTPS clone return 404, the repository is private. Ask the user for a
GitHub token or for a clone over SSH.

If the project already has copies in `.claude/rules/` (see [Use with Claude Code](#use-with-claude-code)),
read those copies instead. They come from this repository.

`skills/*/SKILL.md` holds the same text as `rules/*.md` with different frontmatter. `build.py`
generates the skills from the rule files. Read one set or the other, not both.

### How to apply the rules

1. Before you write the first line of code, read the rule files for every file type in the task.
2. Apply the rules to the code that you write or change. If the code around your change breaks a
   rule, your change must still obey the rule.
3. Leave code that the task does not touch as it is. A style pass on other code is a separate task
   that the user must ask for.
4. When you review code, compare the diff against the rule files. Report each violation with the
   rule file and the section heading, for example `rules/java-style.md, "Class member ordering"`.
5. Before you report the task as done, compare your change against the rule files one more time.
   Correct every violation that you find.
6. Read the rule files for each task. Do not work from memory of them or from the summary below.
   The files hold the exact wording, the examples, and the exceptions.

The examples in the rule files use class names from a made-up subscription-billing domain
(`SubscriptionDetailDto`, `BillingPeriod`, `ServiceRegionService`, `CatalogItemStatus`, and
similar). No such project exists. Do not look for those classes in the project. Apply the shape of
each example to the class names of the project. The names are long and unabbreviated on purpose,
because a rule about long, unabbreviated names cannot be shown with `FooDto`.

### The non-negotiables

This list is a summary for an agent that reads only this README. It does not replace the rule files.

- Name every variable after its full class name. No abbreviations, no generic names (`v`, `el`,
  `tmp`, `dto`).
- Java: never `var`. `final` on every parameter and local. 140-character lines.
  `LoggerFactory.getLogger(getClass())`. Never `log.warn`.
- Templates: no hardcoded user-facing strings and no fallback text. Every string comes from
  `messages.properties`.
- Never build a string with `+`. Use `#{key(args)}` for text, `@{...}` for URLs, and `|...|` for
  identifiers.
- Tests: JUnit 5 + Mockito with `@ExtendWith(MockitoExtension.class)`, AssertJ assertions, and
  `methodUnderTestScenarioExpectedBehavior` names.
- Never leave production code that only tests exercise. Delete the code and its tests together.

## What is in the repository

```text
rules/                   the rule files, single source of truth, with paths: frontmatter
  naming.md
  java-style.md
  frontend-style.md
  testing.md
skills/                  generated from rules/, one Claude Code skill per rule file
commands/style-sync.md   Claude Code command that copies rules/ into a project's .claude/rules/
CLAUDE-snippet.md        block to paste into a project's CLAUDE.md
build.py                 regenerates skills/ from rules/
.claude-plugin/          plugin and marketplace manifests
```

| Rule file | Skill | Covers |
|---|---|---|
| `rules/naming.md` | `naming-style` | Variable names match the class name, no abbreviations, `{Source}To{Target}` converter methods |
| `rules/java-style.md` | `java-style` | No `var`, `final` everywhere, 140-character lines, record and accessor formatting, logger declaration, log-level discipline, magic strings, member ordering, blank-line and comment rules |
| `rules/frontend-style.md` | `thymeleaf-style` | No hardcoded user-facing strings, parameterized i18n messages, the never-concatenate ladder, Bootstrap-first styling, semantic headings |
| `rules/testing.md` | `testing-style` | JUnit 5 + Mockito scaffolding, AssertJ, test naming, fixtures |

## Use with Claude Code

Install the plugin:

```bash
# in Claude Code
/plugin marketplace add barnaclejive/java-spring-style
/plugin install java-spring-style@java-spring-style
```

Then, in each project that uses these rules:

```bash
/style-sync          # copies rules/ into the project's .claude/rules/
```

and paste the block from [CLAUDE-snippet.md](CLAUDE-snippet.md) into the project `CLAUDE.md`.

### Why both skills and rule files

Claude Code has two ways to load this content, and neither one is guaranteed to fire:

- **Skills** load when the task matches the skill `description`, or on an explicit `/skill-name`.
- **`.claude/rules/*.md`** load when an edited file matches the `paths:` frontmatter.

The two cover different moments, so the plugin ships both. The `CLAUDE.md` snippet is the
backstop. It is the only content that loads on every prompt. So it names the non-negotiables and
tells Claude to load the detail before it finishes a change.

## Use with other agents

Add a block like this to the project instruction file. The file name depends on the agent:
`AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`, `GEMINI.md`, or similar.

```markdown
## Code style rules

This project uses the rules in https://github.com/barnaclejive/java-spring-style.
Before you write, change, or review Java, Thymeleaf, JavaScript, SCSS, or test code, read the
README of that repository. Then read the rule files that it lists for the file type. Apply the
rules to every code edit. Before you finish, compare your change against those files again.
```

You can also name the repository in a prompt:

```text
Follow the style rules in https://github.com/barnaclejive/java-spring-style.
```

An agent that reads this README finds the procedure in
[Instructions for coding agents](#instructions-for-coding-agents).

You can also copy the files in `rules/` into the rules directory of the project. The rule text
starts after the `paths:` frontmatter. If your agent does not use the frontmatter, remove it.

## Editing the rules

`rules/` is the single source of truth. `skills/` is generated from it.

```bash
# edit rules/java-style.md, then
python3 build.py
git add rules skills && git commit
```

`build.py` swaps the `paths:` frontmatter of a rule file for the `name:` / `description:`
frontmatter that a skill needs. The body is copied verbatim, so the two cannot drift.
Skill descriptions live in the `SKILLS` map at the top of `build.py`.

If you add a rule to the non-negotiables, update the list in this README and in
[CLAUDE-snippet.md](CLAUDE-snippet.md).

## Project-local rules

Anything specific to one codebase belongs in a separate file in the project `.claude/rules/`
directory, with its own `paths:` frontmatter. Examples: a house UI style guide, domain conventions,
shared utilities. `/style-sync` writes only the four files above and leaves everything else alone.

## License

MIT
