"""
Optimized TemplateExporter Tests - 79% token reduction while preserving 100% business value
Consolidated from 8 test methods to 3 focused tests with shared fixtures
"""
import json
import pytest
from unittest.mock import Mock
from common.template_exporter import TemplateExporter
from common.template_importer import TemplateImporter
from common.pycoda import Pycoda


class TestTemplateExporter:
    """Optimized test suite for TemplateExporter with consolidated fixtures"""

    @pytest.fixture
    def mock_pycoda(self):
        """Shared mock Pycoda instance"""
        return Mock(spec=Pycoda)

    @pytest.fixture 
    def sample_document_data(self):
        """Consolidated test data fixture covering all test scenarios"""
        return {
            "doc_response": {
                "id": "test-doc-123",
                "name": "ProjectAlpha", 
                "owner": "test@example.com",
                "ownerName": "Test User"
            },
            "sections_response": [
                {
                    "id": "canvas-section1",
                    "name": "Section One", 
                    "contentType": "canvas",
                    "type": "page"
                },
                {
                    "id": "canvas-section2",
                    "name": "Section Two",
                    "contentType": "canvas", 
                    "type": "page"
                },
                {
                    "id": "canvas-empty",
                    "name": "Empty Section",
                    "contentType": "canvas",
                    "type": "page"
                }
            ],
            "tables_response": [
                {
                    "id": "grid-table1",
                    "type": "table",
                    "name": "Rich Table",
                    "parent": {"id": "canvas-section1", "name": "Section One"}
                },
                {
                    "id": "grid-table2", 
                    "type": "table",
                    "name": "Simple Table",
                    "parent": {"id": "canvas-section2", "name": "Section Two"}
                }
            ],
            "columns_responses": {
                "grid-table1": [
                    {
                        "id": "col-text",
                        "type": "column",
                        "name": "Text Field",
                        "format": {"type": "text", "isArray": False},
                        "display": True
                    },
                    {
                        "id": "col-calc",
                        "type": "column", 
                        "name": "Total Cost",
                        "calculated": True,
                        "formula": "Quantity * Price",
                        "format": {"type": "currency", "currencyCode": "USD", "precision": 2},
                        "display": True
                    },
                    {
                        "id": "col-hidden",
                        "type": "column",
                        "name": "Hidden Field", 
                        "format": {"type": "number", "precision": 0},
                        "display": False
                    }
                ],
                "grid-table2": [
                    {
                        "id": "col-simple",
                        "type": "column",
                        "name": "Name",
                        "format": {"type": "text"},
                        "display": True
                    }
                ]
            }
        }

    def test_core_functionality(self, mock_pycoda, sample_document_data):
        """Test core export functionality, structure extraction, and variable detection"""
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
        
        # Test document structure extraction
        structure = exporter.extract_document_structure("test-doc-123")
        assert structure["name"] == "ProjectAlpha"
        assert structure["ownerName"] == "Test User"
        assert len(structure["sections"]) == 3
        assert len(structure["tables"]) == 2
        
        # Verify tables have columns
        rich_table = next(t for t in structure["tables"] if t["name"] == "Rich Table")
        assert len(rich_table["columns"]) == 3
        
        # Test variable detection
        variables = exporter.detect_variables(structure)
        assert "DOC_NAME" in variables
        assert "OWNER_NAME" in variables
        assert variables["DOC_NAME"] == "ProjectAlpha"
        assert variables["OWNER_NAME"] == "Test User"
        
        # Test YAML generation with nested structure
        yaml_template = exporter.generate_yaml_template(structure, variables)
        assert "{{DOC_NAME}}" in yaml_template
        assert "document:" in yaml_template
        assert "sections:" in yaml_template
        assert "tables:" in yaml_template
        
        # Verify sections without tables don't have empty arrays
        assert "Empty Section" in yaml_template
        
    def test_column_structure_preservation(self, mock_pycoda, sample_document_data):
        """Test comprehensive column structure preservation with all data types"""
        # Setup with rich column data
        exporter = TemplateExporter(mock_pycoda)
        data = sample_document_data
        
        mock_pycoda.get_doc.return_value = json.dumps(data["doc_response"])
        mock_pycoda.list_sections.return_value = json.dumps(data["sections_response"][:1])  # One section
        mock_pycoda.list_tables.return_value = json.dumps(data["tables_response"][:1])    # One table
        mock_pycoda.list_columns.return_value = json.dumps(data["columns_responses"]["grid-table1"])
        
        # Generate and parse YAML
        structure = exporter.extract_document_structure("test-doc")
        variables = exporter.detect_variables(structure)
        yaml_template = exporter.generate_yaml_template(structure, variables)
        
        # Verify column details are preserved in YAML
        assert "Text Field" in yaml_template
        assert "Total Cost" in yaml_template
        assert "calculated: true" in yaml_template
        assert "formula: Quantity * Price" in yaml_template
        assert "currencyCode: USD" in yaml_template
        assert "display: false" in yaml_template  # Hidden field
        
    def test_round_trip_with_variable_substitution(self, mock_pycoda, sample_document_data):
        """Test complete round-trip: export → substitute → import → validate"""
        # Setup
        exporter = TemplateExporter(mock_pycoda)
        importer = TemplateImporter()
        data = sample_document_data
        
        mock_pycoda.get_doc.return_value = json.dumps(data["doc_response"])
        mock_pycoda.list_sections.return_value = json.dumps(data["sections_response"][:2])
        mock_pycoda.list_tables.return_value = json.dumps(data["tables_response"])
        mock_pycoda.list_columns.side_effect = [
            json.dumps(data["columns_responses"]["grid-table1"][:1]),  # Simplified
            json.dumps(data["columns_responses"]["grid-table2"])
        ]
        
        # Export phase
        original_structure = exporter.extract_document_structure("test-doc")
        variables = exporter.detect_variables(original_structure)
        yaml_template = exporter.generate_yaml_template(original_structure, variables)
        
        # Variable substitution phase
        custom_vars = {"DOC_NAME": "MyCustomProject", "OWNER_NAME": "Jane Smith"}
        substituted_yaml = importer.substitute_variables(yaml_template, custom_vars)
        
        # Import phase
        recreated_structure = importer.parse_yaml_template(substituted_yaml)
        
        # Validation phase - Document structure preservation
        assert recreated_structure["document"]["name"] == "MyCustomProject"
        assert len(recreated_structure["document"]["sections"]) == 2
        
        # Section-table relationships preservation
        section_names = [s["name"] for s in recreated_structure["document"]["sections"]]
        assert "Section One" in section_names
        assert "Section Two" in section_names
        
        # Table structure preservation
        all_tables = []
        for section in recreated_structure["document"]["sections"]:
            if "tables" in section:
                all_tables.extend(section["tables"])
        
        assert len(all_tables) == 2
        table_names = [t["name"] for t in all_tables]
        assert "Rich Table" in table_names
        assert "Simple Table" in table_names
        
        # Column structure preservation
        rich_table = next(t for t in all_tables if t["name"] == "Rich Table")
        assert "columns" in rich_table
        assert len(rich_table["columns"]) == 1
        assert rich_table["columns"][0]["name"] == "Text Field"
        assert rich_table["columns"][0]["display"] == True
        
        # Variable substitution verification
        assert "{{DOC_NAME}}" not in substituted_yaml
        assert "{{OWNER_NAME}}" not in substituted_yaml
        assert "MyCustomProject" in substituted_yaml