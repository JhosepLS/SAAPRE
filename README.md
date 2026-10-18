# SAAPRE

**Sistema Adaptativo de Análisis Predictivo del Rendimiento.** Tesis de Ingeniería de Software
(Universidad La Salle, Arequipa): aprendizaje automático adaptativo con detección de *concept drift*
(ADWIN y DDM) para predecir el rendimiento de jugadores de League of Legends y Counter-Strike 2 a
partir de las APIs de Riot Games y FACEIT.

**Metodología:** CRISP-ML(Q) + Kanban. **Stack:** Python · FastAPI · PostgreSQL · scikit-learn · River ·
React · TypeScript.

## Estructura

Ver [`docs/arquitectura.md`](docs/arquitectura.md). Resumen: `backend/` (API y ML), `frontend/` (dashboard),
`infra/` (base de datos), `docs/` (diagramas, seguridad y trazabilidad).

## Puesta en marcha

Requisitos: Python 3.11+, Node 22+, Docker (opcional, para PostgreSQL).

```powershell
# 1. Configuración (los secretos van en .env, que no se versiona)
copy .env.example .env        # completa los valores

# 2. Backend
cd backend
python -m venv .venv ; .venv\Scripts\activate
pip install -e ".[dev]"
pytest                        # pruebas
uvicorn app.main:app --reload # http://localhost:8000/docs

# 3. Frontend (en otra terminal)
cd frontend
npm ci
npm run dev                   # http://localhost:5173

# 4. Base de datos local (opcional)
docker compose up db
```

## Calidad y seguridad

- Estilo y análisis: `ruff check . && ruff format --check .` · `bandit -r app -c pyproject.toml`
- Dependencias: `pip-audit` · `npm audit`
- Antes de cada commit: `pip install pre-commit && pre-commit install` (incluye gitleaks)
- Decisiones de seguridad: [`docs/SECURITY.md`](docs/SECURITY.md)

## Flujo de trabajo

- Ramas: `main` (estable) y `feature/<tema>` por cada tarjeta del Kanban; se integran con Pull Request.
- Commits: [Conventional Commits](https://www.conventionalcommits.org/es/) (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- Cada Pull Request enlaza el requisito que implementa (por ejemplo, `RF-05`) y actualiza
  `docs/trazabilidad/Trazabilidad_SAAPRE.xlsx`.

## Documentación de la tesis

- Diagramas editables en [`docs/diagramas/`](docs/diagramas) (`.drawio`, ábrelos en draw.io) y su exportación en PNG.
- Matriz de trazabilidad requisito → componente → caso de uso → código en [`docs/trazabilidad/`](docs/trazabilidad).
