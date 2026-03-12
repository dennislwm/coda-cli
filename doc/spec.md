
# Coda CLI Specification
## Configuration
- The CLI reads the Coda API key from the `CODA_API_KEY` environment variable.
- The CLI reads the API key from a `config.json` file when present, overriding the environment variable.
- The CLI fails with a clear error message when no API key is configured.
- Error handling is standardized across modules including document_creator, pycoda, and template_importer.
## Document Commands
- The `list-docs` command lists all Coda documents accessible to the authenticated user and prints them to stdout.
- The `get-doc` command retrieves a single document by ID and prints its details to stdout.
- The `delete-doc` command deletes a Coda document by ID.
- The `whoami` command verifies the configured API key and prints the authenticated account details.
- A `whoami` or `verify-auth` command confirms the API key works.
## Error Handling Enhancements
- Introduced guardrails to prevent accidental deletions of important project files like requirements.json.
- Standardized error handling measures implemented in multiple modules for consistency and clarity.
## Section and Structure Commands
- The `list-sections` command lists all sections in a document given a document ID.
- The `list-tables` command lists all tables in a document given a document ID.
- The `list-columns` command lists all columns in a table given a document ID and table ID.
- The `list-rows` command lists all rows in a table given a document ID and table ID.
- The `get-row` command retrieves a single row by ID from a table given a document ID and table ID.
- The `upsert-row` command inserts or updates a row in a table given a document ID, table ID, and cell values.
- The `update-row` command updates an existing row in a table given a document ID, table ID, row ID, and cell values.
- The `delete-row` command deletes a row from a table given a document ID, table ID, and row ID.
- The `upsert-rows` command inserts or updates multiple rows in a table given a document ID, table ID, a list of row cell values, and optional key columns.
- The CLI now includes implementations for handling errors and edge cases during operations.
## Gaps Handling
- Gaps found in cross-references and verification steps will be stored in .plumb/gaps.json to streamline project management.
## Table Export
- The `export-table` command exports a table to CSV format given a document ID and table ID.
- The `export-table` command prints CSV output to stdout by default.
- The `export-table` command writes CSV output to a file when the `--output` option is provided.
- The `export-table` command includes column headers in the first row of the CSV output.
- The `export-table` command supports UTF-8 encoding for international characters.
- The `export-table` command handles special characters (commas, quotes, newlines) correctly in CSV output.
- The `export-table` command returns an error for invalid document or table IDs.
- The `export-table` command returns an error when it cannot write to the specified output file.
- The `export-table` command accepts a template name in place of a raw document ID for user-friendly access.
## Template Export
- The `export-template` command exports a Coda document structure as a YAML template file.
- The `export-template` command includes document sections, tables, columns, and metadata in the output.
- The `export-template` command preserves variable placeholders for reuse across documents.
- The `export-template` command produces output compatible with the `import-template` command.
- The `export-template` command returns a clear error when the document ID is invalid.

## Template Import and Document Creation
- The `import-template` command creates a new Coda document from a YAML template file.
- The `import-template` command substitutes variable placeholders in the template with provided values.
- The `import-template` command supports variable substitution in nested dictionary structures.
- The `import-template` command supports a dry-run mode that previews the document without creating it.
- The `import-template` command returns a user-friendly error when the template file is not found.
- The `import-template` command returns a user-friendly error when the template file is invalid.
- Fix JSON handling has been applied in document creation and section addition methods.
## Template Registry
- The `register-template` command stores a mapping from a template name to a Coda document ID.
- The `list-templates` command lists all registered template name-to-document-ID mappings.
- The `remove-template` command deletes a template mapping by name.
- The template registry persists mappings to a JSON file between sessions.
- The template registry recovers gracefully from a corrupted JSON file.
- The template registry rejects empty template names or empty document IDs.
- Template names can be used in place of document IDs in commands that accept a document ID.
- Commands that accept a document ID also accept a Coda browser URL, resolving it to a document ID automatically.
- New rules are added to require checks on the requirement count before running `plumb parse-spec`.
## JSON Utilities
- The `JsonFile` class reads and writes JSON data to and from the filesystem.
- The `JsonPlan` class manages structured plan data in JSON format.
