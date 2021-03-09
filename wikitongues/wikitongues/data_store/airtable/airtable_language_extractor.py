from ...language import Language

from abc import ABC, abstractmethod


class IAirtableLanguageExtractor(ABC):
    @abstractmethod
    def extract_languages_from_json(self, json_obj):
        pass

    @abstractmethod
    def extract_language_from_json(self, json_obj):
        pass


class AirtableLanguageExtractor(IAirtableLanguageExtractor):

    RECORDS = 'records'
    FIELDS = 'fields'
    IDENTIFIER = 'Identifier'
    STANDARD_NAME = 'Standardized Name'
    WIKIPEDIA_URL = 'wikipedia_url'

    def extract_languages_from_json(self, json_obj):
        return list(
            map(self.extract_language_from_json, json_obj[self.RECORDS]))

    def extract_language_from_json(self, json_obj):
        fields = json_obj[self.FIELDS]

        return Language(
            fields[self.IDENTIFIER],
            fields[self.STANDARD_NAME],
            fields[self.WIKIPEDIA_URL])
