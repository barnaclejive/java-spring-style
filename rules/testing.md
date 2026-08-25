---
paths:
  - "src/test/**"
---

# Test Conventions

These rules are binding on every test edit. The Java style rules (`java-style.md`) and the naming rules (`naming.md`) apply to test code too.

- **`TestFixtures`** in the test root provides shared entity builders (`buildPaymentTerm`, `buildServiceRegion`, `toStream`). Use these builders. Do not duplicate them in each test file.
- All tests use **AssertJ** assertions (`assertThat`, `assertThatThrownBy`, `hasMessageContaining`), not JUnit assertions (`assertEquals`, `assertTrue`).
- **Test class location mirrors production**: the test for `com.example.admin.usage.service.impl.UsageServiceImpl` lives at `src/test/java/com/example/admin/usage/service/impl/UsageServiceImplTest.java`. Test class names are `<ClassUnderTest>Test`.
- **Unit-test scaffolding**: JUnit 5 + Mockito via `@ExtendWith(MockitoExtension.class)`, `@Mock` for collaborators, `@InjectMocks` for the system under test. Each `@Mock` field gets its own `@Mock` annotation line above the field declaration, with a blank line between mock declarations (this matches the visual rhythm of the rest of the codebase).
- **Test method naming**: `methodUnderTestScenarioExpectedBehavior`. Write the full name in camelCase. Do not use an underscore. Examples: `parseAndPreviewCsvEmptyCsvReturnsError`, `deleteReferencedByProgramThrowsException`, `validateActiveWithMissingStartRejectsStartDateTime`. Read the name as "method `X`, when `scenario`, returns/throws/rejects `Y`." Keep the three parts in this order. The Checkstyle `MethodName` rule with the pattern `^[a-z][a-zA-Z0-9]*$` rejects an underscore in a method name. That rule is common in enterprise builds, and it applies to test sources too.
- **Test method body formatting**: put a blank line directly after the opening `{` of the `@Test` method (this matches the main blank-line rule). Group the body into the standard Arrange / Act / Assert phases with a single blank line between phases. Do not write `// arrange` / `// act` / `// assert` comments.
- **Static imports**: `assertThat` and `assertThatThrownBy` from AssertJ. `when`, `verify`, `never`, `any`, and `eq` from Mockito. Import the test fixture builders (`buildPaymentTerm`, `buildServiceRegion`, `toStream`) as static where used.
- **Per-test helper builders**: a private (non-static) `buildXxx(...)` method at the bottom of the test class, below all `@Test` methods. Use these builders instead of the same setup in multiple tests. When a second test class needs a builder, promote it to `TestFixtures`.
- **`final` on test locals** (parameters and locals inside test methods and helper builders): yes, the same rule as production code.
