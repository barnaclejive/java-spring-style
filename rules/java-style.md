---
paths:
  - "src/main/java/**"
  - "src/test/java/**"
---

# Java Code Style

These rules are binding on every Java edit. The variable and converter-method naming rules live in `naming.md`. The test-specific conventions live in `testing.md`.

## Coding Conventions

- **Never use `var`.** Always use explicit types for all variable declarations.
- Use `final` on all parameters and variables.
- Use primitive `boolean` (not `Boolean`) for non-nullable boolean entity fields.
- Use Java records for DTOs, in the `dto` package of the owning domain.
- When possible, use streams instead of for-loops. Use functional programming (streams, optionals).
- Put a single blank line after method signatures. See *Blank line rules inside methods* for the full rules and for the accessor and field-assignment-constructor exceptions.
- **140-character line limit.** Keep each statement on a single line when the one-line form fits in 140 characters, even if the line is on the longer side. Split across lines only when the joined version exceeds 140 characters. Do NOT split a statement for aesthetics. This rule applies to every statement shape: assignments (if the whole statement fits, never put the RHS on its own line — `final List<Foo> rows = (List<Foo>) session.getAttribute("key");` stays on one line), short method calls (`redirectAttributes.addFlashAttribute("success", "Usage updated successfully. " + csvRows.size() + " records processed.");` — 133 chars including the indent — is one line, not two), short `throw` / `return` statements, field initializers, and more. When a line genuinely exceeds 140 characters, stack the parameters vertically, one per line. **Never break a ternary between its `?` arm and its `:` arm.** A ternary is one thought, and a line break between the two arms hides which one belongs to which condition. Keep `condition ? a : b` on one line. When the whole statement does not fit, break before the `?` and keep `? a : b` together on the continuation line:
  ```java
  form.setDiscountOverrideCode(subscriptionDetailDto.discountOverride() != null
          ? subscriptionDetailDto.discountOverride().code() : null);
  ```
  When even that form does not fit in 140 characters, extract a local variable or a private helper method. Do not stack the arms on separate lines. The same rule applies to a ternary inside a lambda body: `word -> word.isEmpty() ? word : capitalize(word)` stays on one line, and a helper method absorbs the arm that makes it too long. **Exception: `record` declarations.** Always format each record component on its own line, even when the joined form fits in 140 characters. The opening `(` stays on the declaration line. Each component is indented 8 spaces and ends with a comma (no trailing comma on the last component). The closing `)` sits on its own line at column 0, followed by `{}` on the same line. This rule applies to every record declaration, whatever the package. It covers the top-level records in `common.dto`, `common.dto.projection`, `admin.*.dto`, and `customer.dto`, the records in any other package, and the nested records declared inside interfaces or classes. A record with an `implements` clause keeps that clause on the closing line, after the `)`. For a nested record, indent the components 8 spaces from the record declaration, and put the closing `)` at the indent of the declaration. Example:
  ```java
  public record IdCountProjection(
          Long id,
          long count
  ) {}
  ```
  **Exception: getters and setters.** Accessor methods (`getX()`, `isX()`, `setX(...)`) on POJO form/DTO classes always use the standard Java multi-line format with the body on its own line, even when the joined one-line form fits in 140 characters. The opening `{` stays on the signature line. The body sits on its own indented line. The closing `}` is on its own line. Put the getter and the setter for a field together with no blank line between them. Put a single blank line between different field pairs. Do NOT inline a getter/setter body, not even for a trivial `return x;` or `this.x = x;` body. Example:
  ```java
  public String getName() {
      return name;
  }
  public void setName(final String name) {
      this.name = name;
  }

  public List<Long> getPaymentTermIds() {
      return paymentTermIds;
  }
  public void setPaymentTermIds(final List<Long> paymentTermIds) {
      this.paymentTermIds = paymentTermIds;
  }
  ```
