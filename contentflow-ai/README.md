# ContentFlow AI

An intelligent content repurposing and automation platform built with Google's Agent Development Kit (ADK).

## Overview

ContentFlow AI is a platform that leverages AI agents to extract content from various sources, transform it into different formats, and distribute it across multiple platforms. It uses Google's ADK for agent orchestration, Modal Labs for serverless deployment and GPU access, and various specialized tools for content processing.

## Features

- **Intelligent Content Extraction**: Extract content from websites, videos, and other media sources
- **Smart Content Transformation**: Transform content between different formats with AI-powered adaptation
- **Multi-Platform Repurposing**: Automatically adapt content for different platforms and audiences
- **Automated Distribution**: Schedule and distribute content across multiple channels
- **Performance Analytics**: Track content performance and gain insights for optimization

## Architecture

ContentFlow AI is built on a multi-agent architecture using Google's ADK:

```
┌─────────────────────────────────────────────────────────────────┐
│                       ContentFlow AI Platform                    │
├───────────┬───────────┬───────────┬───────────┬─────────────────┤
│ Extraction│ Processing│ Transform │Distribution│    Analytics    │
│   Agents  │   Agents  │   Agents  │   Agents  │     Agents      │
├───────────┴───────────┴───────────┴───────────┴─────────────────┤
│                       ADK Agent Orchestration                    │
├─────────────────────────────────────────────────────────────────┤
│                     Modal Labs GPU Infrastructure                │
└─────────────────────────────────────────────────────────────────┘
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/contentflow-ai.git
   cd contentflow-ai
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

## Usage

### Running Locally

1. Start the development server:
   ```
   python -m src.api.main
   ```

2. Access the API at http://localhost:8000

### Deploying to Modal Labs

1. Deploy the application to Modal Labs:
   ```
   python -m modal.deployment deploy
   ```

2. Access the deployed API at the URL provided by Modal Labs

## Development

### Project Structure

```
contentflow-ai/
├── src/
│   ├── agents/         # Agent implementations
│   ├── tools/          # Tool implementations
│   ├── models/         # Data models
│   ├── api/            # API endpoints
│   └── utils/          # Utility functions
├── tests/              # Test files
├── modal/              # Modal Labs deployment
└── docs/               # Documentation
```

### Running Tests

```
pytest
```

## License

Apache 2.0
