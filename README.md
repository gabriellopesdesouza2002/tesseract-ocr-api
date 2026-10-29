<div align="center">

# Tesseract OCR API

**API REST em Python para extrair texto de documentos PDF usando Tesseract OCR.**

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![OCR](https://img.shields.io/badge/Tesseract-OCR-blue)

*Python · FastAPI · Tesseract · PyMuPDF · Docker*

</div>

## Visão geral / Overview

Esta API recebe um **PDF via HTTP**, converte suas páginas em imagens e utiliza o Tesseract para extrair o texto. Foi criada para uso em automações e integração com ferramentas como **n8n**, scripts Python e outros clientes HTTP.

**EN:** Local REST API that extracts text from PDF files with FastAPI, Tesseract and Docker. Supports configurable OCR language, DPI and page limits.

## Funcionalidades

- `POST /ocr-pdf` — recebe um arquivo PDF e devolve o texto extraído em JSON.
- **Idiomas:** `por`, `eng` e `por+eng` com os pacotes de idioma da imagem Docker.
- **DPI configurável** pelo parâmetro de formulário `dpi` (padrão: `300`).
- **Limite de páginas opcional** via `limit_pages`.
- **Autenticação Bearer** no endpoint de OCR, configurada com `API_TOKEN`.
- **Documentação OpenAPI** gerada pelo FastAPI em `/docs`.

## Executar com Docker Compose

Requisitos: Git e Docker com Compose.

```bash
git clone https://github.com/gabriellopesdesouza2002/tesseract-ocr-api.git
cd tesseract-ocr-api
docker compose up --build -d
```

O Compose atual publica a porta **8085** do host para a porta **8000** do contêiner. A documentação interativa fica em:

**http://localhost:8085/docs**

> **Configuração antes de uso real:** o `docker-compose.yml` publicado contém um `API_TOKEN` de exemplo definido diretamente no arquivo. Substitua-o por um valor privado e restrinja o acesso à porta antes de qualquer exposição fora de um ambiente local controlado. O projeto não deve ser tratado como uma API pública pronta para produção sem revisão adicional.

## Exemplo de requisição

Envie um PDF em `multipart/form-data` para `/ocr-pdf`, com o token configurado no ambiente:

```bash
curl --request POST "http://localhost:8085/ocr-pdf" \
  --header "Authorization: Bearer SEU_TOKEN_CONFIGURADO" \
  --form "file=@documento.pdf" \
  --form "lang=por+eng" \
  --form "dpi=300" \
  --form "limit_pages=2"
```

Campos aceitos:

| Campo | Tipo | Padrão | Descrição |
| --- | --- | --- | --- |
| `file` | arquivo | obrigatório | PDF enviado para OCR |
| `lang` | string | `por` | Idioma(s) do Tesseract |
| `dpi` | inteiro | `300` | Resolução da conversão |
| `limit_pages` | inteiro opcional | todas | Quantidade máxima de páginas |

Resposta ilustrativa:

```json
{
  "text": "Exemplo de texto extraído do PDF.",
  "parameters": {
    "language": "por+eng",
    "dpi": 300,
    "limit_pages": 2
  }
}
```

## Integração com n8n

Use um nó **HTTP Request** com método `POST` para `http://localhost:8085/ocr-pdf` (ou o endereço acessível a partir do ambiente do n8n).

Configure a autenticação no header `Authorization: Bearer ...` e envie o documento como **Binary File** no campo `file`. Os demais parâmetros (`lang`, `dpi` e `limit_pages`) devem ir como campos do formulário.

> Se o n8n estiver em outro contêiner ou host, `localhost` apontará para o próprio ambiente do n8n, não necessariamente para esta API. Ajuste a conectividade entre os serviços.

## Arquitetura

- [`main.py`](main.py) — aplicação FastAPI, autenticação e endpoint HTTP.
- [`ocr.py`](ocr.py) — renderização de páginas via PyMuPDF e OCR via pytesseract.
- [`Dockerfile`](Dockerfile) — imagem Python com Tesseract e pacotes de idioma.
- [`docker-compose.yml`](docker-compose.yml) — configuração local do serviço.
- [`requirements.txt`](requirements.txt) — dependências Python.

## Limitações conhecidas

O processamento atual renderiza páginas do PDF em arquivos temporários, então arquivos grandes podem consumir bastante memória, CPU e espaço em disco. O código também não implementa, por si só, limites de upload, controle de concorrência ou uma rotina completa de limpeza de arquivos temporários em todos os caminhos de erro.

O projeto é um exemplo de API de OCR para integração e automação; avalie esses pontos antes de processar documentos sensíveis ou utilizá-lo em ambientes externos.

## Contato

Projeto de [Gabriel Lopes](https://github.com/gabriellopesdesouza2002). Sugestões e correções podem ser encaminhadas pelo [GitHub Issues](https://github.com/gabriellopesdesouza2002/tesseract-ocr-api/issues).
