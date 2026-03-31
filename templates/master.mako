<!doctype html>
<html lang="${l.language}">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>${self.title()}</title>
    % if settings.production:
      <script type="module" src="/assets/main.js"></script>
    % else:
      <script type="module" src="${settings.www}/@vite/client"></script>
      <script type="module" src="${settings.www}/src/main.js"></script>
    % endif
    <!-- link href="/static/index.css" rel="stylesheet" -->
  </head>
  <body class="bg-primary flex">
    <main class="bg-secondary flex-1">
      ${self.body()}
    </main>
  </body>
</html>
