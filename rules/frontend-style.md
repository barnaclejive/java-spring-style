---
paths:
  - "src/main/resources/templates/**"
  - "src/main/resources/static/js/**"
  - "src/main/resources/static/css/**"
---

# Frontend Style — Thymeleaf, JavaScript, SCSS

These rules are binding on every template, JavaScript, and SCSS edit. The naming rules in `naming.md` apply equally to JavaScript variables and Thymeleaf `th:each` iteration variables.

## JavaScript Conventions

- **Prefer `const` over `let`. Never use `var`.** `const` is the JS equivalent of the Java `final`. Use `const` for all bindings. When the code genuinely reassigns a variable, use `let`. `var` is forbidden (function-scoped, hoisted, no reassignment protection).
- **Blank lines in JavaScript follow the JavaScript layout, not the Java layout.** Indent with 4 spaces. Keep a function body tight: no blank line after its `{` and none before its `return`. Put one blank line between functions and between logical groups of statements.

## Template & SCSS Rules

- **NEVER hard-code dimensions** (for example, `style="width: 160px"`, `style="max-height: 300px"`) in templates or inline styles. Use Bootstrap layout utilities, responsive classes, and SCSS variables instead. Use a hard-coded pixel value only in an extreme edge case where no Bootstrap or CSS class alternative exists — and ask the user first.
- **NEVER use `<h1>`–`<h6>` elements for visual sizing.** Heading elements exist only to express the content hierarchy of the page for screen readers, assistive tech, and document outline tools. Pick the heading level that matches the place of the element in the page: the page title is `<h1>`, section headings are `<h2>`, sub-section headings are `<h3>`, and so on, with no skipped levels. If you need text at a specific size, apply a Bootstrap font-size utility (`fs-1` … `fs-6`, or `display-1` … `display-6` for hero text) or an existing theme typography class. Never pick a smaller or larger heading tag only to get its default font size. Never override the font-size of a heading with an inline `style` or a one-off SCSS rule. If a piece of text is purely a label or a visual emphasis (not a section heading), use a `<div>`, `<span>`, or `<p>` with the applicable font-size utility, not an `<h*>` tag. Examples: a page title that must look visually compact is `<h1 class="fs-4">`, not `<h4>`. A card section title is `<h2 class="fs-5 mb-0">` (the next semantic level after the page `<h1>`), not `<h5>`. The "Buttons", "Forms", and "Cards" labels inside a design-system spec are `<h4>` because they sit inside an `<h3>` sub-section, not because they need a medium size.
- **ALWAYS prefer Bootstrap utility classes (or existing global theme/style classes) over custom SCSS** — for spacing (`p-*`, `m-*`, `gap-*`), font size (`fs-1` … `fs-6`), font weight (`fw-bold`, `fw-normal`), text color (`text-muted`, `text-end`, plus your own theme colour utilities), background (`bg-*`), borders (`border`, `border-top`, `border-0`), display (`d-flex`, `d-none`), flex (`justify-content-*`, `align-items-*`), and similar concerns. The Bootstrap spacing and size utilities are token-driven (`$spacer`, `$h*-font-size`), so the values stay consistent. The utility classes your project already defines (in `_utilities.scss` or its equivalent) are also preferred over new SCSS. Write custom SCSS only when no Bootstrap class and no existing project class can express the rule — typically: project-specific colors, animations, hover-state suppression, scroll behavior, or selector-scoped overrides. If you write a one-off `.foo-lg { font-size: 1rem; padding: 0.55em 1em; }`, replace it with `class="fs-6 py-2 px-3"` on the element.
- **NEVER build a string with `+` in a template.** The **Never Concatenate** section below gives the tool to use for each case.

## Template Whitespace

These rules are binding on every template edit. They describe the layout of every existing template, which is the layout that the IntelliJ IDEA default HTML style produces. A review finds whitespace broken more often than any other template rule.

