---
name: firebase-mathjconjean
description: Administra el sitio Math con Jean en Firebase Hosting (proyecto mathjconjean, https://mathjconjean.web.app). Usala al publicar, iniciar sesion en Firebase, conectar el MCP de Firebase en Claude Code, o cambiar la cache y los archivos estaticos de este sitio.
---

# Firebase Math con Jean

Proyecto: `mathjconjean`
Sitio: https://mathjconjean.web.app
Cuenta de este directorio: `isasdaniel64@gmail.com`
Trabaja en la raiz del repositorio (ahi estan `firebase.json` y `.firebaserc`).

## Conectar Claude Code

Este repositorio incluye `.mcp.json`. Claude Code arranca el MCP `firebase` al abrir la carpeta. Si no esta conectado, desde la raiz:

```shell
claude mcp add firebase npx -- -y firebase-tools@latest mcp --dir .
claude mcp list
```

Tiene que verse `firebase` conectado. El MCP usa la sesion del Firebase CLI, no la consola del navegador.

Antes de publicar o listar proyectos:

```shell
firebase login:use isasdaniel64@gmail.com
firebase projects:list
```

`mathjconjean` tiene que aparecer. Si la cuenta no esta en `firebase login:list`:

```shell
firebase login:add isasdaniel64@gmail.com
```

En el navegador elige ese correo y permite el acceso. No publiques con otra cuenta.

## Publicar

Solo Hosting.

```shell
python tools/generar_lista.py
firebase deploy --only hosting --project mathjconjean
```

Comprueba que https://mathjconjean.web.app responda 200.

## Cache que hay que conservar

- `index.html` se reutiliza 5 minutos (`max-age=300`). No lo pongas en `no-cache`: cada visita volveria a bajar todo el HTML.
- `version.json` es la huella, cache de 60 segundos. La pagina no lo vuelve a pedir en los 90 segundos siguientes de la misma pestaña.
- `materiales.json` y `videos.txt` solo se bajan si `version.json` trae su huella y esa huella no esta ya guardada. La URL lleva `?v=huella`.
- `logo.png` y `marca.png` van aparte. No los incrustes otra vez en base64 dentro del HTML.
- La vista previa de un PDF pide solo las paginas visibles (`disableAutoFetch` y `disableStream`). No descargues el PDF completo para mostrarlo.
- No guardes claves de cuenta de servicio ni tokens en el repositorio.
