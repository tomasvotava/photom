# photom

[![codecov](https://codecov.io/gh/tomasvotava/photom/branch/master/graph/badge.svg?token=JPFB0DLWMU)](https://codecov.io/gh/tomasvotava/photom)
![Project License](https://img.shields.io/github/license/tomasvotava/photom)
![Tests Workflow Status](https://img.shields.io/github/actions/workflow/status/tomasvotava/photom/test.yml?label=tests)
![Pylint Workflow Status](https://img.shields.io/github/actions/workflow/status/tomasvotava/photom/lint.yml?label=pylint)
![Mypy Workflow Status](https://img.shields.io/github/actions/workflow/status/tomasvotava/photom/lint.yml?label=mypy)
![Latest Release](https://img.shields.io/github/v/release/tomasvotava/photom)

## Running

### Backend

Create `.env` file:

```env
GOOGLE_CLIENT_ID="<client-id>"
GOOGLE_CLIENT_SECRET="<client-secret>"
OAUTHLIB_INSECURE_TRANSPORT=1
STORE_BACKEND_PATH="./store.sqlite3"
HOST="localhost"
PORT=3000
```

Run:

```console
poetry install
python -m photom.api.asgi
```

### Frontend

```console
cd frontend
yarn install
echo 'PUBLIC_API_URL=http://localhost:3000' > .env
yarn dev
```
