# Standalone system prompt

For harnesses without skill or rules-file support: paste the block below into your system prompt,
custom instructions, `AGENTS.md`, or `.cursorrules`. It condenses `rules/naming.md`,
`rules/java-style.md`, and `rules/frontend-style.md` into one prompt. The full files, with the
examples and the edge cases, are in `rules/` of https://github.com/barnaclejive/java-spring-style.
The test rules in `rules/testing.md` are not included.

---

When you write, change, or review Java, Thymeleaf, JavaScript, or SCSS code in a Spring Boot project, obey these rules. They are binding on every edit. If the code around your change breaks a rule, your change must still obey the rule. Models get whitespace wrong more often than any other rule in this prompt. Give the JAVA WHITESPACE and HTML WHITESPACE sections the same care as the rest.

NAMING. Name every variable after the full, lowercased simple class name of its type: `SubscriptionDetailDto` → `subscriptionDetailDto`, never `sub`, `subscription`, or `detail`. Never abbreviate a name, and never drop a `Dto`, `Projection`, or `Entity` suffix. This applies to fields, parameters, locals, lambda parameters, JavaScript variables, and Thymeleaf `th:each` variables. Never use a generic name: `v`, `el`, `e`, `x`, `tmp`, `val`, `obj`, `dto`, `btn`, `rows`, `list`, `items`, `data`, `results`. The rule holds even for a variable that only the next line uses. For a `String` or a primitive, name the variable after what it holds: `errorMessage`, `serviceRegionCode`. Name a typed collection with the plural of the element class: `List<UsagePreviewRow>` → `usagePreviewRows`. If the collection comes from a session attribute, a cache, or a map key, name it after that key. The only short names allowed are the loop counters `i` and `j`, and `e` in a `catch` block. A URL query-parameter string can stay short, but the bound variable must be full: `@RequestParam(value = "s") final String sortCode`. Name a converter method `{SourceClassName}To{TargetClassName}` with both names in full: `orderProjectionToOrderSummaryDto`, never `toSummaryDto`.

JAVA. Never use `var`. Write the explicit type. Put `final` on every field, parameter, and local in implementations, constructors, and lambdas. Do not put `final` on interface method parameters. Use primitive `boolean` for a non-nullable entity field. Use a `record` for a DTO, in the `dto` package of its domain. Prefer streams and `Optional` over loops. Store money as `BigDecimal` with `@Column(precision = 19, scale = 2)`. For a null or blank test on a string, use `StringUtils.isBlank` or `StringUtils.isNotBlank` from commons-lang3. Never hand-write `x == null || x.isBlank()`. For a collection that arrives as input, use `CollectionUtils.isEmpty` from collections4. For a collection built in the same code path, or returned by a repository or a stream, use plain `.isEmpty()`. Pass a nullable request string straight to the model: `model.addAttribute("search", search)`, never `search != null ? search : ""`. Thymeleaf treats `null` and `""` the same, and `@{...(param=${x})}` renders `param=` for both. Keep an explicit fallback only where a consumer is not null-safe: `Collectors.toMap`, Java string concatenation, or an equality test where `null == null` is wrong.

JAVA WHITESPACE. This is the highest-value formatting rule in the codebase, and the one that a review finds broken most often. A method body reads as short paragraphs, one per step, with one blank line between paragraphs. Never write a body as one dense block. Never put two blank lines in a row. When you edit a method, keep the blank lines that already surround your change. Put a blank line after the `{` of every method that holds logic. Do not put one in a getter, a setter, a constructor that only assigns fields, or a one-statement delegate. Put a blank line after the `{` of a substantive block. A block is substantive when it declares a local, nests a block, or has more than one step. Keep a guard return, a one-value branch, or a lone flash message tight. If a `try` body has more than one statement, pad it. Put a blank line after `try {`, before `} catch`, after `} catch (...) {`, and after the last `}`. Keep a one-statement `try` / `catch` tight. Between statements, in priority order: keep a run of same-shape one-liners together (`addAttribute` calls, setters, a local and the `if` that tests it). Give a multi-line statement a blank line above and below. If it completes the one-liner above it, keep them together. Put a blank line after the closing `}` of a guard. If the statement above the guard is one line, put no blank line above the guard. Put a blank line between independent `if` blocks. Put a blank line between phases: resolve input, look up data, compute, build the result. Give the final `return` its own paragraph. If it only hands back what the one or two lines above produced, keep it attached. Put exactly one blank line between methods. Put one blank line between member groups and none between sibling fields or constants. If a case is unclear, add the blank line. The shape:

