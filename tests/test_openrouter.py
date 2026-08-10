import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from models import openrouter


class OpenRouterAdapterTests(unittest.TestCase):
    def _response(self, content="ok", usage=None):
        response = Mock()
        response.ok = True
        response.json.return_value = {
            "choices": [{"message": {"content": content}}],
            "usage": usage or {},
        }
        return response

    @patch.dict(
        os.environ,
        {"OPENROUTER_API_KEY": "test-key", "OPENROUTER_LOG_USAGE": "0"},
        clear=False,
    )
    @patch("models.openrouter.requests.post")
    def test_text_request_is_capped_and_disables_reasoning(self, post):
        post.return_value = self._response('{"choice":"A"}')

        answer = openrouter.ask_text(
            'Choose. Return JSON only in this shape: {"choice": "A"}'
        )

        self.assertEqual(answer, '{"choice":"A"}')
        request = post.call_args.kwargs["json"]
        self.assertEqual(request["max_tokens"], openrouter.MAX_TOKENS)
        self.assertEqual(request["top_p"], 1)
        self.assertEqual(request["reasoning"]["effort"], "none")
        response_format = request["response_format"]
        self.assertEqual(response_format["type"], "json_schema")
        schema = response_format["json_schema"]["schema"]
        self.assertTrue(response_format["json_schema"]["strict"])
        self.assertEqual(
            schema["properties"]["choice"]["enum"], list("ABCDE")
        )
        self.assertFalse(schema["additionalProperties"])
        self.assertIn("Choose.", request["messages"][1]["content"])

    @patch.dict(
        os.environ,
        {"OPENROUTER_API_KEY": "test-key", "OPENROUTER_LOG_USAGE": "0"},
        clear=False,
    )
    @patch("models.openrouter.requests.post")
    def test_dialogue_request_does_not_force_json(self, post):
        post.return_value = self._response("How can I help?")

        openrouter.ask_text("Respond naturally.")

        request = post.call_args.kwargs["json"]
        self.assertNotIn("response_format", request)

    @patch.dict(
        os.environ,
        {"OPENROUTER_API_KEY": "test-key", "OPENROUTER_LOG_USAGE": "0"},
        clear=False,
    )
    @patch("models.openrouter.requests.post")
    def test_audio_request_uses_openrouter_input_audio_shape(self, post):
        post.return_value = self._response("heard it")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.wav"
            path.write_bytes(b"RIFFtest")

            answer = openrouter.ask(str(path), "What did you hear?")

        self.assertEqual(answer, "heard it")
        content = post.call_args.kwargs["json"]["messages"][1]["content"]
        self.assertEqual(content[0]["type"], "text")
        self.assertEqual(content[1]["type"], "input_audio")
        self.assertEqual(content[1]["input_audio"]["format"], "wav")
        self.assertNotIn("test-key", str(post.call_args.kwargs["json"]))

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_key_fails_before_network_request(self):
        with self.assertRaisesRegex(RuntimeError, "OPENROUTER_API_KEY"):
            openrouter.ask_text("hello")

    def test_list_content_is_normalized_to_text(self):
        payload = {
            "choices": [
                {
                    "message": {
                        "content": [
                            {"type": "text", "text": "one"},
                            {"type": "output_text", "text": " two"},
                        ]
                    }
                }
            ]
        }
        self.assertEqual(openrouter._response_text(payload), "one two")

    @patch.dict(
        os.environ,
        {"OPENROUTER_API_KEY": "test-key", "OPENROUTER_LOG_USAGE": "0"},
        clear=False,
    )
    @patch("models.openrouter.requests.post")
    def test_usage_can_be_consumed_once(self, post):
        response = self._response(
            "ok",
            {
                "prompt_tokens": 12,
                "completion_tokens": 3,
                "total_tokens": 15,
                "cost": 0.0001,
            },
        )
        response.json.return_value["model"] = "resolved/model"
        post.return_value = response

        openrouter.ask_text("hello")

        usage = openrouter.pop_usage()
        self.assertEqual(usage["total_tokens"], 15)
        self.assertEqual(usage["resolved_model"], "resolved/model")
        self.assertEqual(openrouter.pop_usage(), {})


if __name__ == "__main__":
    unittest.main()
