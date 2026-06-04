# TaskFlow
## Project Overview

TaskFlow is a backend API that a frontend application (web or mobile) would consume.

## Core Entities
EntityDescriptionBelongs to
UserAnyone who registers and logs
inTop-level entity
ProjectA container of related tasksCreated by a User (owner)
MembershipLinks a User to a Project they
can accessUser ↔ Project (many-to-many)
TaskA unit of work inside a projectBelongs to a Project, assigned to a
User
CommentA message on a taskBelongs to a Task and a User