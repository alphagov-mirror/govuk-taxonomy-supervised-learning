import unittest
import responses
from data_extraction import content_export
from test.data_extraction.content_store_helpers import *


class TestContentLinksGenerator(unittest.TestCase):

    @responses.activate
    def test_content_links_generator(self):
        responses.add(responses.GET, "http://example.com/search.json", json=content_links)
        response = content_export.content_links_generator(rummager_url="http://example.com")
        self.assertListEqual(list(response), ['/first/path', '/second/path'])


class TestGetContent(unittest.TestCase):

    @responses.activate
    def test_404_response(self):
        responses.add(responses.GET, "http://example.com/content/base_path", status=404)
        self.assertFalse(content_export.get_content('/base_path', content_store_url="http://example.com"))

    @responses.activate
    def test_simple_content(self):
        responses.add(responses.GET, "http://example.com/content/base_path", json=content_without_taxons)
        expected = {"base_path": "/base_path", "content_id": "d282d35a-2bd2-4e14-a7a6-a04e6b10520f"}
        response = content_export.get_content('/base_path',
                                              content_store_url="http://example.com")
        self.assertEquals(expected.get('base_path'), response.get('base_path'))
        self.assertEquals(expected.get('content_id'), response.get('content_id'))

    @responses.activate
    def test_taxons(self):
        responses.add(responses.GET, "http://example.com/content/base_path", json=content_with_taxons)
        expected = [{"content_id": "237b2e72-c465-42fe-9293-8b6af21713c0"},
                    {"content_id": "8da62d85-47c0-42df-94c4-eaaeac329671"}]
        response = content_export.get_content('/base_path',
                                              content_store_url="http://example.com")

        self.assertListEqual(response.get('links').get('taxons'), expected)

    @responses.activate
    def test_primary_publishing_organisations(self):
        responses.add(responses.GET, "http://example.com/content/base_path", json=content_with_ppo)
        expected = {"title": "title1"}
        response = content_export.get_content('/base_path',
                                              content_store_url="http://example.com")
        self.assertDictEqual(response.get('links').get('primary_publishing_organisation')[0], expected)
