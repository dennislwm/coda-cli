import pytest
import tempfile
import os
from unittest.mock import Mock
from common.pycoda import Pycoda
from common.document_creator import DocumentCreator


class TestDocumentCreator:
    """Consolidated tests for DocumentCreator - all functionality in one place"""
    
    def test_document_creator_instantiation(self):
        """DocumentCreator should instantiate with a Pycoda instance"""
        # Arrange
        mock_pycoda = Mock(spec=Pycoda)
        
        # Act & Assert
        creator = DocumentCreator(mock_pycoda)
        
        # Verify the instance was created and has the expected dependency
        assert creator is not None
        assert hasattr(creator, 'pycoda')
        assert creator.pycoda is mock_pycoda

    def test_substitute_variables_in_simple_string(self):
        """DocumentCreator should replace {{VARIABLE}} patterns in strings"""
        # Arrange
        mock_pycoda = Mock(spec=Pycoda)
        creator = DocumentCreator(mock_pycoda)
        content = "Project: {{PROJECT_NAME}}, Status: {{STATUS}}"
        variables = {"PROJECT_NAME": "Test Project", "STATUS": "Active"}
        
        # Act
        result = creator.substitute_variables(content, variables)
        
        # Assert
        assert result == "Project: Test Project, Status: Active"

    def test_substitute_variables_in_dictionary(self):
        """DocumentCreator should replace {{VARIABLE}} patterns in nested dictionary structures"""
        # Arrange
        mock_pycoda = Mock(spec=Pycoda)
        creator = DocumentCreator(mock_pycoda)
        
        # Template-like dictionary structure
        content = {
            "document": {
                "name": "{{PROJECT_NAME}} Dashboard",
                "sections": [
                    {
                        "name": "Overview", 
                        "content": "Project: {{PROJECT_NAME}}, Lead: {{LEAD_NAME}}"
                    }
                ]
            }
        }
        variables = {"PROJECT_NAME": "Test Project", "LEAD_NAME": "John Doe"}
        
        # Act
        result = creator.substitute_variables(content, variables)
        
        # Assert
        assert result["document"]["name"] == "Test Project Dashboard"
        assert result["document"]["sections"][0]["content"] == "Project: Test Project, Lead: John Doe"

    def test_load_template_from_yaml_file(self):
        """DocumentCreator should load and parse valid YAML template files"""
        # Arrange
        mock_pycoda = Mock(spec=Pycoda)
        creator = DocumentCreator(mock_pycoda)
        
        template_content = """
document:
  name: "{{PROJECT_NAME}} Dashboard"
  sections:
    - name: "Project Overview"
      type: "canvas"
      content: "Welcome to {{PROJECT_NAME}}"
    - name: "Task List"
      type: "table"
      columns: ["Task", "Assignee", "Status"]
"""
        
        # Create temporary YAML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            temp_file.write(template_content)
            temp_file_path = temp_file.name
        
        try:
            # Act
            result = creator.load_template(temp_file_path)
            
            # Assert
            assert result is not None
            assert "document" in result
            assert result["document"]["name"] == "{{PROJECT_NAME}} Dashboard"
            assert len(result["document"]["sections"]) == 2
            assert result["document"]["sections"][0]["type"] == "canvas"
            assert result["document"]["sections"][1]["type"] == "table"
            assert "Task" in result["document"]["sections"][1]["columns"]
        finally:
            # Cleanup
            os.unlink(temp_file_path)

    def test_create_document_from_template(self):
        """DocumentCreator should create Coda documents from processed templates"""
        # Arrange
        mock_pycoda = Mock(spec=Pycoda)
        mock_pycoda.create_document.return_value = {"id": "doc123", "name": "Test Project Dashboard"}
        mock_pycoda.add_section.return_value = {"id": "section456"}
        
        creator = DocumentCreator(mock_pycoda)
        
        # Processed template (after variable substitution)
        processed_template = {
            "document": {
                "name": "Test Project Dashboard",
                "sections": [
                    {
                        "name": "Project Overview",
                        "type": "canvas",
                        "content": "Welcome to Test Project"
                    }
                ]
            }
        }
        
        # Act
        result = creator.create_document_from_template(processed_template)
        
        # Assert
        assert result["document_id"] == "doc123"
        mock_pycoda.create_document.assert_called_once_with("Test Project Dashboard")
        mock_pycoda.add_section.assert_called_once_with("doc123", "Project Overview", "canvas", "Welcome to Test Project")