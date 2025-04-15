# ContentFlow AI - Modal Labs Deployment Guide

## Overview

This guide outlines the steps for deploying ContentFlow AI services to Modal Labs. ContentFlow AI consists of two main services:

1. **Main Service**: Handles content extraction, transformation, and API endpoints
2. **vLLM Service**: Provides high-performance model serving with optimized inference

## Prerequisites

Before deploying ContentFlow AI to Modal Labs, ensure you have the following:

- Modal Labs account and API token
- Python 3.10+ installed
- Required Python packages:
  - `modal>=0.55.4`
  - `vllm>=0.3.0`
  - `torch>=2.2.0`
  - `fastapi>=0.115.0`
  - `pydantic>=2.0.0`
  - `google-adk>=0.1.0`

## Setup Modal CLI

1. Install the Modal CLI:
   ```bash
   pip install modal
   ```

2. Authenticate with Modal:
   ```bash
   modal token new
   ```

3. Follow the prompts to authenticate and save your token.

## Project Structure

The ContentFlow AI deployment configuration is organized as follows:

- `modal/deployment.py`: Main deployment configuration for ContentFlow AI
- `src/models/serving/vllm_service.py`: vLLM service configuration
- `deploy.py`: Deployment script for both services

## Deployment Options

ContentFlow AI can be deployed to different environments:

- **Development**: For testing and development
- **Staging**: For pre-production testing
- **Production**: For production use

You can also deploy specific services:

- **All**: Deploy both main and vLLM services
- **Main**: Deploy only the main service
- **vLLM**: Deploy only the vLLM service

## Deployment Steps

### 1. Configure Environment Variables

Create a `.env` file in the project root with the following variables:

```
MODAL_ENVIRONMENT=development  # or staging, production
GOOGLE_API_KEY=your_google_api_key
```

### 2. Deploy Services

Use the deployment script to deploy ContentFlow AI services:

```bash
python deploy.py --env development --service all
```

Available options:
- `--env`: `development`, `staging`, `production` (default: `development`)
- `--service`: `all`, `main`, `vllm` (default: `all`)

### 3. Verify Deployment

After deployment, Modal Labs will provide URLs for your services:

- Main Service: `https://contentflow-ai-dev--dev.modal.run` (development)
- vLLM Service: `https://contentflow-ai-vllm-dev--dev.modal.run` (development)

For production:
- Main Service: `https://contentflow-ai--prod.modal.run`
- vLLM Service: `https://contentflow-ai-vllm--prod.modal.run`

## Testing Endpoints

You can test the deployed endpoints using the `test_endpoints.py` script:

```bash
python modal/test_endpoints.py --main-url https://contentflow-ai-dev--dev.modal.run --vllm-url https://contentflow-ai-vllm-dev--dev.modal.run
```

Available options:
- `--main-url`: URL of the main ContentFlow AI API
- `--vllm-url`: URL of the ContentFlow AI vLLM API
- `--test`: Specific test to run (`all`, `health`, `extraction`, `transformation`, `vllm-models`, `vllm-generate`, `vllm-download`)

## Available Endpoints

### Main Service Endpoints

- `GET /health`: Health check endpoint
- `POST /extract`: Extract content from a URL
- `POST /extract/audio`: Extract audio from a video URL
- `POST /analyze/audio`: Analyze audio content from a video URL
- `POST /transform`: Transform content to a different format

### vLLM Service Endpoints

- `GET /models`: List available models
- `GET /models/{model_name}`: Get information about a specific model
- `POST /models/generate`: Generate text using a specified model
- `POST /models/download/{model_name}`: Download a model for use with vLLM

## GPU Configuration

ContentFlow AI uses A100 GPUs for high-performance content processing and model serving. The GPU configuration is defined in the deployment files:

- `modal/deployment.py`: GPU configuration for content extraction and transformation
- `src/models/serving/vllm_service.py`: GPU configuration for vLLM model serving

## Monitoring and Logs

You can monitor your deployed services and view logs in the Modal Labs dashboard:

1. Go to [https://modal.com/apps](https://modal.com/apps)
2. Select your application (`contentflow-ai-dev` or `contentflow-ai-vllm-dev`)
3. View logs, metrics, and other information

## Troubleshooting

### Common Issues

1. **Deployment Fails**: Ensure you have the correct Modal Labs API token and permissions.
2. **GPU Not Available**: Check if you have GPU quota available in your Modal Labs account.
3. **Model Download Fails**: Ensure you have sufficient storage in your Modal volume.

### Getting Help

If you encounter issues with Modal Labs deployment, you can:

1. Check the [Modal Labs documentation](https://modal.com/docs)
2. Contact Modal Labs support
3. Open an issue in the ContentFlow AI repository

## Best Practices

1. **Environment Management**: Use different environments for development, staging, and production.
2. **Version Control**: Use version control for deployment configurations.
3. **Testing**: Test services locally before deploying to Modal Labs.
4. **Monitoring**: Monitor service performance and logs regularly.
5. **Security**: Keep API keys and credentials secure.

## Conclusion

By following this guide, you should be able to successfully deploy ContentFlow AI services to Modal Labs. The deployment process is designed to be flexible and scalable, allowing you to deploy services to different environments and with different configurations.

For more information on ContentFlow AI architecture and design, refer to the project documentation in the `docs` directory.
