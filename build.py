#!/usr/bin/env python3
"""Regenerate skills/ from rules/.

rules/*.md is the single source of truth for the rule text. Each rule file carries
`paths:` frontmatter, which the .claude/rules/ mechanism uses. A skill needs
`name:` and `description:` frontmatter instead. This script swaps one for the other,
so the same body serves both loading paths and cannot drift.

Run it after any edit to rules/, then commit both directories:

    python3 build.py
"""
import io
import os

SKILLS = {
    "naming-style": {
        "rules": "naming.md",
        "description": (
            "Variable and method naming for Java, JavaScript, and Thymeleaf. Name every variable "
            "after its full class name, never abbreviate or use generic names (v, el, tmp, dto, po), "
            "and name converter methods {SourceType}To{TargetType}. Use when writing or reviewing "
            "any Java, JavaScript, or Thymeleaf code."
        ),
    },
    "java-style": {
        "rules": "java-style.md",
        "description": (
            "Java coding conventions for Spring Boot projects: never use var, final on every "
            "parameter and local, 140-character lines, record and accessor formatting, "
            "LoggerFactory.getLogger(getClass()), log-level discipline (never log.warn), "
            "StringUtils for blank checks, magic-string extraction, and class member ordering. "
            "Use when writing, reviewing, or refactoring any Java file."
        ),
    },
    "thymeleaf-style": {
        "rules": "frontend-style.md",
        "description": (
            "Thymeleaf, JavaScript, and SCSS conventions. No hardcoded user-facing strings and no "
            "fallback text: every string comes from messages.properties. Never concatenate with + "
            "in a template: use parameterized #{key(args)} messages, @{...} URL expressions, and "
            "|...| literal substitution. Bootstrap utilities over custom SCSS, semantic heading "
            "levels, and URLSearchParams in JavaScript. Use when editing Thymeleaf templates, "
            "static JavaScript, SCSS, or message bundles."
        ),
    },
    "testing-style": {
        "rules": "testing.md",
        "description": (
            "Test conventions for JUnit 5 and Mockito: @ExtendWith(MockitoExtension.class) "
            "scaffolding, AssertJ assertThat and assertThatThrownBy, "
            "methodUnderTest_scenario_expectedBehavior naming, shared fixtures, per-test builders, "
            "and body formatting. Use when writing or changing tests."
        ),
    },
}

HERE = os.path.dirname(os.path.abspath(__file__))


def strip_frontmatter(text):
    """Return the body of a markdown file, dropping a leading --- ... --- block."""
    if not text.startswith("---"):
        return text
    end = text.index("\n---", 3)
    return text[end + len("\n---"):].lstrip("\n")


def main():
    for name, spec in sorted(SKILLS.items()):
        source = os.path.join(HERE, "rules", spec["rules"])
        body = strip_frontmatter(io.open(source, encoding="utf-8").read())
        target_dir = os.path.join(HERE, "skills", name)
        os.makedirs(target_dir, exist_ok=True)
        frontmatter = "---\nname: %s\ndescription: %s\nlicense: MIT\n---\n\n" % (name, spec["description"])
        header = ("<!-- Generated from rules/%s by build.py. Edit the rule file, not this file. -->\n\n"
                  % spec["rules"])
        io.open(os.path.join(target_dir, "SKILL.md"), "w", encoding="utf-8").write(frontmatter + header + body)
        print("generated skills/%s/SKILL.md from rules/%s" % (name, spec["rules"]))


if __name__ == "__main__":
    main()