```java
public String commit(final HttpSession session, final RedirectAttributes redirectAttributes) {

    final List<CatalogItemCsvRow> catalogItemCsvRows = claimCatalogItemCsvRows(session);

    if (CollectionUtils.isEmpty(catalogItemCsvRows)) {
        redirectAttributes.addFlashAttribute("error",
                messageSource.getMessage("catalogItem.flash.noDataToCommit", null, LocaleContextHolder.getLocale()));
        return REDIRECT_CATALOG_ITEM;
    }

    try {

        catalogItemService.commitUpload(catalogItemCsvRows);
        redirectAttributes.addFlashAttribute("success", messageSource.getMessage(
                "catalogItem.flash.committed",
                new Object[]{catalogItemCsvRows.size()},
                LocaleContextHolder.getLocale()));

    } catch (final Exception e) {

        log.error("The catalog item upload was not committed", e);
        redirectAttributes.addFlashAttribute("error",
                messageSource.getMessage("catalogItem.flash.commitError", null, LocaleContextHolder.getLocale()));
    }

    return REDIRECT_CATALOG_ITEM;
}
```

JAVA LINE BREAKS. The limit is 140 characters. If a statement fits in 140 characters, keep it on one line. Never split a statement for looks. If a statement does not fit, break it with one of these patterns. Declarations in implementations and controllers: align each continuation parameter under the first parameter, one annotated parameter per line. Interface declarations: one parameter per line with an 8-space continuation indent. Call arguments: break after the `(`, then one argument per line with an 8-space indent. Stream chains: each `.call(...)` on its own line with an 8-space indent. Never break a ternary between its `?` arm and its `:` arm. If the statement is too long, break before the `?` and keep `? a : b` together. If that still does not fit, extract a local or a helper. Two shapes ignore the one-line rule. A `record` always puts each component on its own line with an 8-space indent. The closing `) {}` sits on its own line at the indent of the declaration. A getter or setter always uses the multi-line body form. Keep the getter and setter of one field together, with one blank line between field pairs.

MEMBER ORDER. Declare class members in this order. Put one blank line between groups and none between siblings. 1) The logger. 2) `static final` constants. 3) `private final` instance fields, injected dependencies first, then `@Value` values. 4) One constructor with constructor injection and no `@Autowired`. 5) Public methods, `@Override` methods first in interface order. 6) Private helpers directly below their callers. 7) Shared helpers and converters at the bottom. For an enum: constants, static lookup map, instance fields, constructor, accessors, static factories. Put a helper with one caller directly after that caller. If a helper calls a second helper, put the second helper directly after the first. The code then steps down from the public method to the details. Put a helper with several nearby callers after the last caller. Put a helper with distant callers in the shared group at the bottom. If a class has three or more converters, keep them together at the bottom. Never put a helper above the first public method. If a helper and its caller do not fit on one screen, move the helper.

LOGGING. Declare the logger as `private final Logger log = LoggerFactory.getLogger(getClass());`, never static and never with `ClassName.class`. Never use `log.warn`. Use `log.error` only for an unexpected failure that a developer must investigate. Examples: a catch-all `catch (final Exception e)`, a 5xx branch, a lost connection, a programming error. Never log an expected, handled problem. Examples: a validation failure, a bad upload, a business-rule rejection caught by name, a not-found lookup, an error flash with a redirect. If a `log.error` sits beside a user-facing error message in the same path, delete the log line. The test: if no realistic incident makes a developer miss the entry, the entry must not exist.

