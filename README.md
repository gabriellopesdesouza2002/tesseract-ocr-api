# 📃 Tesseract OCR API com FastAPI

Este projeto implementa uma **API local de OCR** compatível com aplicações de automação (n8n, Node.js, Python, etc.), utilizando o **Tesseract** para extração de texto de PDFs.

---

## 🚀 Funcionalidades

📄 **Extração de texto (OCR)** de arquivos PDF com suporte a múltiplos idiomas (`por`, `eng`, `por+eng`)
⚙️ **Configuração de DPI** (qualidade da conversão de imagem para texto)
📑 **Limite de páginas opcional** (`limit_pages`) para PDFs grandes
🔐 **Proteção com autenticação Bearer (API_TOKEN)**
🐳 **Pronto para uso com Docker e docker-compose**

---

## ▶️ Como executar

docker compose up --build -d

Interface de teste (Swagger UI):
👉 [http://localhost:8085/docs](http://localhost:8085/docs)

---

## 🔐 Variáveis de ambiente

| Variável    | Descrição                                | Obrigatória |
| ----------- | ---------------------------------------- | ----------- |
| `API_TOKEN` | Chave de acesso para autenticação Bearer | ✅           |

Exemplo (`docker-compose.yml`):
```
environment:
    API_TOKEN=secret-key
```

---

## 📥 Exemplo de requisição
```
curl --location 'http://localhost:8085/ocr-pdf' \
--header 'Authorization: Bearer 2342i32goq3784hf85' \
--form 'file=@"C:\Users\gablo\Downloads\Invoice-UNK1SIQL-0001.pdf"' \
--form 'lang="por+eng"' \
--form 'dpi="400"' \
--form 'limit_pages="2"'
```

---

## ⚡ Resposta esperada
```
{
"text": "Invoice 0001\nTotal: R$ 2.500,00\n...",
"parameters": {
    "language": "por+eng",
    "dpi": 400,
    "limit_pages": 2
    }
}
```
---

## 🐳 Base Docker

* **Imagem:** python:3.11-slim
* **Dependências:**

  * tesseract-ocr, tesseract-ocr-por, tesseract-ocr-eng
  * fastapi, uvicorn, pytesseract, PyMuPDF, Pillow
* **Porta exposta:** 8000
* **Modo de execução:** uvicorn main:app --host 0.0.0.0 --port 8000

---

## 🧪 Testado com

✅ Docker Compose
✅ n8n HTTP Request + Binary File
✅ Postman / cURL
✅ Python requests

---

## 💬 Exemplo de integração no n8n

Use o nó **HTTP Request**, método **POST**, tipo **multipart/form-data**, e envie:

* `file` (Binary File)
* `lang` (por ou eng)
* `dpi` (ex: 400)
* Header: `Authorization: Bearer 2342i32goq3784hf85`

---

📦 **Plug & Play:**
Suba com `docker compose up` e comece a extrair texto de PDFs em segundos.