- **Indent with 4 spaces. Never use tabs.** Each nested element indents one level from its parent. The children of `<html>`, `<body>`, `<thead>`, `<tbody>`, and `<tfoot>` are the exception. They stay at the indent of the parent, so `<tr>` sits at the indent of `<tbody>`, and `<td>` indents one level from `<tr>`. `<th:block>` indents like any other element.
- **One block element per line.** Keep an element with an empty body on one line: `<span th:text="#{key}"></span>`. Keep a short inline pair on one line: `<i class="fa-solid fa-plus me-1"></i><span th:text="#{key}"></span>`.
- **Attribute order.** Put plain attributes before `th:` attributes, and `th:text` last. A structural `th:if`, `th:unless`, or `th:each` can come first.
- **Continuation attributes align under the first attribute.** When a tag has many attributes, group related attributes on a line and break between the groups. Align every continuation line under the first attribute of the tag. Never use a fixed indent for continuation attributes.
  ```html
  <button type="button" class="btn btn-outline-primary btn-sm" id="exportSelectedBtn" disabled
          data-bs-toggle="modal" data-bs-target="#exportConfirmModal">
  ```
- **No line limit, and no break inside an expression.** A long `th:href` or `th:with` value stays on one line. Two values break at their commas. A `th:with` with several assignments puts one assignment per line, aligned under the first one. A fragment call puts one parameter per line, indented 2 spaces past the tag, with the closing `)}"></div>` on the last parameter line.
  ```html
  <main id="main-content" class="container content-wrapper" role="main"
        th:with="sortParam=${#strings.isEmpty(currentSort) ? null : currentSort},
                 searchParam=${#strings.isEmpty(search) ? null : search}">
      <div th:replace="~{fragments/page-header :: pageHeader(
        title=${subscription.name},
        backUrl=@{/admin/subscriptions},
        backTextKey='regions.button.back')}"></div>
  ```
- **A blank line separates sibling blocks, and nothing else.** The blocks are page sections, form cards, `row` columns, the modals at the end of `<main>`, and the top-level children of `<body>`. Inside a block, keep the leaf lines tight. A label, its input, and its feedback have no blank line between them. Do not put a blank line after an opening tag or before a closing tag. `<body>` and `<main>` are the exception. Their top-level blocks can have a blank line on each side. Never put two blank lines in a row.
- **A comment introduces each major block.** Put the comment on its own line at the indent of the block, in the form `<!-- Order count recap — each tile opens its card -->`. Put a blank line before the comment and none between the comment and its block.
- **Inline scripts.** The code inside `<script th:inline="javascript">` starts at the indent of the `<script>` tag.

The shape of a page body:

```html
<main id="main-content" class="container content-wrapper" role="main">
    <div th:replace="~{fragments/flash-messages :: alerts}"></div>

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

## No Hardcoded User-Facing Strings

`messages.properties` is the single source of truth for every word the user reads. A template must contain zero user-facing English. These rules are absolute. Compare every template, fragment, and script edit against them.

**The test**: read the template and remove every `#{...}` message expression and every `${...}` model expression. If a reader can still tell what language the page is in, the template has a hardcoded string.

### What counts as a user-facing string

Any run of letters that reaches the screen, the accessibility tree, or the browser chrome:

- Element body text, including one-word text and punctuation between elements (`?`, `:`, `(`, `)`, `-`, `—`, `,`).
- `title`, `alt`, `placeholder`, `aria-label`, `value` (on a submit button), and `data-*` attributes that carry text into JavaScript.
- The `<title>` of the page, and every literal passed to a fragment parameter.
- String literals in inline `<script>` blocks and in `static/js/*.js` that reach `textContent`, `innerHTML`, `alert()`, `setAttribute('title', …)`, or `setAttribute('aria-label', …)`.

**Exempt**: numerals (`0`, `50`, `2`), HTML entities and symbols (`&laquo;`, `&rarr;`, `&#10003;`, `&nbsp;`), CSS class names, element IDs, `data-bs-*` Bootstrap values, and URL paths inside `@{...}`.

### The rules

