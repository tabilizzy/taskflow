# TaskFlow: Team Task Management REST API

TaskFlow is a production-ready, high-performance REST API designed to power collaborative project management applications (like a lightweight Trello or Linear). It supports multi-tenant teams, secure JWT authentication, structured task workflows, and relational data cascading, backed by PostgreSQL.


---

##  Live Demo & Documentation
- **API Base URL:** `https://onrender.com`
- **Interactive OpenAPI Docs:** `https://onrender.com/docs`
- **Swagger URL: ** `http://127.0.0.1:8000/docs#/`

---

## Features & Technical Stack

- **Framework:** FastAPI (Python 3.10+)
- **ORM / Database Layer:** SQLModel (SQLAlchemy) + PostgreSQL
- **Security:** JWT (JSON Web Tokens) with asymmetric/symmetric signing + `passlib` (Bcrypt) password hashing.
- **Data Validation:** Pydantic v2 (Strict typing, structural validation, and multi-model pattern configurations).
- **Access Control:** Context-driven middleware verifying project ownership, memberships, and content authorization rules.


##  Database Schema Architectural Layout

The API enforces strict multi-tenant access boundaries around five core entities:
1. **User**: Handled via standard user identity registration.
2. **Project**: Top-level task containers managed and owned by a User.
3. **Membership**: Many-to-many bridge linking Users to Projects with specific access permissions (`owner` | `member`).
4. **Task**: Action items nested under parent Projects and assigned to team members.
5. **Comment**: Threaded communications linked directly to individual Tasks.



##  API Endpoints & Access Control Matrix

### Authentication (`/auth`)
* `POST /auth/register` — Register a new account (Public)
* `POST /auth/login` — Exchange credentials for a JWT token (Public)
* `GET /auth/me` — Retrieve profile data for the authenticated session (🔒 Authenticated)

### Projects (`/projects`)
* `POST /projects` — Create a project; automatically sets the creator as `owner` (🔒 Authenticated)
* `GET /projects` — List all projects you own or are a member of (🔒 Member)
* `GET /projects/{id}` — View detail profiles (🔒 Member)
* `PUT /projects/{id}` — Modify name/description metrics (🔒 👑 Owner Only)
* `DELETE /projects/{id}` — Permanently delete a project and cascade all its items (🔒 👑 Owner Only)
* `POST /projects/{id}/members` — Invite a user by username (🔒 👑 Owner Only)
* `DELETE /projects/{id}/members/{uid}` — Remove a user from the project space (🔒 👑 Owner Only)

### Tasks (`/projects/{project_id}/tasks`)
* `GET /projects/{id}/tasks` — Fetch tasks with integrated parameter filters for `status`, `priority`, or `assignee_id` (🔒 Member)
* `POST /projects/{id}/tasks` — Instantiate a task asset (🔒 Member)
* `PUT /projects/{id}/tasks/{tid}` — Update execution elements (🔒 Member)
* `DELETE /projects/{id}/tasks/{tid}` — Delete a task (🔒 Creator / 👑 Owner Only)

### Comments (`/tasks/{task_id}/comments`)
* `GET /tasks/{id}/comments` — View task timeline logs sequentially by date (🔒 Member)
* `POST /tasks/{id}/comments` — Post a message onto a task card (🔒 Member)
* `DELETE /tasks/{id}/comments/{cid}` — Delete a specific comment (🔒 Author Only)



