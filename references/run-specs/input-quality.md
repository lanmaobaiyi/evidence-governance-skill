# Run spec: input quality

**Purpose:** verify that supplied records or policy files are safe to interpret.

**Inputs:** CSV, XLSX, JSON, DOCX, TXT, or Markdown; declared source role.

**Outputs:** accepted source inventory, normalized fields, warnings, and blocking errors.

**Checks:** file/container integrity, encoding, header location, duplicate/ambiguous aliases, required fields, revision/date, and source hash.

For Office Open XML containers (XLSX/DOCX), treat the file as an untrusted ZIP container: reject path traversal, encrypted documents, macros/VBA, and unsafe external or embedded content; enforce limits on entry count, decompressed size, individual XML size, and compression ratio. Surface external links, embedded objects, and comments as warnings or review items rather than silently importing them.

Unknown columns and fields may be retained, but must be reported as warnings. If aliases map to multiple canonical fields, pause for human confirmation. Never choose an ambiguous mapping by position or alias order.

**Failure codes:** `unsupported_format`, `invalid_container`, `required_field_missing`, `ambiguous_mapping`, `source_unidentified`.

**Validator:** no analysis starts while a blocking error remains unresolved.