MAGIC STRINGS. If the same literal occurs in two or more places, extract it. A closed set of values (`"DRAFT"` / `"SUBMITTED"`, `"asc"` / `"desc"`) becomes an `enum` in the `dto` package. Reference it in Thymeleaf as `T(fully.qualified.Enum).CONSTANT`. One repeated string (a column name, a session key, a CSV header) becomes a `private static final String` in the class that owns it. User-facing text becomes a message key. The bar is the occurrence count, not the importance. When you add a `*Status`, `*Type`, `*Mode`, `*Kind`, or `*State` concept, create the enum on day one.

COMMENTS. A comment in a method body does one of three jobs. It explains why, it summarizes a dense chain, or it marks a step. Keep step and summary comments. Do not delete one because the code "says the same thing". Do not comment a line that any reader understands at a glance. Keep a comment to one line where possible, and update it when the code changes. Prefer a better name over a comment. Use `//` on the line above the code. Use a trailing comment only for a very short note. Never add a decorative divider such as `// --- getters and setters ---`. Write Javadoc only at class level, and only on an infrastructure class whose role the name does not show. Never write method-level Javadoc in application code.

HTML WHITESPACE. Indent with 4 spaces. Never use tabs. Each nested element indents one level from its parent. The children of `<html>`, `<body>`, `<thead>`, `<tbody>`, and `<tfoot>` are the exception: they stay at the indent of the parent. So `<tr>` sits at the indent of `<tbody>`, and `<td>` indents one level from `<tr>`. `<th:block>` indents like any element. Put every block element on its own line. Keep an element with an empty body on one line: `<span th:text="#{key}"></span>`. Keep a short inline pair on one line: `<i class="fa-solid fa-plus me-1"></i><span th:text="#{key}"></span>`. Put plain attributes before `th:` attributes, and `th:text` last. A structural `th:if`, `th:unless`, or `th:each` can come first. When a tag has many attributes, group related attributes on a line and break between the groups. Align every continuation line under the first attribute of the tag. Never use a fixed indent for continuation attributes. A template has no line limit. Never break inside a Thymeleaf expression: a long `th:href` or `th:with` value stays on one line. Two values break at their commas. A `th:with` with several assignments puts one assignment per line, aligned under the first. A fragment call puts one parameter per line, indented 2 spaces past the tag, with `)}"></div>` on the last parameter line. A blank line separates sibling blocks. Examples: page sections, form cards, `row` columns, the modals at the end of `<main>`, the top-level children of `<body>`. Inside a block, keep the leaf lines tight. A label, its input, and its feedback have no blank line between them. Do not put a blank line after an opening tag or before a closing tag. `<body>` and `<main>` are the exception. Their top-level blocks can have a blank line on each side. Never put two blank lines in a row. Introduce each major block with a comment on its own line, at the indent of the block: `<!-- Order count recap — each tile opens its card -->`. Put a blank line before the comment and none between the comment and its block. The code inside `<script th:inline="javascript">` starts at the indent of the `<script>` tag. The shape:

```html
<main id="main-content" class="container content-wrapper" role="main"
      th:with="sortParam=${#strings.isEmpty(currentSort) ? null : currentSort},
               searchParam=${#strings.isEmpty(search) ? null : search}">
    <div th:replace="~{fragments/flash-messages :: alerts}"></div>

    <div th:replace="~{fragments/page-header :: pageHeader(
      title=${subscription.name},
      backUrl=@{/admin/subscriptions},
      backTextKey='regions.button.back')}"></div>

    <!-- Service regions — one row per region -->
    <div class="card mb-4" id="serviceRegionCard"
         th:data-search-base-url="@{/admin/regions(page=0, sort=${sortParam})}">
        <div class="card-header d-flex justify-content-between align-items-center">
            <h2 class="fs-5 mb-0" th:text="#{regions.heading}"></h2>
            <button type="button" class="btn btn-outline-primary btn-sm" id="addRegionBtn"
                    data-bs-toggle="modal" data-bs-target="#addRegionModal">
                <i class="fa-solid fa-plus me-1"></i><span th:text="#{regions.button.add}"></span>
            </button>
        </div>
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-striped mb-0">
                    <thead>
                    <tr>
                        <th scope="col" th:text="#{regions.table.code}"></th>
                        <th scope="col" th:text="#{regions.table.name}"></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr th:each="serviceRegion : ${serviceRegions}" th:id="|serviceRegion-row-${serviceRegion.id}|">
                        <td th:text="${serviceRegion.code}"></td>
                        <td th:text="${serviceRegion.name}"></td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Add region — confirmation modal -->
    <div class="modal fade" id="addRegionModal" tabindex="-1"
         aria-labelledby="addRegionModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title fs-5" id="addRegionModalLabel" th:text="#{regions.add.title}"></h2>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" th:aria-label="#{alert.close}"></button>
                </div>
            </div>
        </div>
    </div>

</main>
```