- Store monetary values as `BigDecimal` with `@Column(precision = 19, scale = 2)` — for example, `5499.00` for $5,499.00.
- **No decorative section-divider comments.** Do not add comments like `// --- getters and setters ---`, `// === Constants ===`, or similar decorative separators between class members. These labels repeat what the class structure already shows. This rule is about decoration between members. It does not restrict the step comments inside a method body that *Comment style* permits.
- **Use `StringUtils.isBlank` / `StringUtils.isNotBlank` for string null/blank checks.** Never hand-write `x == null || x.isBlank()` or `x != null && !x.isBlank()`. Import `org.apache.commons.lang3.StringUtils` (commons-lang3 is on the classpath transitively via Spring Boot). The same rule applies to the empty-only variants: when the input is a `String` or `CharSequence`, use `StringUtils.isEmpty` / `StringUtils.isNotEmpty` instead of `x == null || x.isEmpty()` / `x != null && !x.isEmpty()`. Both helpers are null-safe and handle method-call expressions cleanly (for example, `StringUtils.isBlank(form.getName())` replaces `form.getName() == null || form.getName().isBlank()`). This rule applies only to strings. For `Collection`, `Map`, `MultipartFile`, and other types with their own `isEmpty()` method, keep the explicit `x == null || x.isEmpty()` check (or use `CollectionUtils.isEmpty` / `MapUtils.isEmpty` if preferred).
- **Logger declarations use `getClass()`, not `ClassName.class`.** Always declare the SLF4J logger as `private final Logger log = LoggerFactory.getLogger(getClass());`. Never use `private static final Logger log = LoggerFactory.getLogger(ClassName.class);`. The `getClass()` form is copy-paste safe (there is no class name to get wrong when you copy the line between files). It is rename-safe (there is no class reference to update). It also keeps the declaration identical in every file, so the convention is easy to review. The per-instance cost is irrelevant for Spring singletons (`@Controller`, `@Service`, `@ControllerAdvice`, `@Component`, `@Repository`), which are the only places where this codebase declares loggers.
- **`log.error` is reserved for truly unexpected runtime failures — never for expected, handled scenarios.** The bar is this question: does a developer want a page or an alert to investigate this event? If the answer is no, the event does not belong at ERROR. The error log is a signal that something is broken and that a code change can be necessary. Routine user-input failures in that log destroy the signal. **Do log at ERROR**: a `catch (final Exception e)` catch-all block (the code did not anticipate the exception by name — by definition unexpected), a 5xx server-error branch in `GlobalExceptionHandler`, infrastructure failures (a lost DB connection, an unreachable downstream service), and programming errors that escape into runtime (illegal state assertions). **Do NOT log at ERROR**: a user uploaded a malformed or corrupt CSV (`CsvReadException`), validation failures (missing required fields, bad date formats, unknown serviceRegion codes), business-rule rejections caught by name (`BillingPeriodValidationException`, an `IllegalArgumentException` thrown from a service to signal a 400-class problem), an `Optional.empty()` from a not-found lookup, or any branch that ends in an error flash message and a redirect. The user already gets feedback through the UI. A developer who reads the error log later can do nothing about the bad CSV of a customer. **Never use `log.warn`** in this codebase — there is no middle ground. Either the event is a real unexpected failure (ERROR), or it is not loggable at all. If you write `log.error` next to a localized user-facing error message in the same code path, delete the log line. Practical test: after you remove the log line, will a developer ever miss it during the triage of a production incident? If you cannot construct a realistic incident where the log entry helps, the entry must not exist.
- **Pass nullable strings directly to `model.addAttribute`.** Never write `model.addAttribute("search", search != null ? search : "");` for an `@RequestParam(required = false) String`. Thymeleaf treats `null` and `""` identically in the contexts where these attributes are used: `${#strings.isEmpty(x)}` returns `true` for both. `th:value="${x}"` either omits the attribute (null) or renders `value=""` (""), and the two behave the same for `<input>` rendering. And `@{...(param=${x})}` renders the same URL for both: Thymeleaf writes `param=` for a null value, exactly as it does for an empty string. A null query parameter is **not** omitted. Never pass `null` in the belief that the parameter will disappear, and never hand-build a query string to get that omission — see **Never Concatenate** in `frontend-style.md`. Pass the raw nullable value: `model.addAttribute("search", search);`. The same rule applies to other passthrough nullable strings, like sort codes and filter values. **Exceptions** — keep an explicit non-null fallback when a consumer of the value is not null-safe: `Collectors.toMap` (NPE on null values), string concatenation in Java (`"foo" + nullVal` produces `"foonull"`), or an equality check like `${navItem.code() == filterCode}` where both sides can be null and a `null == null → true` match is wrong. When in doubt, trace the value through every consumer before you simplify.
- **No repeated magic string literals.** When the same hardcoded string occurs in more than one place, extract it to a single source of truth. The compiler cannot catch a typo in a repeated string literal, and a renamed value silently goes out of sync across files. The correct replacement depends on the kind of literal:
  - **Closed sets of named values** (`"new"` / `"updated"` / `"unchanged"`, `"DRAFT"` / `"SUBMITTED"`, `"asc"` / `"desc"`, and similar sets) → use a Java `enum` in the applicable `dto` package. Reference the enum constant in Java (`CatalogItemStatus.NEW`) and in Thymeleaf via `T(fully.qualified.EnumClass).CONSTANT` (for example, `${row.status == T(com.example.catalogitem.dto.CatalogItemStatus).UPDATED}`).
  - **Single repeated string** (a column name, a session-attribute key, a CSV header, a fixed parameter name) → extract it to a `private static final String CONSTANT_NAME = "...";` at the top of the class that owns the value. If multiple classes use it, extract it to a shared constants holder.
  - **User-facing text** → message keys in `messages.properties` (already required — see the i18n rules in `frontend-style.md`).
  A literal is "repeated" if it occurs at two or more places (an assignment site + a comparison site counts as two, and multiple comparison sites count). A literal that genuinely occurs only once and represents a one-off, never-compared value can stay inline. **The bar is the occurrence count, not the domain importance.** `"updated"` repeated five times is a magic string, even if it feels self-documenting. `"GET"` passed once to an HTTP client is not. When you introduce a new domain concept with a fixed value set (anything with a name like `*Status`, `*Type`, `*Mode`, `*Kind`, `*State`), create an enum on day one. Do not start with strings and refactor later.