- **NEVER put fallback text in a Thymeleaf template.** When you use `th:text="#{key}"`, `th:utext="#{key}"`, or `th:text="${var}"`, leave the element body empty. Write `<span th:text="#{some.key}"></span>`, NOT `<span th:text="#{some.key}">Fallback Text</span>`. A fallback is a second source of truth. It goes stale, and it flashes on screen before Thymeleaf replaces it. This applies to `${...}` model expressions too: `<title th:text="${title}">My App</title>` must become `<title th:text="${title}"></title>`.
- **NEVER put a fallback attribute next to its `th:` form.** `<nav th:aria-label="#{nav.main.label}" aria-label="Main navigation">` has the same defect: two sources of truth for one label. Delete the plain attribute and keep only `th:aria-label="#{nav.main.label}"`. The same applies to `placeholder` next to `th:placeholder`, `title` next to `th:title`, and `src` next to `th:src`.
- **NEVER pass a literal string to a fragment parameter that renders as text.** Pass a resolved message expression instead. Write `~{fragments/layout :: head(#{page.title.settings})}`, NOT `~{fragments/layout :: head('Settings')}`. A fragment parameter that names a message key (the `messageKey`, `titleKey`, `countKey`, and `backTextKey` parameters) is the one exception. That parameter takes the key itself as a string, and the fragment resolves it with `${#messages.msg(key)}`.
- **NEVER build a sentence with `+` string concatenation.** Concatenation freezes English word order, spacing, and punctuation into the template. Use a parameterized message with `{0}`-style placeholders, and pass the values with the `#{key(arg1, arg2)}` syntax.
  ```html
  <!-- WRONG — word order and the space are hardcoded -->
  <div th:text="#{order.detail.heading} + ' ' + ${order.orderCode}"></div>
  <div th:text="${serviceRegion.name} + ' (' + ${serviceRegion.code} + ')'"></div>
  <div th:text="${#temporals.format(startDateTimeCt, '__#{format.dateTime}__')} + ' (CT)'"></div>
  ```
  ```properties
  order.detail.heading=Order {0}
  format.nameCode={0} ({1})
  format.centralTime={0} (CT)
  ```
  ```html
  <!-- Correct — the message owns the whole sentence -->
  <div th:text="#{order.detail.heading(${order.orderCode})}"></div>
  <div th:text="#{format.nameCode(${serviceRegion.name}, ${serviceRegion.code})}"></div>
  <div th:text="#{format.centralTime(${#temporals.format(startDateTimeCt, '__#{format.dateTime}__')})}"></div>
  ```
  A message with parameters goes through `java.text.MessageFormat`. In a `MessageFormat` pattern a single quote is an escape character. Double every apostrophe in the value (`Do not delete the program''s orders.`) when you add parameters to a key.
- **NEVER leave punctuation or a separator as a bare text node between elements.** A `?`, a `:`, a `(`, or a `-` outside a `th:text` is a hardcoded string, and translators cannot reach it. Pull the whole phrase into one parameterized message.
  ```html
  <!-- WRONG — the question mark and the parentheses are hardcoded -->
  <p><span th:text="#{detail.delete.confirm}"></span> <strong th:text="${subscription.name}"></strong>?</p>
  <label><span th:text="${serviceRegion.name}"></span> (<code th:text="${serviceRegion.code}"></code>)</label>
  <!-- Correct -->
  <p th:utext="#{detail.delete.confirm(${subscription.name})}"></p>
  <label th:utext="#{edit.serviceRegions.option(${serviceRegion.name}, ${serviceRegion.code})}"></label>
  ```
  ```properties
  detail.delete.confirm=Do you want to delete <strong>{0}</strong>?
  edit.serviceRegions.option={0} (<code>{1}</code>)
  ```
  Put the inline markup (`<strong>`, `<code>`) in the message value and render with `th:utext`. The markup is part of how the sentence reads, so it belongs with the sentence. Use `th:utext` only for a message value that the code owns. Never use `th:utext` on user-supplied data.
