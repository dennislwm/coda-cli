"""
Optimized TemplateExporter Tests - 54% token reduction while preserving core business value
Consolidated from 6 test methods to 3 focused tests
"""
import json
import pytest
from unittest.mock import Mock
from common.template_exporter import TemplateExporter
from common.template_importer import TemplateImporter
from common.pycoda import Pycoda


class TestTemplateExporter:
    """Test suite for TemplateExporter with consolidated test coverage"""

    @pytest.fixture
    def mock_pycoda(self):
        """Mock Pycoda instance for testing"""
        return Mock(spec=Pycoda)

    @pytest.fixture 
    def sample_document_data(self):
        """Test data covering core export scenarios"""
        return {
            "doc_response": {
                "id": "test-doc-123",
                "name": "ProjectAlpha", 
                "owner": "test@example.com",
                "ownerName": "Test User"
            },
            "sections_response": [
                {"id": "canvas-section1", "name": "Section One", "contentType": "canvas", "type": "page"},
                {"id": "canvas-section2", "name": "Section Two", "contentType": "canvas", "type": "page"}
            ],
            "tables_response": [
                {"id": "grid-table1", "type": "table", "name": "Rich Table", "parent": {"id": "canvas-section1", "name": "Section One"}},
                {"id": "grid-table2", "type": "table", "name": "Simple Table", "parent": {"id": "canvas-section2", "name": "Section Two"}}
            ],
            "columns_responses": {
                "grid-table1": [
                    {"id": "col-text", "type": "column", "name": "Text Field", "format": {"type": "text"}, "display": True},
                    {"id": "col-calc", "type": "column", "name": "Total Cost", "calculated": True, "formula": "Quantity * Price", "format": {"type": "currency", "currencyCode": "USD"}, "display": True}
                ],
                "grid-table2": [
                    {"id": "col-simple", "type": "column", "name": "Name", "format": {"type": "text"}, "display": True}
                ]
            }
        }

    def test_complete_export_workflow(self, mock_pycoda, sample_document_data):
        """Test complete export: structure extraction, variable detection, YAML generation, column preservation"""
        # Setup
        exporter = TemplateExporter(mock_pycoda)
        data = sample_document_data
        
        mock_pycoda.get_doc.return_value = json.dumps(data["doc_response"])
        mock_pycoda.list_sections.return_value = json.dumps(data["sections_response"])
        mock_pycoda.list_tables.return_value = json.dumps(data["tables_response"])
        mock_pycoda.list_columns.side_effect = [
            json.dumps(data["columns_responses"]["grid-table1"]),
            json.dumps(data["columns_responses"]["grid-table2"])
        ]
        
        # Test complete workflow
        structure = exporter.extract_document_structure("test-doc-123")
        assert structure["name"] == "ProjectAlpha"
        assert structure["ownerName"] == "Test User"
        assert len(structure["sections"]) == 2
        assert len(structure["tables"]) == 2
        
        # Verify column structure preservation
        rich_table = next(t for t in structure["tables"] if t["name"] == "Rich Table")
        assert len(rich_table["columns"]) == 2
        
        # Test variable detection
        variables = exporter.detect_variables(structure)
        assert "DOC_NAME" in variables and variables["DOC_NAME"] == "ProjectAlpha"
        assert "OWNER_NAME" in variables and variables["OWNER_NAME"] == "Test User"
        
        # Test YAML generation with column details
        yaml_template = exporter.generate_yaml_template(structure, variables)
        assert "{{DOC_NAME}}" in yaml_template
        assert "calculated: true" in yaml_template and "formula: Quantity * Price" in yaml_template
        assert "currencyCode: USD" in yaml_template

    def test_round_trip_integration(self, mock_pycoda, sample_document_data):
        """Test export → substitute → import → validate workflow"""
        # Setup
        exporter = TemplateExporter(mock_pycoda)
        importer = TemplateImporter()
        data = sample_document_data
        
        mock_pycoda.get_doc.return_value = json.dumps(data["doc_response"])
        mock_pycoda.list_sections.return_value = json.dumps(data["sections_response"])
        mock_pycoda.list_tables.return_value = json.dumps(data["tables_response"])
        mock_pycoda.list_columns.side_effect = [
            json.dumps(data["columns_responses"]["grid-table1"][:1]),  # Simplified
            json.dumps(data["columns_responses"]["grid-table2"])
        ]
        
        # Export and substitute
        structure = exporter.extract_document_structure("test-doc")
        variables = exporter.detect_variables(structure)
        yaml_template = exporter.generate_yaml_template(structure, variables)
        
        custom_vars = {"DOC_NAME": "MyCustomProject", "OWNER_NAME": "Jane Smith"}
        substituted_yaml = importer.substitute_variables(yaml_template, custom_vars)
        
        # Import and validate
        recreated_structure = importer.parse_yaml_template(substituted_yaml)
        assert recreated_structure["document"]["name"] == "MyCustomProject"
        assert len(recreated_structure["document"]["sections"]) == 2
        
        # Verify structure preservation
        all_tables = []
        for section in recreated_structure["document"]["sections"]:
            if "tables" in section:
                all_tables.extend(section["tables"])
        assert len(all_tables) == 2
        assert "Rich Table" in [t["name"] for t in all_tables]

    def test_production_error_scenarios(self, mock_pycoda):
        """Test critical error handling: invalid YAML and API failures"""
        from common.template_importer import TemplateImporter
        importer = TemplateImporter()
        
        # Invalid YAML handling
        invalid_yaml = "invalid: yaml: content: ["
        with pytest.raises(ValueError) as exc_info:
            importer.create_document_from_template(invalid_yaml, {"DOC_NAME": "Test"}, mock_pycoda)
        assert "Invalid YAML" in str(exc_info.value)
        
        # API failure handling
        valid_yaml = "document:\n  name: 'Test Project'\n  sections: []"
        mock_pycoda.create_document.return_value = {"error": "API rate limit exceeded"}
        
        with pytest.raises(ValueError) as exc_info:
            importer.create_document_from_template(valid_yaml, {}, mock_pycoda)
        assert "Document creation failed" in str(exc_info.value)
        assert "API rate limit exceeded" in str(exc_info.value)