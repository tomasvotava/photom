# photom

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