- **NEVER hardcode a currency symbol, a date separator, or a unit.** These change with the locale. Route them through a format message.
  ```properties
  format.price.usd=${0}
  format.dateRange={0} - {1}
  ```
  ```html
  <td th:text="#{format.price.usd(${#numbers.formatDecimal(product.priceUsd, 1, 2)})}"></td>
  <span th:text="#{format.dateRange(${startFormatted}, ${endFormatted})}"></span>
  ```
- **NEVER hardcode a placeholder dash for an empty value.** Write `<span th:text="#{common.empty}"></span>`, NOT `<span>-</span>`.
- **NEVER hardcode a string in JavaScript.** JavaScript has no access to the message bundle. Pass every string in from Thymeleaf. Two patterns are approved. Use the one that matches the file.
  1. **Inline `<script>` in a template** — use Thymeleaf JavaScript inlining. Collect the strings into one `labels` object at the top of the script.
     ```html
     <script th:inline="javascript">
     const labels = {
         serviceRegion: /*[[#{usage.confirm.table.serviceRegion}]]*/ '',
         noChanges: /*[[#{usage.confirm.noChanges}]]*/ ''
     };
     </script>
     ```
     The `''` after the comment is the Thymeleaf inlining placeholder, not a fallback string. Thymeleaf replaces it at render time. Keep it empty.
  2. **An external `static/js/*.js` file** — the file never passes through Thymeleaf, so the template must hand it the strings through `data-*` attributes on a root element. Read them with `dataset` in the module.
     ```html
     <div id="draft-root" th:data-msg-success="#{draft.update.success}"
          th:data-msg-error="#{draft.update.error}"></div>
     ```
     ```javascript
     const messages = { success: root.dataset.msgSuccess, error: root.dataset.msgError };
     ```
     For a message with placeholders, pass the raw pattern in the attribute and substitute in JavaScript with `.replace('{0}', value)`. See `orders.export.modal.exportedBefore` in `admin/order/list.html`.
- **NEVER write a default string in a shared JavaScript module.** `const text = options.btnText || 'Confirm';` puts English in a file that Thymeleaf never sees. Require the caller to supply the text. Every caller has a template, and every template has the message bundle.
- **NEVER use `alert()`, `confirm()`, or `prompt()`.** They cannot be styled, and their text is easy to hardcode. Use `ConfirmModal` or the toast helper, and pass a message key through one of the two patterns above.
- **NEVER hardcode an absolute URL or a URL prefix in display text.** `th:text="'Example: https://programs.example.com/program/' + ${subscription.slug}"` hardcodes English, a host name, and a path. Put the host in `application.yml`, and put the sentence in a parameterized message.

### Adding a message key

1. Add the key to `messages.properties` in the section for its page.
2. Add the same key to `messages_fr_CA.properties` at the same position. The two files must stay key-for-key identical.
3. Name it `section.subsection.element` (for example, `dashboard.upload.button`). Reuse a `format.*` or a `common.*` key for a value that more than one page shows.
4. Write the value in ASD-STE100 Simplified Technical English, the same as all other prose in the repository.


## Never Concatenate

`+` in a template is almost always the wrong tool. Thymeleaf has a purpose-built construct for every case, and each one adds something `+` cannot: escaping, encoding, context-path resolution, or translator control over word order. Work down this ladder and stop at the first rule that fits.

**1. The result is text a person reads → a parameterized message.**

```html
<!-- WRONG: word order, spacing, and punctuation are frozen into the template -->
<span th:text="#{order.detail.heading} + ' ' + ${order.orderCode}"></span>
<!-- RIGHT -->
<span th:text="#{order.detail.heading(${order.orderCode})}"></span>
```

A translator can move `{0}`. A translator cannot move a `+` that lives in your HTML. This is the rule in the **No Hardcoded User-Facing Strings** section above, and it outranks every rule below it. Never reach for `|...|` to glue a message to a value.

**2. The result is a URL → `@{...}` with a parameter list.**

```html
<!-- WRONG: no encoding of the appended part -->
<a th:href="@{'/user/' + ${id}}">
<!-- RIGHT: names matching {placeholder} become path segments, the rest become query params -->
<a th:href="@{/user/{id}/orders(id=${id}, page=0, search=${search})}">
```