TEMPLATES: NO HARDCODED TEXT. `messages.properties` is the single source of every word a user reads. A template holds zero user-facing English. The test: remove every `#{...}` and `${...}` expression. If a reader can still tell the language of the page, the template has a hardcoded string. User-facing text is any text that reaches the screen, the accessibility tree, or the browser chrome. That includes element text, punctuation between elements, `title`, `alt`, `placeholder`, `aria-label`, a submit `value`, `data-*` text, the `<title>`, a fragment parameter, and script literals. Numerals, HTML entities, CSS classes, IDs, `data-bs-*` values, and paths inside `@{...}` are exempt. Never put fallback text in an element. Write `<span th:text="#{key}"></span>` with an empty body. The same applies to `th:text="${...}"`. Never put a plain attribute beside its `th:` form. Delete `aria-label` beside `th:aria-label`. The same applies to `placeholder`, `title`, and `src`. Never pass a literal to a fragment parameter that renders as text. Pass `#{key}`. The exception is a parameter that takes a key by name, such as `messageKey` or `titleKey`. Never build a sentence with `+`. Write a parameterized message, `order.detail.heading=Order {0}`, and call it as `#{order.detail.heading(${order.orderCode})}`. In a message with parameters, double every apostrophe (`program''s`). Never leave a `?`, `:`, `(`, or `-` as bare text between elements. Pull the whole phrase into one message. Put inline `<strong>` or `<code>` in the message value, and render it with `th:utext`. Use `th:utext` only on message values that the code owns, never on user data. Never hardcode a currency symbol, a date separator, a unit, or an empty-value dash. Use `format.*` keys and `#{common.empty}`. Never hardcode an absolute URL or a URL prefix in display text. Put the host in `application.yml` and the sentence in a message. When you add a key, add it to `messages.properties` and to `messages_fr_CA.properties` at the same position. Name it `section.subsection.element`. Write the value in Simplified Technical English.

TEMPLATES: NEVER CONCATENATE. `+` in a template is almost always wrong. Work down this ladder and stop at the first match. 1) Text a person reads: a parameterized message `#{key(args)}`. Never glue a message to a value with `|...|`. 2) A URL: `@{/user/{id}/orders(id=${id}, page=0)}` for `th:href`, `th:src`, and `th:action`. It resolves the context path and encodes every value. A null value renders as `?x=`, not omitted. A path variable is encoded too, so use `__${path}__` only for a trusted raw segment. A list expands to repeated parameters. For a non-HTTP scheme, use `|mailto:${email}|`. Store an external URL template in `application.yml` with `{slug}` tokens and use it as the `@{...}` base. Never use `#request.contextPath`. 3) A machine identifier (`id`, `name`, `for`, `data-bs-target`, a map key): literal substitution `|billingPeriod-row-${billingPeriod.id}|`. Do not put `#{...}` or `@{...}` inside `|...|`. 4) A value that you need more than once: name it once with `th:with`. Assignments evaluate in order, and a name must never reference itself. 5) In JavaScript: `new URL(base, window.location.origin)` with `searchParams.set()` and `.delete()`, never string appends. Build markup with DOM calls and `.text()`, never with `+` on HTML strings. `+` stays correct only inside `${...}` for a Java-side value such as a map key.

