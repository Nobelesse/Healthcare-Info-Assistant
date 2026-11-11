import httpx
import pytest
from services import ollama_service as ollama


def test_emergency_notice():
    assert "Emergency" in ollama.emergency_notice("I have severe chest pain", "en")
    assert "आपातकाल" in ollama.emergency_notice("सांस नहीं आ रही", "hi")
    assert ollama.emergency_notice("What is a vitamin?", "en")==""


def test_local_ollama_message_shape(monkeypatch):
    captured={}
    class FakeResponse:
        def raise_for_status(self):pass
        def json(self):return {"message":{"content":"## Medical definition\nEducational answer."}}
    def fake_post(url,*,json,timeout):
        captured.update({"url":url,"body":json})
        return FakeResponse()
    monkeypatch.setattr(ollama.httpx,"post",fake_post)
    answer=ollama.medical_answer("What is anemia?","en")
    assert "Educational answer" in answer
    assert captured["url"].startswith("http://127.0.0.1:11434/")
    assert captured["body"]["stream"] is False
    assert captured["body"]["messages"][0]["role"]=="system"


def test_offline_error_is_user_friendly(monkeypatch):
    def no_connection(*args,**kwargs):
        raise httpx.ConnectError("Connection refused")
    monkeypatch.setattr(ollama.httpx,"post",no_connection)
    with pytest.raises(ollama.OllamaUnavailable,match="local Ollama"):
        ollama.medical_answer("What is vitamin D?","en")