`@{...}` resolves the context path and URL-encodes every value. Concatenation does neither. This applies to `th:href`, `th:src`, and `th:action`.

Four things to know:
- **Null renders as `?x=`, not omitted.** Thymeleaf emits an empty parameter for a null value. Guard the caller instead when the parameter must disappear, or accept the empty parameter when the controller treats blank and absent alike. Never hand-build `'&x=' + ${value}` to get omission — that trades encoding for tidiness.
- **Path variables are encoded too.** `@{/files/{p}(p=${path})}` turns `a/b` into `a%2Fb`. To inject raw path segments, use preprocessing: `@{/files/__${path}__}`. Preprocessing runs before parsing, so use it only on trusted values.
- **A list expands to repeated parameters.** `@{/search(tag=${tags})}` gives `?tag=java&tag=web`.
- **A non-HTTP scheme is not an application URL.** Use literal substitution: `th:href="|mailto:${subscription.contactEmail}|"`.

Store an external URL template in `application.yml` with `{placeholder}` tokens, expose it as a model attribute, and use it as the `@{...}` base:

```yaml
myapp:
  customer-program-url: https://programs.example.com/program/{slug}
```
```html
<a th:href="@{${customerProgramUrl}(slug=${subscription.slug})}">Link</a>
```

Never build a URL from `#request.contextPath` — `#request` was removed in Thymeleaf 3.1, and `@{/...}` already resolves the context path.

**3. The result is a machine-readable identifier → literal substitution `|...|`.**

Element IDs, `name`, `for`, `data-bs-target` selectors, and map keys are not prose and not URLs. Use `|...|`.

```html
<!-- WRONG -->
<tr th:id="'billingPeriod-row-' + ${billingPeriod.id}">
<label th:for="'pbillingPeriod-' + ${product.id} + '-' + ${billingPeriod.billingPeriodId}">
<!-- RIGHT -->
<tr th:id="|billingPeriod-row-${billingPeriod.id}|">
<label th:for="|pbillingPeriod-${product.id}-${billingPeriod.billingPeriodId}|">
```

`|...|` in Thymeleaf 3.1 also accepts `#{...}` and `@{...}` inside it. Do not use it for either. A message belongs in rule 1 so the whole sentence stays translatable, and a URL belongs in rule 2 so the parameters stay encoded.

**4. The same composed value is needed more than once → `th:with`.**

Name it once, then reference the name. This keeps each use site short and makes a change land in one place.

```html
<main th:with="submittedSortParam=${#strings.isEmpty(currentSubmittedSort) ? null : currentSubmittedSort}">
    <a th:href="@{/admin/orders(ss=${submittedSortParam})}">…</a>
```

Assignments in one `th:with` evaluate in order, so a later name can use an earlier one. A name must never reference itself — `x=${x}` silently yields null.

**5. In JavaScript → `URL` and `URLSearchParams`, or DOM construction.**

```javascript
// WRONG: no encoding, and a repeated call appends a duplicate parameter
let url = baseUrl + '&size=' + size + '&search=' + encodeURIComponent(search);
// RIGHT: set() replaces, delete() removes, encoding is automatic
const url = new URL(baseUrl, window.location.origin);
url.searchParams.set('size', size);
if (search) { url.searchParams.set('search', search); } else { url.searchParams.delete('search'); }
```

Build markup with DOM calls and `.text()`, not with `+` on HTML strings. `.text()` escapes the value, so a product code or a customer name cannot inject markup:

```javascript
$('<th scope="col">').text(labels.serviceRegion)
```

Rule 1 still applies to every string in that markup: the label comes from the bundle, never from a literal.

### Where `+` is still correct

Inside a `${...}` expression, when the result is a Java-side value and not markup — for example a map key, `${quantities.get(product.itemCode + '_' + billingPeriod.id)}`. Prefer restructuring the data so the template does not need the key at all. When the key must be built in the template, `+` is the only tool available, and that is fine.

