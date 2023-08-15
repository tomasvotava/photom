FROM node:18.17 as builder

ENV PUBLIC_API_URL=http://localhost:3000

WORKDIR /build

COPY frontend/yarn.lock frontend/package.json /build/

RUN yarn install --frozen-lockfile

COPY frontend /build

RUN yarn build

FROM nginx:1.21

COPY --from=builder /build/build /usr/share/nginx/html

# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