## Java Formatting & Style

Beyond the substance rules in *Coding Conventions*, the codebase follows a consistent visual layout. Match these patterns when you write or change code, so new code reads like the surrounding code.

### Class member ordering

Always declare members in this fixed order, with a single blank line between each non-empty group:

1. **Logger** (if the class logs) — `private final Logger log = LoggerFactory.getLogger(getClass());` as the very first field.
2. **Static final constants** — grouped together with no blank lines between siblings.
3. **Instance fields** — all `private final`, grouped together with no blank lines between siblings. Constructor-injected dependencies first, then plain configuration values (for example, `@Value`-bound primitives) at the end of the group.
4. **Constructor** — a single constructor with constructor injection (no `@Autowired` annotation is necessary on the sole constructor).
5. **Public methods** — `@Override` interface implementations first, in the same order as the interface declares them. Then the non-interface public methods.
6. **Private helper methods** — directly below the public method that calls them. See *Private helper placement*.
7. **Shared helpers and shared converter methods** — in one group at the bottom of the class. See *Private helper placement*.

For enums (such as the `*Sort` enums), the order is: enum constants → static final lookup map (for example, `BY_CODE`) → instance fields → constructor → instance accessors → static factory methods (`fromCode`, `resolve`).

### Private helper placement

Keep a private helper near the method that calls it. A reader who studies a public method must find the helpers of that method without a search. Do not collect all private methods at the bottom of the file. The bottom of a large class can be many hundreds of lines from the call site.

These rules give one position for each helper:

- **One caller** — put the helper directly after the public method that calls it. When one public method calls several helpers, put the helpers in first-call order.
- **Nested helper** — when a helper calls a second helper, put the second helper directly after the first one. Each method comes before the methods that it calls. This layout is a stepdown from the public API down to the details.
- **Several callers that sit close together** — put the helper directly after the last caller. Then all callers stay above the helper. The count of callers does not matter. Four callers in one block still keep the helper next to that block.
- **Callers that sit far apart** — put the helper in the shared group at the bottom. A helper of this kind belongs to the whole class, not to one public method.
- **Converter methods** (named `{Source}To{Target}`, see `naming.md`) — a converter that serves one public method follows the rules above. A converter that serves the whole class goes in the shared group at the bottom. When a class holds three or more converters, keep them together as one mapping layer at the bottom. A reader compares near-identical converters side by side. That comparison is worth more than the short distance to one caller.
- The stepdown creates distance of its own. When a public method calls a helper, and that helper calls three more helpers, the second helper of the public method starts about 100 lines down. This distance is correct. Do not flatten a good stepdown to close a gap.
- A helper group between two public methods must belong to the public method directly above it. Never put the helper of a later public method before that method.
- Never put a private helper above the first public method of the class.

