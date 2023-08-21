# Vue Frontend

## Auth Pattern

`login-controller` mounted at index level, and show info on side panel. It will refresh token, and on failure clear necessary local storage items.

`router/index.js` sets auth level for each router.

## Project setup

`nginx.conf` (specifically the statement `try_files $uri $uri/ /index.html`)required for `vue-router`.

- `npm install``
- Compiles and hot-reloads for development `npm run serve`.
- Compiles and minifies for production `npm run build`
- Lints and fixes files `npm run lint`
- Customize configuration see [Configuration Reference](https://cli.vuejs.org/config/).
