# Edge RAG Evaluator

BEIR 기반 평가와 RAGAS 점수를 계산하는 CLI 모듈입니다.

CLI module that evaluates BEIR retrieval and computes RAGAS metrics.

---
## 개요 / Overview
- 외부 서버에 질문을 POST로 전송합니다.
- 응답을 기반으로 BEIR / RAGAS 평가를 실행합니다.
- 결과를 JSON/Markdown으로 저장할 수 있습니다.


- Sends questions to an external server via POST.
- Runs BEIR / RAGAS evaluation from the responses.
- Persists results as JSON/Markdown.

---
## 설치 / Installation
```bash
uv sync
```

---
## 사용법 / Usage
```bash
uv run main.py \
  --dataset scifact \
  --base-url http://localhost:8000 \
  --top-k 5 \
  --ragas-metric Faithfulness \
  --ragas-metric ResponseRelevancy
```

---
## GitHub Actions Automation
- `CI and Deploy`: `push`/`pull_request`마다 테스트를 실행하고, `master`/`main` push 시 VM에 최신 코드를 반영합니다.
- `Run Evaluation`: GitHub Actions의 `workflow_dispatch` 버튼으로 평가를 수동 실행합니다.

### GitHub Secrets
- `VM_HOST`: Compute Engine external IP or hostname
- `VM_USER`: SSH login user
- `VM_SSH_KEY`: private key for a deploy key that can SSH into the VM

### GitHub Variables
- `VM_APP_DIR`: optional, defaults to `/home/<VM_USER>/edge_rag_server`
- `VM_SSH_PORT`: optional, defaults to `22`

### VM Setup
```bash
ssh-keygen -t ed25519 -f ~/.ssh/github_actions_vm -C "github-actions"
cat ~/.ssh/github_actions_vm.pub >> ~/.ssh/authorized_keys
git clone <YOUR_GITHUB_REPO_URL> ~/edge_rag_server
cd ~/edge_rag_server
~/.local/bin/uv sync --frozen
```

Save the contents of `~/.ssh/github_actions_vm` as the GitHub secret `VM_SSH_KEY`.

After that, code deployment is automatic on `push`, while evaluation remains a manual GitHub Actions run.
---
## 아키텍처 / Architecture
UML 다이어그램: `UML/evaluation_architecture.puml`

---
### 다이어그램 이미지 / Diagram Image
![Evaluation Architecture](UML/image.png)

---
## 요청/응답 스키마 / Request/Response Schema

이 모듈은 외부 서버로 단일 POST 요청을 보냅니다.

The module sends a single POST request to an external server.


서버는 아래 형식의 요청 본문을 받고, 동일한 스키마로 응답해야 합니다.

The server should accept the request body and return a response in the format below.

### Request (JSON)
```json
{
  "question": "string",
  "top_k": 5
}
```

### Response (JSON)
```json
{
  "answer": "string",
  "contexts": [
    {
      "id": "doc_id",
      "text": "context chunk",
      "score": 0.91
    }
  ]
}
```