The distance test settles an unclear case. When the helper and its caller do not fit on one screen together, the helper is too far away. Move it up, or move it to the shared group.

Example of the stepdown layout:

```java
@Override
public ParseResult parseAndPreviewCsv(final InputStream csvStream) {
    // calls validateHeaders, then parseRow
}

private List<LocalizedCsvMessage> validateHeaders(final Map<String, Integer> headerMap) {
}

private CatalogItemCsvRow parseRow(final String[] line, final Map<String, Integer> headerMap, final String sku) {
    // calls splitDelimited
}

private List<String> splitDelimited(final String value) {
}

@Override
public void commitUpload(final List<CatalogItemCsvRow> catalogItemCsvRows) {
    // the next public method starts the next stepdown
}
```

### Blank line rules inside methods

A method body must read as a short sequence of paragraphs. Each paragraph is one step of the work. Blank lines mark the paragraph breaks. This is the highest-value formatting rule in this codebase, and it is the rule that an audit gets wrong most often. **When a case is not clear, add the blank line.** Generous vertical spacing is the preference. A dense, unbroken block of statements is not.

The canonical reference method is `AdminCatalogItemController.commit`. It shows the guard, the padded `try` / `catch`, and the separated `return` in one place.

#### After the opening brace

- **Default**: one blank line after the opening `{` of a method, before the first statement of the body. Apply it to every method that contains logic.
- **Exceptions** (no blank line after `{`) — bodies that hold no logic to separate:
  - **Getters and setters** on POJO form, DTO, and entity classes. The body sits directly under the signature (per the rule in *Coding Conventions*).
  - **Constructors whose body only assigns the parameters to fields.** This covers every dependency-injection constructor on a `@Controller`, `@Service`, or `@Component`, and every exception constructor that only calls `super(...)`. The body is boilerplate with no steps in it, so a blank line adds nothing. Reference implementations: `AdminOrderController`, `AdminSubscriptionController`, `UsageServiceImpl`, `CsvReadException`.
  - **One-statement delegate methods** that only forward to another overload, for example `public static Sort resolve(final String code, final OrdersSort defaultSort) { return resolve(code, defaultSort.getSort()); }`.

  ```java
  public AdminOrderController(final SubscriptionService subscriptionService,
                              final ExportService exportService,
                              final MessageSource messageSource,
                              @Value("${myapp.admin-orders-page-size}") final int adminOrdersPageSize) {
      this.subscriptionService = subscriptionService;
      this.exportService = exportService;
      this.messageSource = messageSource;
      this.adminOrdersPageSize = adminOrdersPageSize;
  }
  ```

#### Nested blocks: `if`, `else`, `for`, `while`, `try`, and block lambdas

A nested block gets the same test as a method body. Ask whether the block does work that has steps, or one handling action.

- **A block that does substantive work gets a blank line after its `{`.** A block is substantive when it declares a local variable, holds a nested block, or moves through more than one step.
- **A short handling block stays tight.** Keep the statements directly under the `{` for an early-return guard, a branch that sets one value, or a block that only adds a flash message.

```java
// Substantive: the block declares locals and builds the form.
if (!model.containsAttribute("subscriptionEditForm")) {

    final SubscriptionEditForm form = new SubscriptionEditForm();
    form.setName(subscriptionDetailDto.name());
    ...
}

// Substantive: the loop body holds a nested block.
for (final CsvCatalogItemRow.DateRange range : incomingRanges) {

    if (!existingByRange.containsKey(range)) {

        validateBillingPeriodDates(range.startDate(), range.endDate());

        final BillingPeriod billingPeriod = new BillingPeriod();
        billingPeriod.setStartDate(range.startDate());
        subscription.getBillingPeriods().add(billingPeriod);
    }
}

// Short handling block: one action, no local, stays tight.
if (detail.isEmpty()) {
    return Views.REDIRECT_ADMIN;
}
```