TEMPLATES AND SCSS. Never hard-code a dimension such as `style="width: 160px"`. Use Bootstrap layout utilities, responsive classes, and SCSS variables. If no class can express it, ask the user before you write a pixel value. Never pick an `<h1>`–`<h6>` tag for its size. The heading level follows the document outline, with no skipped levels. Set the size with `fs-1` to `fs-6` or `display-*`: a compact page title is `<h1 class="fs-4">`, never `<h4>`. For a label or an emphasis, use a `<div>`, `<span>`, or `<p>` with a font-size utility. Never override a heading size with an inline style or a one-off SCSS rule. Prefer Bootstrap utilities (`p-*`, `m-*`, `gap-*`, `fs-*`, `fw-*`, `text-*`, `bg-*`, `border*`, `d-*`, `justify-content-*`) and existing project classes over custom SCSS. Write custom SCSS only for what no class can express: project colors, animations, hover suppression, scroll behavior, scoped overrides.

JAVASCRIPT. Use `const` by default and `let` only for a value that the code reassigns. Never use `var`. Indent with 4 spaces. Do not apply the Java blank-line rules to JavaScript. Keep a function body tight, with no blank line after its `{` and none before its `return`. Put one blank line between functions and between logical groups of statements. The naming rules apply: `button`, `element`, `event`, never `btn`, `el`, `evt`. JavaScript has no access to the message bundle, so never write a string literal that reaches the screen. In an inline script, use `th:inline="javascript"` and collect the strings in one `labels` object: `serviceRegion: /*[[#{usage.confirm.table.serviceRegion}]]*/ ''`. Keep the `''` empty. In an external `static/js` file, read the strings from `th:data-msg-*` attributes on a root element through `dataset`. Substitute a placeholder with `.replace('{0}', value)`. Never write a default string in a shared module, such as `options.btnText || 'Confirm'`. The caller supplies the text. Never use `alert()`, `confirm()`, or `prompt()`. Use `ConfirmModal` or the toast helper with a message key.

SELF-CHECK before you return. Whitespace first. In every Java method that you touched, make sure that a blank line follows the `{`. Make sure that a padded `try` / `catch` has its four blank lines. Make sure that a blank line follows each guard and that the final `return` stands in its own paragraph. Make sure that no method body is one dense block. In every template that you touched, make sure that the indent is 4 spaces. Make sure that `<tr>` sits at the indent of `<tbody>`. Make sure that continuation attributes align under the first attribute. Make sure that blank lines separate sibling blocks and nothing else. Then scan the Java diff for `var`, a missing `final`, and a dropped `Dto` suffix. Scan it for an abbreviated or generic name and a repeated literal. Then scan it for `log.warn`, a `log.error` beside a user-facing error message, and a line over 140 characters. In templates, scan for `+` and for text inside an element that has `th:text`. Scan for an attribute beside its `th:` form and a literal fragment parameter. Then scan for a bare punctuation node, a heading tag picked for size, and an inline dimension. In scripts, scan for a string literal that reaches the screen, `alert(`, and a URL built with `+`.

---

## Word-budget version (~330 tokens)

For tight system prompts:

> Java + Spring Boot + Thymeleaf style. Whitespace matters most. Java: a blank line after every method `{` (not in accessors or field-assignment constructors), a padded `try` / `catch`, a blank line after each guard block, the final `return` in its own paragraph, one blank line between steps, never a dense block. HTML: 4-space indent, no indent under `html`, `body`, `thead`, `tbody`, continuation attributes aligned under the first attribute, one fragment parameter per line, blank lines only between sibling blocks, a comment above each major block. Name every variable after its full class name, never abbreviated (`subscriptionDetailDto`, not `sub`), converters `{Source}To{Target}`. Never `var`, `final` on every field, parameter, and local, 140-character lines, records for DTOs, `StringUtils.isBlank`. Logger via `LoggerFactory.getLogger(getClass())`, never `log.warn`, `log.error` only for unexpected failures. Repeated literals become enums, constants, or message keys. Templates: zero hardcoded user-facing text, no fallback text, no `+`: `#{key(args)}` for text, `@{...}` for URLs, `|...|` for identifiers, `th:with` for reuse. Bootstrap utilities over custom SCSS, heading levels by outline, not by size. JavaScript: `const`, tight function bodies, no string literals, strings via inlining or `data-*`.
