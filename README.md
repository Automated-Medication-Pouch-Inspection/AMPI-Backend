# MEDILUX Backend

FastAPI로 API 개발을 시작하기 위한 기본 프로젝트입니다. 서버 실행, 설정 관리, API 경로 분리, 응답 형식 정의, 기본 테스트를 포함합니다.

## 로컬에서 실행하기

Python 3.12 이상이 필요합니다. 아래 명령은 macOS 터미널에서 실행하는 예시입니다. Python 3.13 등 다른 지원 버전을 사용한다면 첫 번째 명령의 `python3.12`를 해당 실행 명령으로 바꾸세요.

먼저 터미널에서 이 README가 있는 `backend` 폴더로 이동한 뒤 실행합니다.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
cp .env.example .env
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

`.venv`는 이 프로젝트의 Python 패키지를 설치할 공간입니다. `.[dev]`는 서버 실행에 필요한 패키지와 테스트·코드 검사 도구를 함께 설치합니다. `--reload`는 개발 중 Python 파일을 수정하면 서버를 다시 시작합니다.

`.env` 복사는 처음 설정할 때 한 번만 실행하세요. 이미 수정한 `.env`가 있다면 다시 복사할 필요가 없습니다.

서버가 실행되면 다음 주소에서 확인할 수 있습니다.

| 주소 | 용도 |
| --- | --- |
| [상태 확인](http://127.0.0.1:8000/api/v1/health) | 서버가 요청에 응답하는지 확인 |
| [Swagger UI](http://127.0.0.1:8000/docs) | API 목록을 보고 직접 요청 실행 |
| [ReDoc](http://127.0.0.1:8000/redoc) | API 설명과 데이터 형식 확인 |
| [OpenAPI JSON](http://127.0.0.1:8000/openapi.json) | API 명세를 JSON으로 확인 |

`GET /api/v1/health`의 응답은 다음과 같습니다.

```json
{"status":"ok"}
```

`/` 경로에는 API가 등록되어 있지 않으므로 `404 Not Found`가 표시됩니다. 실행 확인에는 `/api/v1/health`를 사용하세요.

서버를 종료할 때는 `Control + C`를 누릅니다. 새 터미널에서 다시 실행할 때는 `backend` 폴더에서 아래 두 명령만 실행하면 됩니다.

```bash
source .venv/bin/activate
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 프로젝트 구조

주요 파일의 역할은 다음과 같습니다.

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── router.py
│   │   └── routes/
│   │       └── health.py
│   ├── core/
│   │   └── config.py
│   └── schemas/
│       └── health.py
├── tests/
├── .env.example
├── pyproject.toml
└── README.md
```

| 파일·폴더 | 역할 |
| --- | --- |
| `app/main.py` | `create_app()`에서 설정과 라우터를 연결해 FastAPI 앱을 만듭니다. Uvicorn은 여기의 `app`을 실행합니다. |
| `app/api/router.py` | 개별 라우터를 모으고 공통 URL 앞부분인 `/api/v1`을 붙입니다. |
| `app/api/routes/health.py` | `/health` 요청을 받아 응답하는 함수를 정의합니다. |
| `app/schemas/health.py` | 상태 확인 API가 반환할 데이터의 필드와 타입을 정의합니다. |
| `app/core/config.py` | 환경 변수와 `.env`를 읽고 설정값을 검증합니다. |
| `tests/` | 앱의 기본 동작을 자동으로 확인하는 테스트를 둡니다. |
| `.env.example` | 로컬 설정 파일을 만들 때 복사하는 예시입니다. |
| `pyproject.toml` | Python 버전, 의존성, 테스트와 코드 검사 설정을 관리합니다. |

라우터는 URL별 처리 함수를 묶는 단위입니다. 이 프로젝트에서는 `/api/v1`이라는 공통 경로와 `/health`라는 개별 경로가 합쳐져 `/api/v1/health`가 됩니다. [FastAPI 공식 문서: 여러 파일로 앱 구성하기](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

## 설정 변경하기

`backend/.env`에서 설정을 변경할 수 있습니다. 설정 이름에는 `MEDILUX_` 접두사를 사용합니다.

| 환경 변수 | 기본값 | 의미 |
| --- | --- | --- |
| `MEDILUX_APP_NAME` | `MEDILUX API` | API 문서에 표시할 앱 이름 |
| `MEDILUX_ENVIRONMENT` | `development` | 실행 환경 이름. `development`, `test`, `production` 중 하나 |
| `MEDILUX_DOCS_ENABLED` | `true` | Swagger UI, ReDoc, OpenAPI 명세 제공 여부 |
| `MEDILUX_CORS_ORIGINS` | 아래 설명 참고 | 브라우저에서 API를 호출할 수 있도록 허용할 출처 목록 |

CORS 기본값은 `http://localhost:3000`, `http://127.0.0.1:3000`, `http://localhost:5173`, `http://127.0.0.1:5173`입니다. 웹 화면의 주소가 달라지면 해당 출처를 목록에 추가하세요. 목록은 쉼표로만 나열하지 않고 JSON 배열로 작성합니다.

```dotenv
MEDILUX_APP_NAME="MEDILUX API"
MEDILUX_ENVIRONMENT=development
MEDILUX_DOCS_ENABLED=true
MEDILUX_CORS_ORIGINS='["http://localhost:3000","http://localhost:5173"]'
```

위 CORS 예시는 두 출처만 허용하도록 기본 목록을 대체합니다. iOS 네이티브 앱의 `URLSession`에는 브라우저의 CORS 제한이 적용되지 않습니다.

설정은 앱을 만들 때 읽으므로 `.env`를 바꾼 뒤에는 서버를 종료하고 다시 실행하세요. 같은 이름의 환경 변수가 터미널에 설정되어 있다면 `.env`보다 우선합니다. [FastAPI 공식 문서: 설정과 환경 변수](https://fastapi.tiangolo.com/advanced/settings/)

## 테스트와 코드 검사

`backend` 폴더에서 가상 환경을 활성화한 상태로 실행합니다. 테스트를 위해 개발 서버를 별도로 켤 필요는 없습니다. [FastAPI 공식 문서: 테스트](https://fastapi.tiangolo.com/tutorial/testing/)

```bash
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

- `pytest`: 자동 테스트를 실행합니다.
- `ruff check`: 코드 규칙 위반을 검사합니다.
- `ruff format --check`: 파일을 수정하지 않고 코드 서식을 검사합니다.

서식을 자동으로 맞추려면 `python -m ruff format .`을 실행하세요.

## 새 API를 추가할 때

1. `app/api/routes/`에 API를 담당할 Python 파일을 만듭니다. 기존 `health.py`의 `APIRouter`와 요청 처리 함수를 참고하세요.
2. 요청이나 응답에 데이터 형식이 필요하면 `app/schemas/`에 Pydantic 모델을 정의합니다.
3. `app/api/router.py`에서 새 파일을 가져오고 `api_router.include_router(새_모듈.router)`로 등록합니다. `/api/v1`은 공통 라우터가 붙이므로 개별 API 경로에 중복해서 적지 않습니다.
4. `tests/`에 예상 응답과 필요한 오류 상황을 확인하는 테스트를 추가합니다.
5. 테스트와 코드 검사를 실행하고 `/docs`에서 요청·응답 형식을 확인합니다.

현재 필요한 역할만 파일로 나누었습니다. 이후 기능이 생기면 실제 책임에 맞춰 구조를 확장하세요.
