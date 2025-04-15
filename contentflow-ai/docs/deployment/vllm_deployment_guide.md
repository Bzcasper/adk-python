# ContentFlow AI - vLLM Deployment Guide

## Overview

This guide provides detailed instructions for deploying the high-performance model serving capabilities of ContentFlow AI using vLLM and Modal Labs. The vLLM service enables efficient inference of large language models with optimized memory usage and throughput.

## Prerequisites

Before deploying the vLLM service, ensure you have:

- Modal Labs account with GPU quota (A100 recommended)
- Python 3.10+ installed
- All dependencies installed from `requirements.txt`

## Architecture

The vLLM service consists of the following components:

1. **vLLM Stub**: Modal Labs configuration for the vLLM service
2. **Model Volume**: Persistent storage for downloaded models
3. **GPU Configuration**: A100 GPU configuration for optimal performance
4. **API Endpoints**: FastAPI endpoints for model management and text generation

## Supported Models

The vLLM service supports the following models:

- **Mistral 7B Instruct v0.2** (mistral-7b)
- **Meta Llama 3 8B Instruct** (llama3-8b)
- **Microsoft Phi-3 Medium (14B)** (phi3-14b)
- **Google Gemma 7B Instruct** (gemma-7b)

All models are open-source and suitable for commercial use.

## Deployment Steps

### 1. Install Dependencies

First, install all required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure Modal Labs

Authenticate with Modal Labs:

```bash
modal token new
```

Follow the prompts to authenticate and save your token.

### 3. Deploy the vLLM Service

Deploy the vLLM service to Modal Labs:

```bash
python deploy.py --env development --service vllm
```

This will deploy the vLLM service to the development environment. For production, use:

```bash
python deploy.py --env production --service vllm
```

### 4. Download Models

After deployment, download the models you want to use:

```bash
curl -X POST "https://contentflow-ai-vllm-dev--dev.modal.run/models/download/mistral-7b"
```

Replace `mistral-7b` with the model you want to download.

## API Endpoints

The vLLM service provides the following API endpoints:

### List Models

```
GET /models
```

Returns a list of all available models with their information.

### Get Model Information

```
GET /models/{model_name}
```

Returns detailed information about a specific model.

### Generate Text

```
POST /models/generate
```

Generates text using a specified model.

Request body:
```json
{
  "prompt": "Write a short story about a robot learning to paint.",
  "model_name": "mistral-7b",
  "max_tokens": 512,
  "temperature": 0.7,
  "top_p": 0.9,
  "repetition_penalty": 1.1,
  "use_torch_compile": true
}
```

### Download Model

```
POST /models/download/{model_name}
```

Downloads a model for use with vLLM.

## Performance Optimization

The vLLM service uses several techniques to optimize performance:

1. **vLLM**: Efficient memory management and optimized inference
2. **torch.compile**: Just-in-time compilation for improved performance
3. **A100 GPU**: High-performance GPU for fast inference
4. **Modal Labs**: Serverless deployment with automatic scaling

## Integration with ContentFlow AI

The vLLM service is integrated with the ContentFlow AI platform through the TextTransformationAgent, which provides the following capabilities:

1. **Text Summarization**: Condenses content while preserving key information
2. **Style Transfer**: Transforms text to different writing styles
3. **Format Conversion**: Converts content between formats (markdown, HTML, JSON, etc.)

The TextTransformationAgent uses the vLLM service for high-performance inference, with fallback to Google's ADK when vLLM is unavailable.

## Monitoring and Troubleshooting

### Monitoring

You can monitor the vLLM service using the Modal Labs dashboard:

1. Go to [https://modal.com/apps](https://modal.com/apps)
2. Select the `contentflow-ai-vllm-dev` application
3. View logs, metrics, and other information

### Troubleshooting

Common issues and solutions:

1. **Model Download Fails**: Ensure you have sufficient storage in your Modal volume
2. **GPU Not Available**: Check if you have GPU quota available in your Modal Labs account
3. **Slow Inference**: Try using `torch.compile` for improved performance
4. **Memory Issues**: Reduce batch size or use a smaller model

## Best Practices

1. **Model Selection**: Choose the appropriate model for your task
2. **Parameter Tuning**: Adjust temperature, top_p, and other parameters for optimal results
3. **Caching**: Use caching for frequently used prompts
4. **Monitoring**: Monitor performance and resource usage

## Conclusion

By following this guide, you should be able to successfully deploy the vLLM service for high-performance model serving with ContentFlow AI. The service provides efficient inference of large language models with optimized memory usage and throughput, enabling high-quality text generation, summarization, and format conversion.

For more information on ContentFlow AI architecture and design, refer to the project documentation in the `docs` directory.
