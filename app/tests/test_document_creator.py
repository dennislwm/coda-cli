# Test file for DocumentCreator TDD implementation
import pytest
from unittest.mock import Mock
from common.document_creator import DocumentCreator
from common.pycoda import Pycoda


class TestDocumentCreator:
    """Consolidated tests for DocumentCreator - following streamlined TDD approach"""

    def test_document_creator_instantiation(self):
        """DocumentCreator should be instantiable with Pycoda client"""
        # Arrange
        mock_pycoda = Mock(spec=Pycoda)

        # Act
        creator = DocumentCreator(mock_pycoda)

        # Assert
        assert creator is not None
        assert creator.client == mock_pycoda

    def test_substitute_variables_in_simple_string(self):
        """DocumentCreator should replace {{VARIABLE}} patterns with provided values"""
        # Arrange
        mock_pycoda = Mock(spec=Pycoda)
        creator = DocumentCreator(mock_pycoda)
        template_string = "Hello {{NAME}}, welcome to {{PROJECT}}!"
        variables = {"NAME": "Alice", "PROJECT": "MyApp"}

        # Act
        result = creator.substitute_variables(template_string, variables)

        # Assert
        assert result == "Hello Alice, welcome to MyApp!"

    def test_substitute_variables_in_dictionary(self):
        """DocumentCreator should replace variables in nested dictionary structure"""
        # Arrange
        mock_pycoda = Mock(spec=Pycoda)
        creator = DocumentCreator(mock_pycoda)
        template_dict = {
            "name": "{{PROJECT_NAME}} Dashboard",
            "metadata": {
                "version": "{{VERSION}}",
                "title": "{{PROJECT_NAME}} Documentation"
            }
        }
        variables = {"PROJECT_NAME": "MyProject", "VERSION": "1.0"}

        # Act
        result = creator.substitute_variables(template_dict, variables)

        # Assert
        expected = {
            "name": "MyProject Dashboard",
            "metadata": {
                "version": "1.0",
                "title": "MyProject Documentation"
            }
        }
        assert result == expected