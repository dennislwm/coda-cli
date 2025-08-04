Title: codaio documentation — codaio documentation

URL Source: https://codaio.readthedocs.io/en/latest/index.html

Markdown Content:
[codaio](https://codaio.readthedocs.io/en/latest/index.html#)

Python wrapper for [coda.io](https://coda.io/developers/apis/v1beta1) API

Project home: [https://github.com/blasterai/codaio](https://github.com/blasterai/codaio)

_class_`codaio.``Coda`(_api\_key: str_, _href: str = 'https://coda.io/apis/v1beta1'_)[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda "Permalink to this definition")
Raw API client. It is used in codaio objects like Document to access the raw API endpoints. Can also be used by itself to access Raw API.

`account`() → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.account "Permalink to this definition")
At this time, the API exposes some limited information about your account. However, /whoami is a good endpoint to hit to verify that you’re hitting the API correctly and that your token is working as expected.

Docs: [https://coda.io/developers/apis/v1beta1#tag/Account](https://coda.io/developers/apis/v1beta1#tag/Account)

`create_doc`(_title: str_, _source\_doc: Optional[str] = None_, _tz: Optional[str] = None_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.create_doc "Permalink to this definition")
Creates a new Coda doc, optionally copying an existing doc.

Docs: [https://coda.io/developers/apis/v1beta1#operation/createDoc](https://coda.io/developers/apis/v1beta1#operation/createDoc)

Parameters
*   **title** – Title of the new doc.

*   **source_doc** – An optional doc ID from which to create a copy.

*   **tz** – The timezone to use for the newly created doc.

Returns`delete`(_endpoint: str_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.delete "Permalink to this definition")
Make a DELETE request to the API endpoint.

Parameters
**endpoint** – API endpoint to request

Returns`delete_doc`(_doc\_id: str_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.delete_doc "Permalink to this definition")
Deletes a doc.

Docs: [https://coda.io/developers/apis/v1beta1#operation/deleteDoc](https://coda.io/developers/apis/v1beta1#operation/deleteDoc)

Parameters
**doc_id** – ID of the doc. Example: “AbCDeFGH”

Returns`delete_row`(_doc\_id_, _table\_id\_or\_name: str_, _row\_id\_or\_name: str_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.delete_row "Permalink to this definition")
Deletes the specified row from the table. This endpoint will always return a 202, so long as the row exists and is accessible (and the update is structurally valid). Row deletions are generally processed within several seconds. When deleting using a name as opposed to an ID, an arbitrary row will be removed.

Docs: [https://coda.io/developers/apis/v1beta1#operation/deleteRow](https://coda.io/developers/apis/v1beta1#operation/deleteRow)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **table_id_or_name** – ID or name of the table. Names are discouraged because they’re easily prone to being changed by users.

If you’re using a name, be sure to URI-encode it. Example: “grid-pqRst-U”

Parameters
**row_id_or_name** – ID or name of the row. Names are discouraged because they’re easily prone to being changed by users.

If you’re using a name, be sure to URI-encode it. If there are multiple rows with the same value in the identifying column, an arbitrary one will be selected.

_classmethod_`from_environment`() → codaio.coda.Coda[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.from_environment "Permalink to this definition")
Initializes a Coda instance using API key store in environment variables under CODA_API_KEY

Returns`get`(_endpoint: str_, _data: Dict = None_, _limit=None_, _offset=None_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.get "Permalink to this definition")
Make a GET request to API endpoint.

Parameters
*   **endpoint** – API endpoint to request

*   **data** – dictionary of optional query params

*   **limit** – Maximum number of results to return in this query.

*   **offset** – An opaque token used to fetch the next page of results.

Returns`get_column`(_doc\_id: str_, _table\_id\_or\_name: str_, _column\_id\_or\_name: str_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.get_column "Permalink to this definition")
Returns details about a column in a table.

Docs: [https://coda.io/developers/apis/v1beta1#operation/getColumn](https://coda.io/developers/apis/v1beta1#operation/getColumn)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **table_id_or_name** – ID or name of the table. Names are discouraged because they’re easily prone to being changed by users. If you’re using a name, be sure to URI-encode it. Example: “grid-pqRst-U”

*   **column_id_or_name** – ID or name of the column. Names are discouraged because they’re easily prone to being changed by users. If you’re using a name, be sure to URI-encode it. Example: “c-tuVwxYz”

Returns`get_control`(_doc\_id: str_, _control\_id\_or\_name: str_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.get_control "Permalink to this definition")
Returns info on a control.

Docs: [https://coda.io/developers/apis/v1beta1#operation/getControl](https://coda.io/developers/apis/v1beta1#operation/getControl)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **control_id_or_name** – ID or name of the control. Names are discouraged because they’re easily prone to being changed by users.

If you’re using a name, be sure to URI-encode it. Example: “ctrl-cDefGhij”

`get_doc`(_doc\_id: str_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.get_doc "Permalink to this definition")
Returns metadata for the specified doc.

Docs: [https://coda.io/developers/apis/v1beta1#operation/getDoc](https://coda.io/developers/apis/v1beta1#operation/getDoc)

Parameters
**doc_id** – ID of the doc. Example: “AbCDeFGH”

Returns`get_folder`(_doc\_id: str_, _folder\_id\_or\_name: str_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.get_folder "Permalink to this definition")
Returns details about a folder.

Docs: [https://coda.io/developers/apis/v1beta1#operation/getFolder](https://coda.io/developers/apis/v1beta1#operation/getFolder)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **folder_id_or_name** – ID or name of the folder. Names are discouraged because they’re easily prone to being changed by users. If you’re using a name, be sure to URI-encode it. Example: “section-IjkLmnO”

Returns`get_formula`(_doc\_id: str_, _formula\_id\_or\_name: str_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.get_formula "Permalink to this definition")
Returns info on a formula.

Docs: [https://coda.io/developers/apis/v1beta1#operation/getFormula](https://coda.io/developers/apis/v1beta1#operation/getFormula)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **formula_id_or_name** – ID or name of the formula. Names are discouraged because they’re easily prone to being changed by users.

If you’re using a name, be sure to URI-encode it. Example: “f-fgHijkLm”

`get_row`(_doc\_id: str_, _table\_id\_or\_name: str_, _row\_id\_or\_name: str_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.get_row "Permalink to this definition")
Returns details about a row in a table.

Docs: [https://coda.io/developers/apis/v1beta1#operation/getRow](https://coda.io/developers/apis/v1beta1#operation/getRow)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **table_id_or_name** – ID or name of the table. Names are discouraged because they’re easily prone to being changed by users. If you’re using a name, be sure to URI-encode it. Example: “grid-pqRst-U”

*   **row_id_or_name** – ID or name of the row. Names are discouraged because they’re easily prone to being changed by users. If you’re using a name, be sure to URI-encode it. If there are multiple rows with the same value in the identifying column, an arbitrary one will be selected.

`get_section`(_doc\_id: str_, _section\_id\_or\_name: str_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.get_section "Permalink to this definition")
Returns details about a section.

Docs: [https://coda.io/developers/apis/v1beta1#operation/getSection](https://coda.io/developers/apis/v1beta1#operation/getSection)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **section_id_or_name** – ID or name of the section. Names are discouraged because they’re easily prone to being changed by users. If you’re using a name, be sure to URI-encode it. Example: “canvas-IjkLmnO”

Returns`get_table`(_doc\_id: str_, _table\_id\_or\_name: str_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.get_table "Permalink to this definition")
Returns details about a specific table.

Docs: [https://coda.io/developers/apis/v1beta1#operation/getTable](https://coda.io/developers/apis/v1beta1#operation/getTable)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **table_id_or_name** – ID or name of the table. Names are discouraged because they’re easily prone to being changed by users. If you’re using a name, be sure to URI-encode it. Example: “grid-pqRst-U”

Returns`get_view`(_doc\_id: str_, _view\_id\_or\_name: str_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.get_view "Permalink to this definition")
Returns details about a specific view.

Docs: [https://coda.io/developers/apis/v1beta1#operation/getView](https://coda.io/developers/apis/v1beta1#operation/getView)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **view_id_or_name** – ID or name of the view. Names are discouraged because they’re easily prone to being changed by users. If you’re using a name, be sure to URI-encode it. Example: “table-pqRst-U”

Returns`list_columns`(_doc\_id: str_, _table\_id\_or\_name: str_, _offset: Optional[int] = None_, _limit: Optional[int] = None_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.list_columns "Permalink to this definition")
Returns a list of columns in a table.

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **table_id_or_name** – ID or name of the table. Names are discouraged because they’re easily prone to being changed by users. If you’re using a name, be sure to URI-encode it. Example: “grid-pqRst-U”

*   **limit** – Maximum number of results to return in this query.

*   **offset** – An opaque token used to fetch the next page of results.

Returns`list_controls`(_doc\_id: str_, _offset: Optional[int] = None_, _limit: Optional[int] = None_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.list_controls "Permalink to this definition")
Controls provide a user-friendly way to input a value that can affect other parts of the doc. This API lets you list controls and get their current values.

Docs: [https://coda.io/developers/apis/v1beta1#tag/Controls](https://coda.io/developers/apis/v1beta1#tag/Controls)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **limit** – Maximum number of results to return in this query.

*   **offset** – An opaque token used to fetch the next page of results.

Returns`list_docs`(_is\_owner: bool = False_, _query: Optional[str] = None_, _source\_doc\_id: Optional[str] = None_, _limit: Optional[int] = None_, _offset: Optional[int] = None_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.list_docs "Permalink to this definition")
Returns a list of Coda docs accessible by the user. These are returned in the same order as on the docs page: reverse chronological by the latest event relevant to the user (last viewed, edited, or shared).

Docs: [https://coda.io/developers/apis/v1beta1#operation/listDocs](https://coda.io/developers/apis/v1beta1#operation/listDocs)

Parameters
*   **is_owner** – Show only docs owned by the user.

*   **query** – Search term used to filter down results.

*   **source_doc_id** – Show only docs copied from the specified doc ID.

*   **limit** – Maximum number of results to return in this query.

*   **offset** – An opaque token used to fetch the next page of results.

Returns`list_folders`(_doc\_id: str_, _offset: Optional[int] = None_, _limit: Optional[int] = None_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.list_folders "Permalink to this definition")
Returns a list of folders in a Coda doc.

Docs: [https://coda.io/developers/apis/v1beta1#operation/listFolders](https://coda.io/developers/apis/v1beta1#operation/listFolders)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **limit** – Maximum number of results to return in this query.

*   **offset** – An opaque token used to fetch the next page of results.

Returns`list_formulas`(_doc\_id: str_, _offset: Optional[int] = None_, _limit: Optional[int] = None_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.list_formulas "Permalink to this definition")
Returns a list of named formulas in a Coda doc.

Docs: [https://coda.io/developers/apis/v1beta1#operation/listFormulas](https://coda.io/developers/apis/v1beta1#operation/listFormulas)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **limit** – Maximum number of results to return in this query.

*   **offset** – An opaque token used to fetch the next page of results.

`list_rows`(_doc\_id: str_, _table\_id\_or\_name: str_, _query: Optional[str] = None_, _use\_column\_names: bool = False_, _limit: Optional[int] = None_, _offset: Optional[int] = None_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.list_rows "Permalink to this definition")
Returns a list of rows in a table.

Docs: [https://coda.io/developers/apis/v1beta1#tag/Rows](https://coda.io/developers/apis/v1beta1#tag/Rows)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **table_id_or_name** – ID or name of the table. Names are discouraged because they’re easily prone to being changed by users. If you’re using a name, be sure to URI-encode it. Example: “grid-pqRst-U”

*   **query** – Query used to filter returned rows, specified as <column_id_or_name>:<value>. If you’d like to use a column name instead of an ID, you must quote it (e.g., “My Column”:123). Also note that value is a JSON value; if you’d like to use a string, you must surround it in quotes (e.g., “groceries”).

*   **use_column_names** – Use column names instead of column IDs in the returned output. This is generally discouraged as it is fragile. If columns are renamed, code using original names may throw errors.

*   **limit** – Maximum number of results to return in this query.

*   **offset** – An opaque token used to fetch the next page of results.

`list_sections`(_doc\_id: str_, _offset: Optional[int] = None_, _limit: Optional[int] = None_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.list_sections "Permalink to this definition")
Returns a list of sections in a Coda doc.

Docs: [https://coda.io/developers/apis/v1beta1#operation/listSections](https://coda.io/developers/apis/v1beta1#operation/listSections)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **limit** – Maximum number of results to return in this query.

*   **offset** – An opaque token used to fetch the next page of results.

Returns`list_tables`(_doc\_id: str_, _offset: Optional[int] = None_, _limit: Optional[int] = None_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.list_tables "Permalink to this definition")
Returns a list of tables in a Coda doc.

Docs: [https://coda.io/developers/apis/v1beta1#operation/listTables](https://coda.io/developers/apis/v1beta1#operation/listTables)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **limit** – Maximum number of results to return in this query.

*   **offset** – An opaque token used to fetch the next page of results.

Returns`list_views`(_doc\_id: str_, _offset: Optional[int] = None_, _limit: Optional[int] = None_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.list_views "Permalink to this definition")
Returns a list of views in a Coda doc.

Docs: [https://coda.io/developers/apis/v1beta1#operation/listViews](https://coda.io/developers/apis/v1beta1#operation/listViews)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **limit** – Maximum number of results to return in this query.

*   **offset** – An opaque token used to fetch the next page of results.

Returns`post`(_endpoint: str_, _data: Dict_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.post "Permalink to this definition")
Make a POST request to the API endpoint.

Parameters
*   **endpoint** – API endpoint to request

*   **data** – data dict to be sent as body json

Returns`put`(_endpoint: str_, _data: Dict_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.put "Permalink to this definition")
Make a PUT request to the API endpoint.

Parameters
*   **endpoint** – API endpoint to request

*   **data** – data dict to be sent as body json

Returns`resolve_browser_link`(_url: str_, _degrade\_gracefully: bool = False_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.resolve_browser_link "Permalink to this definition")
Given a browser link to a Coda object, attempts to find it and return metadata that can be used to get more info on it. Returns a 400 if the URL does not appear to be a Coda URL or a 404 if the resource cannot be located with the current credentials.

Docs: [https://coda.io/developers/apis/v1beta1#operation/resolveBrowserLink](https://coda.io/developers/apis/v1beta1#operation/resolveBrowserLink)

Parameters
*   **url** – The browser link to try to resolve. Example: “[https://coda.io/d/_dAbCDeFGH/Launch-Status_sumnO](https://coda.io/d/_dAbCDeFGH/Launch-Status_sumnO)”

*   **degrade_gracefully** – By default, attempting to resolve the Coda URL of a deleted object will result in an error. If this flag is set, the next-available object, all the way up to the doc itself, will be resolved.

`update_row`(_doc\_id: str_, _table\_id\_or\_name: str_, _row\_id\_or\_name: str_, _data: Dict_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.update_row "Permalink to this definition")
Updates the specified row in the table. This endpoint will always return a 202, so long as the row exists and is accessible (and the update is structurally valid). Row updates are generally processed within several seconds. When updating using a name as opposed to an ID, an arbitrary row will be affected.

Docs: [https://coda.io/developers/apis/v1beta1#operation/updateRow](https://coda.io/developers/apis/v1beta1#operation/updateRow)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **table_id_or_name** – ID or name of the table. Names are discouraged because they’re easily prone to being changed by users.

If you’re using a name, be sure to URI-encode it. Example: “grid-pqRst-U”

Parameters
**row_id_or_name** – ID or name of the row. Names are discouraged because they’re easily prone to being changed by users.

If you’re using a name, be sure to URI-encode it. If there are multiple rows with the same value in the identifying column, an arbitrary one will be selected.

Parameters
**data** – Example: {“row”: {“cells”: [{“column”: “c-tuVwxYz”, “value”: “$12.34”}]}}

`upsert_row`(_doc\_id: str_, _table\_id\_or\_name: str_, _data: Dict_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Coda.upsert_row "Permalink to this definition")
Inserts rows into a table, optionally updating existing rows if any upsert key columns are provided. This endpoint will always return a 202, so long as the doc and table exist and are accessible (and the update is structurally valid). Row inserts/upserts are generally processed within several seconds. When upserting, if multiple rows match the specified key column(s), they will all be updated with the specified value.

Docs: [https://coda.io/developers/apis/v1beta1#operation/upsertRows](https://coda.io/developers/apis/v1beta1#operation/upsertRows)

Parameters
*   **doc_id** – ID of the doc. Example: “AbCDeFGH”

*   **table_id_or_name** – ID or name of the table. Names are discouraged because they’re easily prone to being changed by users.

If you’re using a name, be sure to URI-encode it. Example: “grid-pqRst-U”

Parameters
**data** – {“rows”: [{“cells”: [{“column”: “c-tuVwxYz”, “value”: “$12.34”}]}], “keyColumns”: [“c-bCdeFgh”]}

_class_`codaio.``Document`(_id: str_, _coda: Coda_)[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Document "Permalink to this definition")
Main class for interacting with coda.io API using codaio objects.

_classmethod_`from_environment`(_doc\_id: str_)[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Document.from_environment "Permalink to this definition")
Initializes a Document instance using API key stored in environment variables under CODA_API_KEY

Parameters
**doc_id** – ID of the doc. Example: “AbCDeFGH”

Returns`get_table`(_table\_id\_or\_name: str_) → codaio.coda.Table[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Document.get_table "Permalink to this definition")
Gets a Table object from table name or ID.

Parameters
**table_id_or_name** – ID or name of the table. Names are discouraged because they’re easily prone to being changed by users. If you’re using a name, be sure to URI-encode it. Example: “grid-pqRst-U”

Returns`list_sections`(_offset: Optional[int] = None_, _limit: Optional[int] = None_) → List[codaio.coda.Section][¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Document.list_sections "Permalink to this definition")
Returns a list of Section objects for each section in the document.

Parameters
*   **limit** – Maximum number of results to return in this query.

*   **offset** – An opaque token used to fetch the next page of results.

Returns`list_tables`(_offset: Optional[int] = None_, _limit: Optional[int] = None_) → List[codaio.coda.Table][¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Document.list_tables "Permalink to this definition")
Returns a list of Table objects for each table in the document.

Parameters
*   **limit** – Maximum number of results to return in this query.

*   **offset** – An opaque token used to fetch the next page of results.

Returns _class_`codaio.``Table`(_id: str_, _type: str_, _href: str_, _name: str_, _document: Document_, _display\_column: Dict = None_, _browser\_link: str = None_, _row\_count: int = None_, _sorts: List = []_, _layout: str = None_, _created\_at=None_, _updated\_at=None_, _columns\_storage: List[Column] = []_)[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Table "Permalink to this definition")`columns`(_offset: Optional[int] = None_, _limit: Optional[int] = None_) → List[codaio.coda.Column][¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Table.columns "Permalink to this definition")
Returns a list of Table columns. Columns are stored in self.columns_storage for faster access as they tend to change less frequently than rows.

Parameters
*   **limit** – Maximum number of results to return in this query.

*   **offset** – An opaque token used to fetch the next page of results.

Returns`delete_row`(_row: codaio.coda.Row_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Table.delete_row "Permalink to this definition")
Delete row.

Parameters
**row** – a Row object to delete.

`delete_row_by_id`(_row\_id: str_)[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Table.delete_row_by_id "Permalink to this definition")
Deletes row by id.

Parameters
**row_id** – ID of the row to delete.

`find_row_by_column_id_and_value`(_column\_id_, _value_) → List[codaio.coda.Row][¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Table.find_row_by_column_id_and_value "Permalink to this definition")
Fins rows by a value in column specified by id.

Parameters
*   **column_id** – ID of the column.

*   **value** – Search value.

Returns`find_row_by_column_name_and_value`(_column\_name: str_, _value: Any_) → List[codaio.coda.Row][¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Table.find_row_by_column_name_and_value "Permalink to this definition")
Finds rows by a value in column specified by name (discouraged).

Parameters
*   **column_name** – Name of the column.

*   **value** – Search value.

Returns`get_column_by_id`(_column\_id_) → codaio.coda.Column[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Table.get_column_by_id "Permalink to this definition")
Gets a Column by id.

Parameters
**column_id** – ID of the column. Example: “c-tuVwxYz”

Returns`get_column_by_name`(_column\_name_) → codaio.coda.Column[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Table.get_column_by_name "Permalink to this definition")
Gets a Column by id.

Parameters
**column_name** – Name of the column. Discouraged in case using column_id is possible. Example: “Column 1”

Returns`rows`(_offset: Optional[int] = None_, _limit: Optional[int] = None_) → List[codaio.coda.Row][¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Table.rows "Permalink to this definition")
Returns list of Table rows.

Parameters
*   **limit** – Maximum number of results to return in this query.

*   **offset** – An opaque token used to fetch the next page of results.

Returns`update_row`(_row: Union[str, codaio.coda.Row], cells: List[codaio.coda.Cell]_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Table.update_row "Permalink to this definition")
Updates row with values according to list in cells.

Parameters
*   **row** – a str ROW_ID or an instance of class Row

*   **cells** –

`upsert_row`(_cells: List[codaio.coda.Cell]_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Table.upsert_row "Permalink to this definition")
Upserts a row using Cell objects in list.

Parameters
**cells** – list of Cell objects.

`upsert_rows`(_list\_cells: List[List[codaio.coda.Cell]]_) → Dict[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Table.upsert_rows "Permalink to this definition")
Works similar to Table.upsert_row() but uses 1 POST request for multiple rows. Input is a list of lists of Cells.

Parameters
**list_cells** – list of lists of Cell objects, one list for each row.

_class_`codaio.``Column`(_id: str_, _type: str_, _href: str_, _document: Document_, _name: str_, _table: Table_, _display: bool = None_, _calculated: bool = False_)[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Column "Permalink to this definition")_class_`codaio.``Row`(_id: str_, _type: str_, _href: str_, _document: Document_, _name: str_, _created\_at_, _index: int_, _updated\_at_, _values_, _table: Table_, _browser\_link: str = None_)[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Row "Permalink to this definition")`delete`()[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Row.delete "Permalink to this definition")
Delete row.

Returns _class_`codaio.``Cell`(_column: Column_, _value\_storage: Any_, _row: Row = None_)[¶](https://codaio.readthedocs.io/en/latest/index.html#codaio.Cell "Permalink to this definition")