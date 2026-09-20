# RepoMedic

**RepoMedic is a portable AI agent for software project diagnosis.**

It scans a software repository, detects common project problems, connects findings to observable evidence, and produces an explainable repair plan with confidence levels.

RepoMedic is designed around a simple idea: **diagnosis should be evidence-driven, explainable, and portable across agent frameworks.**

## What it does

RepoMedic inspects a target project and produces structured findings containing:

- **Problem** - what appears to be wrong
- **Cause** - the likely reason
- **Evidence** - what was observed in the project
- **Suggested Fix** - a practical repair action
- **Confidence** - how strongly the available evidence supports the finding

Example:

```text
Project Type:
  Node.js

Problem:
  Missing start script

Cause:
  The Node.js project does not define a start script in package.json.

Evidence:
  The scripts section does not contain a start command.

Suggested Fix:
  Add a start script to package.json.

Confidence:
  High
```

## Why RepoMedic?

Many debugging tools jump directly from an error to a proposed fix. RepoMedic separates the diagnosis into observable evidence, likely cause, and suggested repair.

The core diagnostic path is deterministic, while framework adapters provide a portable interface for running the same agent logic in different ecosystems.

## Architecture

```text
                         ┌─────────────────────┐
                         │      RepoMedic      │
                         │      Agent Core     │
                         └──────────┬──────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
          Repository Scanner   Diagnostics     Result Model
                  │                 │                 │
                  │        ┌────────┼────────┐        │
                  │        ▼        ▼        ▼        │
                  │     Package   Errors  Dependencies│
                  │      Checks   Checks     Checks    │
                  └─────────────────┬─────────────────┘
                                    │
                                    ▼
                          ┌───────────────────┐
                          │ Framework Adapters│
                          └─────────┬─────────┘
                                    │
             ┌──────────────┬───────┼────────┬──────────────┐
             ▼              ▼       ▼        ▼              │
          OpenAI          CrewAI  Claude    Lyzr            │
                                  Code
```

## Project structure

```text
RepoMedic/
├── agent.yaml
├── SOUL.md
├── EXPLAINABILITY.md
├── AGENTS.md
├── DUTIES.md
├── README.md
│
├── agent.py
├── core/
│   └── result.py
│
├── tools/
│   ├── repository_scanner.py
│   ├── diagnostics.py
│   ├── diagnosis_engine.py
│   ├── dependency_checker.py
│   └── error_checker.py
│
├── adapters/
│   ├── base.py
│   ├── openai/
│   │   └── adapter.py
│   ├── crewai/
│   │   └── adapter.py
│   ├── claude/
│   │   └── adapter.py
│   └── lyzr/
│       └── adapter.py
│
└── tests/
    ├── sample_project/
    ├── broken_project/
    ├── test_all_adapters.py
    └── passport_verify.py
```

## Agent specification

RepoMedic follows the GitAgent/OpenGAP structure with:

- `agent.yaml` for agent identity and specification metadata
- `SOUL.md` for identity, principles, purpose, goals, and behavior
- `AGENTS.md` for the Maker and Checker roles
- `DUTIES.md` for separation of responsibilities
- `EXPLAINABILITY.md` for decision-making, inputs, and limitations

This structure allows the agent definition to remain independent from a single framework.

## Framework portability

RepoMedic has been verified through four framework export paths:

| Framework | Status |
|---|---|
| OpenAI SDK | ✓ Verified |
| CrewAI | ✓ Verified |
| Claude Code | ✓ Verified |
| Lyzr | ✓ Verified |

The repository also contains local adapter contracts and verification tests so the same diagnosis result can be checked across the supported adapter interfaces.

## Running RepoMedic

### 1. Clone the repository

```bash
git clone https://github.com/Jofil-Joby/RepoMedic.git
cd RepoMedic
```

### 2. Run the agent

The included broken sample project demonstrates a diagnosis:

```bash
python agent.py
```

The default example analyzes:

```text
tests/broken_project
```

### 3. Test the framework adapters

```bash
python tests/test_all_adapters.py
```

Expected result:

```text
openai: PASS
crewai: PASS
claude: PASS
lyzr: PASS

All adapter verification checks: PASS
```

## OpenAI integration

The OpenAI adapter can operate locally without an API key.

When `OPENAI_API_KEY` is available, the OpenAI adapter can additionally request an explanation from the OpenAI API while keeping the deterministic diagnosis as its input.

Install the OpenAI Python package if you want to use that optional integration:

```bash
pip install openai
```

Then configure your API key through your environment.

> The core repository diagnosis does not require an OpenAI API key.

## Diagnostics currently included

RepoMedic currently includes checks for:

### Project structure

Detects common project types including:

- Node.js
- Python
- Java Maven
- Java Gradle
- Rust
- Go

### Node.js configuration

Checks for:

- Missing `package.json`
- Missing `start` script
- Declared dependencies without a detected `node_modules` directory

### Error logs

Detects common error log files such as:

- `error.log`
- `errors.log`
- `npm-debug.log`

The diagnostic system is intentionally modular so additional project-specific checks can be added without changing the core agent interface.

## Example

Run:

```bash
python agent.py
```

Example output:

```text
RepoMedic Agent
================

Project Type:
  Node.js

Summary:
  1 problem(s) detected.

Diagnosis:
  Status: problems_detected

  Problem 1
  Problem: Missing start script
  Cause: The Node.js project does not define a start script in package.json.
  Evidence: The scripts section does not contain a start command.
  Suggested Fix: Add a start script to package.json.
  Confidence: High
```

## Verification

RepoMedic was built and verified as part of the **HiDevs × Lyzr Agent Passport Challenge**.

Official Passport result:

- **Passport status:** Validated
- **Score:** 575
- **Framework visas:** 4/4
- **OpenAI SDK:** Visa earned
- **CrewAI:** Visa earned
- **Claude Code:** Visa earned
- **Lyzr:** Visa earned

The Passport pipeline validated the GitAgent structure, checked explainability, exported the agent across framework adapters, and issued a verifiable passport.

## Design principles

RepoMedic is built around a few principles:

1. **Evidence before assumptions**
2. **Explain the diagnosis**
3. **Separate diagnosis from repair**
4. **Make uncertainty visible**
5. **Keep the agent portable**
6. **Keep framework-specific integrations isolated**

## Current limitations

RepoMedic is an evolving prototype.

Current limitations include:

- Diagnostic coverage is still limited compared with a full static-analysis platform.
- Some checks are currently focused on common project files and Node.js workflows.
- The framework adapters provide portability and verification interfaces; they should not be interpreted as full native implementations of every framework.
- Diagnosis quality depends on the project information available to the agent.

## Roadmap

Potential future work:

- [ ] Python dependency and configuration diagnostics
- [ ] JavaScript/TypeScript build diagnostics
- [ ] Git and version-control diagnostics
- [ ] Static code analysis
- [ ] Test failure analysis
- [ ] Dependency version conflict detection
- [ ] Structured JSON diagnosis reports
- [ ] Repository-level repair suggestions
- [ ] CI/CD integration
- [ ] Additional agent framework adapters

## License

No license has been specified for this repository yet.