#### `try` / `catch` blocks

A `try` / `catch` is padded on both sides of the `} catch` boundary. The success path and the failure path must be easy to tell apart at a glance.

- Put a blank line after `try {` when the `try` body holds more than one statement. The body is then the success path of the method, and that path has steps.
- Put a blank line before each `} catch (...)`, at the end of a padded `try` body.
- Put a blank line after each `} catch (...) {`.
- **Exception**: keep a block tight when every statement in it fits on one line. A one-statement `try` that only assigns a value, and the `catch` that returns one error result, need no padding. Reference implementations: `CsvServiceImpl.parseAndValidate`, `UsageServiceImpl.parseAndPreviewCsv`, and `CsvParsingUtils.readAllRows` all keep the compact form:
  ```java
  final List<String[]> allRows;
  try {
      allRows = CsvParsingUtils.readAllRows(csvStream);
  } catch (final CsvReadException e) {
      return CsvValidationResult.failure(List.of(CsvError.of(0, COLUMN_FILE, "csv.error.fileReadFailed")));
  }
  ```
- Put a blank line after the closing `}` of the last `catch`, before the statement that follows (almost always the `return`).

```java
try {

    catalogItemService.commitUpload(catalogItemCsvRows);
    session.removeAttribute(SESSION_CATALOG_ITEM_UPLOAD_CSV_ROWS);
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
```

#### Between statements

These rules give the paragraph breaks inside the body. They are listed in priority order. An earlier rule wins over a later one.

1. **Statements that form one step stay together.** A run of same-shape one-line statements is one paragraph: a block of `model.addAttribute(...)` calls, a block of `form.setX(...)` calls, a block of `this.x = x` assignments, a local declaration and the `if` that tests the state it produced. Never break up such a run.
2. **A statement that spans more than one line is its own paragraph.** Put a blank line above it and below it. A multi-line statement is already hard to scan, and a neighboring statement directly above or below it hides where it starts and where it ends. This covers a stream pipeline, a wrapped method call, a multi-line ternary, and a wrapped assignment. **Exception**: when the multi-line statement and the one-line statement directly above it produce one named result together, keep them in one paragraph (for example, `final List<Long> billingPeriodIds = ...;` directly above the stream that maps those ids to DTOs).
3. **Put a blank line after the closing `}` of a guard block.** The guard belongs to the statement that produced the value it tests, not to the work that follows it. Do NOT put a blank line above the guard when the statement above is one line.
4. **Put a blank line between consecutive `if` blocks** that test independent conditions.
5. **Put a blank line between the phases of the method.** The usual phases are (a) input and argument resolution, (b) data lookup or aggregation, (c) the main computation, and (d) result construction or model attribute population.
6. **The final `return` of the method gets its own paragraph.** Put a blank line above it. This applies to a `return` after a block of `model.addAttribute(...)` calls, after a `try` / `catch`, after an `if` / `else`, and after a stream pipeline. **Exception**: a `return` that only hands back what the one or two one-line statements directly above it produced can stay attached to them (for example, `final DiscountOverride saved = repository.save(discountOverride); return discountOverrideToDiscountOverrideDto(saved);`). A guard `return` inside an `if` block is not covered by this rule. It follows *Nested blocks*.
7. **Between methods**: exactly one blank line between consecutive methods.

Worked example. Every blank line in it comes from one of the rules above. The trailing `//` markers annotate this guide only. Do not copy them into code:

```java
@GetMapping("/programs")
public String listPrograms(@AuthenticatedUser final User user,
                           @RequestParam(value = "page", defaultValue = "0") final int page,
                           @RequestParam(value = "size", required = false) final Integer size,
                           @RequestParam(value = "s", required = false) final String sortCode,
                           final Model model) {

    final SubscriptionSort subscriptionSort = SubscriptionSort.fromCode(sortCode);      // phase (a): resolve the input
    final Sort resolvedSort = SubscriptionSort.resolve(sortCode, SubscriptionSort.NAME_ASC);
    final int resolvedSize = size != null ? size : customerProgramPageSize;

    final Page<SubscriptionSummaryDto> programsPage =                                   // phase (b): multi-line, own paragraph
            subscriptionService.listAllAvailablePage(PageRequest.of(page, resolvedSize, resolvedSort));

    model.addAttribute("programsPage", programsPage);                                   // phase (d): one run, one paragraph
    model.addAttribute("currentSort", subscriptionSort == null ? null : subscriptionSort.getCode());
    model.addAttribute("defaultPageSize", customerProgramPageSize);
    model.addAttribute("user", user);

    return "customer/programs";                                                         // the return gets its own paragraph
}
```

A second worked example, with a guard and a shared helper call:

```java
private String renderEditPage(final String code,
                              final Model model,
                              final User user,
                              final SubscriptionDetailDto subscriptionDetailDto) {

    model.addAttribute("subscription", subscriptionDetailDto);

    final List<PaymentTermEditDto> editList = subscriptionService.buildPaymentTermEditList(subscriptionDetailDto.id());
    model.addAttribute("paymentTermEditList", editList);

    final boolean hasUsed = editList.stream().anyMatch(PaymentTermEditDto::usedInOrders);
    model.addAttribute("hasUsedPaymentTerms", hasUsed);

    model.addAttribute("serviceRegionEditList", subscriptionService.buildServiceRegionEditList(subscriptionDetailDto.id()));
    model.addAttribute("discountOverrides", discountOverrideService.findAll());

    addBillingPeriodAndProductAttributes(model, subscriptionDetailDto);

    model.addAttribute("user", user);

    return VIEW_EDIT;
}
```

A local declaration and the single statement that consumes it form one paragraph (`editList` + its `addAttribute`, `hasUsed` + its `addAttribute`). A call of a different shape (`addBillingPeriodAndProductAttributes`) is its own paragraph. The plain `addAttribute` calls that need no local stay in one run.

#### Vertical spacing checklist

Run this list over every method that you write or change:

1. Does the body contain logic? Add a blank line after the `{`. Is the body only field assignments or an accessor? Remove it.
2. Is there a `try` with more than one statement in its body? Pad after `try {`, before `} catch`, and after `} catch (...) {`. Keep a one-statement `try` / `catch` pair tight.
3. Does a guard `if` block end the entry phase? Add a blank line after its closing `}`.
4. Does a statement span more than one line? Give it a blank line above and below, unless it completes the one-line statement directly above it.
5. Does the method end in a `return`? Add a blank line above it, unless the return only hands back what the line above produced.
6. Is any run of more than about five statements unbroken? Find the phase boundary and break it.

### Parameter and argument formatting

When a single-line method/constructor signature or call exceeds 140 chars, break it across lines with one of these two patterns. Pick by construct, not by aesthetics:

- **Method/constructor declarations in implementations and controllers**: align the continuation parameters under the first parameter (directly after the opening `(`). The first parameter stays on the signature line. Each annotated parameter (`@Value`, `@RequestParam`, `@PathVariable`, `@AuthenticatedUser`, `@Valid @ModelAttribute`) is its own logical unit and goes on its own line.
  ```java
  public AdminUsageController(final UsageService usageService,
                                  final ServiceRegionService serviceRegionService,
                                  final MessageSource messageSource,
                                  @Value("${myapp.admin-usage-page-size}") final int adminUsagePageSize) {
  ```
- **Interface method declarations**: prefer one parameter per line with an **8-space continuation indent** (not aligned to the first param). This keeps the API surface readable when the method names are long, and it gives a stable left edge.
  ```java
  void updateDetails(Long id,
          String name,
          String slug,
          LocalDateTime startDateTime,
          LocalDateTime endDateTime,
          ...);
  ```
- **Method call argument lists** that overflow: break after the opening `(`, use an **8-space continuation indent**, and put each argument on its own line. Do not align under the opening paren — the call site is too narrow horizontally.
  ```java
  final Page<OrderSummaryDto> submittedOrdersPage = exportService.getSubmittedOrderSummariesPage(
          subscriptionSummaryDto.id(),
          PageRequest.of(submittedPage, submittedResolvedSize, submittedResolvedSort),
          submittedSearch);
  ```
