# AGENTS.md

## Project Overview

This is a Todo List REST API built with Python and FastAPI.

This project is primarily for learning backend development concepts step by step.

The goal is not only to make the code work, but also to understand why each part is implemented that way.

The project is being developed incrementally based on mentoring feedback.

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLite

Prefer simple solutions and Python standard libraries when they are sufficient.

Do not introduce additional frameworks, ORMs, or dependencies unless they are explicitly requested or clearly necessary.

## Current Architecture

The project separates Todo Lists and Todos.

Repository responsibilities are also separated:

- `TodoListRepository` manages Todo Lists.
- `TodoRepository` manages Todos.

Keep these responsibilities separated unless explicitly asked to redesign the architecture.

## Existing API Rules

Preserve the existing API behavior unless explicitly asked to change it.

Important conventions:

- Use UTC for datetime values.
- Return `400 Bad Request` when a requested Todo or Todo List does not exist.
- Return `200 OK` when deletion succeeds.
- Keep `complete` and `uncomplete` operations as separate endpoints.
- Keep Todo List and Todo responsibilities separated.
- Keep repository responsibilities separated.

Do not change these conventions simply because another convention is more common.

## Development Principles

Before making changes:

1. Inspect the existing code and project structure.
2. Understand the current implementation.
3. Identify the smallest necessary change.
4. Preserve the current architecture whenever possible.
5. Avoid unnecessary abstraction or overengineering.
6. Do not perform large refactoring unless explicitly requested.
7. Do not add unnecessary dependencies.

Prefer small and understandable changes over large generated implementations.

If multiple implementation approaches are possible, explain the simplest approach first.

## Learning Guidelines

This is a learning project, so do not only provide finished code.

When introducing a new concept:

- Briefly explain what it is.
- Explain why it is needed in this project.
- Connect it to the existing code.
- Prefer beginner-friendly explanations.
- Avoid introducing advanced patterns unless they are necessary.

When asked to plan a change, do not modify files until explicitly asked to implement it.

When implementing a change, explain the important changes after completing the work.

## Database Guidelines

The current learning goal is SQLite integration.

When working with SQLite:

- Prefer Python's built-in `sqlite3` module.
- Do not introduce SQLAlchemy or another ORM unless explicitly requested.
- Explain new SQL queries and database operations.
- Preserve the existing Repository structure where practical.
- Keep database-related logic out of API endpoint functions when possible.
- Introduce database changes incrementally.

## Agent Behavior

Always read this `AGENTS.md` before working on the project.

Do not rewrite working code only for stylistic reasons.

Do not make large architectural decisions without explanation.

If the user's request is ambiguous, explain the available options before making a major change.

Prioritize helping the user understand the project over maximizing implementation speed.