- **Stream / fluent chains**: put each `.foo(...)` on its own line with an 8-space continuation indent. Inline a chain only when the entire chain fits in 140 chars.

### `final` on interface vs implementation parameters

- **Interface method declarations**: do NOT add `final` to the parameters. The interface is only a contract. `final` is meaningless there and adds noise.
- **Implementation methods, constructors, lambdas, locals, fields**: always `final` (per *Coding Conventions*).

### Comment style

A comment inside a method body can do any of these three jobs:

1. **Explain why** the code makes a non-obvious choice. A constraint, a business rule, or a trap that the code alone cannot show.
2. **Summarize a dense line or chain.** Long stream pipelines, nested collectors, and multi-clause conditions are slow to read. One short line above them gives the reader the gist before the details.
3. **Mark a logical step.** A longer method often moves through several steps. A short comment above each step breaks up the method and shows the shape of the work.

Jobs 2 and 3 are wanted, not tolerated. Do not delete a step comment or a summary comment because the code below it "says the same thing". The comment is faster to read than the code, and that is the point.

Keep comments honest and cheap:

- Do not comment a line that any reader understands at a glance. A plain assignment or a well-named single call needs no comment.
- Keep the comment to one line where possible. Describe the step, not each statement in it.
- Update the comment when the code below it changes. A stale comment is worse than no comment.
- Prefer a better name over a comment when a rename can carry the meaning.

Mechanics:

- Use `//` line comments inside method bodies and above class fields. Put the comment on the line(s) directly above the code that it describes.
- Trailing inline comments are acceptable only for very short clarifications at the end of a single line (for example, `if (requestedCodes.contains(paymentTermCode)) return false; // keep — the term is still selected`).
- Reserve `/** ... */` Javadoc for class-level documentation on infrastructure classes whose role is not obvious from the name and code (for example, environment-specific shims like `StubSecurityContextFilter`, whose Javadoc says "the JWT auth replaces this in production"). Do NOT write Javadoc on ordinary services, controllers, or DTO records.
- No method-level Javadoc on application code. The method name + parameter names + return type must be self-documenting. If they are not, rename them.

Example of a step comment and a summary comment that the rules above want you to keep:

```java
// Get the payment term codes that orders use. The update must not remove these codes.
final Set<String> usedCodes = customerOrderRepository.findDistinctPaymentTermCodesBySubscriptionId(id);

// Build a map of the existing associations by payment term code.
final Map<String, SubscriptionPaymentTerm> existingSubscriptionPaymentTermMap =
        subscription.getPaymentTermAssociations().stream()
        .collect(Collectors.toMap(
                subscriptionPaymentTerm -> subscriptionPaymentTerm.getPaymentTerm().getCode(),
                subscriptionPaymentTerm -> subscriptionPaymentTerm));
```

### `StringUtils` vs `CollectionUtils` vs plain `.isEmpty()`

The choice depends on whether the value can be null at the call site:

- **Strings** (any `String` / `CharSequence`, from any source): always use `StringUtils.isBlank` / `StringUtils.isNotBlank` from `org.apache.commons.lang3`. This rule applies whether the string came from a request param, a DTO field, a session attribute, or a local variable. The helpers are null-safe and cheap, and their use everywhere removes a class of `NullPointerException` bugs by construction. (Per the existing *Coding Conventions* rule.)
- **Collections from outside the method** — request params, session attributes, form-bound `List<T>` fields, anything that arrived as input — use `CollectionUtils.isEmpty` from `org.apache.commons.collections4`. These are the boundary points where `null` is realistically possible.
- **Collections built or returned inside the same code path** — a locally constructed `List`/`Map`/`Set`, the result of a stream pipeline, the result of a repository `find...` method, the contents of an `Optional` — use plain `.isEmpty()`. These have a non-null contract, so a null-safe wrapper adds noise and no safety.
- For `MultipartFile`, use `file.isEmpty()` after a non-null check (or a `CsvUploadValidator.validate` call, which contains both checks). `CollectionUtils.isEmpty` does not work on `MultipartFile`.
