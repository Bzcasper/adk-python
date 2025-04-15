# n8n Workflow Integration Guide

This guide shows how to set up n8n workflows to monetize your content extraction API.

## Prerequisites

1. n8n installed and running (cloud or self-hosted)
2. Your Modal Labs Content Extraction API deployed
3. API Token for authentication

## Setting Up Workflow Templates

Here are the core workflow templates you can implement:

### 1. Content Extraction Workflow

This workflow allows you to extract content from a webpage and generate a summary:

1. **HTTP Webhook Trigger**
   - Set up an incoming webhook in n8n
   - This will be the endpoint your customers hit to request content extraction

2. **Function Node: Validate Input**
   ```javascript
   // Validate incoming request
   const url = $input.body.url;
   const extractType = $input.body.extractType || "full_page";
   const format = $input.body.format || "markdown";
   
   if (!url) {
     return {
       error: true,
       message: "URL is required"
     };
   }
   
   return {
     url,
     extractType,
     format,
     maxLength: $input.body.maxLength || null,
     followLinks: $input.body.followLinks || false,
     depth: $input.body.depth || 1,
     includeImages: $input.body.includeImages || false
   };
   ```

3. **HTTP Request Node: Call Extraction API**
   - Method: POST
   - URL: `https://your-workspace--content-extraction-service-extract-web-content.modal.run`
   - Authentication: Bearer Token
   - Request Body:
     ```json
     {
       "url": "{{$node.Function.json.url}}",
       "extract_type": "{{$node.Function.json.extractType}}",
       "format": "{{$node.Function.json.format}}",
       "max_length": "{{$node.Function.json.maxLength}}",
       "follow_links": "{{$node.Function.json.followLinks}}",
       "depth": "{{$node.Function.json.depth}}",
       "include_images": "{{$node.Function.json.includeImages}}"
     }
     ```

4. **Wait Node: Delay**
   - Wait for 10 seconds to allow processing

5. **HTTP Request Node: Check Task Status**
   - Method: GET
   - URL: `https://your-workspace--content-extraction-service-get-task-status.modal.run?task_id={{$node["HTTP Request"].json.task_id}}`
   - Authentication: Bearer Token

6. **IF Node: Check Status**
   - Condition: `{{$node["HTTP Request1"].json.status}} === "completed"`
   - If True: Continue to summarization
   - If False: Loop back to Wait node

7. **HTTP Request Node: Summarize Content**
   - Method: POST
   - URL: `https://your-workspace--content-extraction-service-summarize-text.modal.run`
   - Authentication: Bearer Token
   - Request Body:
     ```json
     {
       "content": "{{$node["HTTP Request1"].json.data}}",
       "max_length": 500,
       "min_length": 100,
       "model": "Falconsai/text_summarization"
     }
     ```

8. **Respond to Webhook Node**
   - Response Body:
     ```json
     {
       "status": "success",
       "original_content": "{{$node["HTTP Request1"].json.data}}",
       "summary": "{{$node["HTTP Request2"].json.summary}}",
       "metadata": "{{$node["HTTP Request1"].json.metadata}}"
     }
     ```

### 2. Video Processing Workflow

This workflow extracts audio/video content and generates transcripts:

1. **HTTP Webhook Trigger**
   - Set up an incoming webhook in n8n

2. **Function Node: Validate Input**
   ```javascript
   // Validate incoming request
   const url = $input.body.url;
   const extractType = $input.body.extractType || "audio";
   const format = $input.body.format || "mp3";
   
   if (!url) {
     return {
       error: true,
       message: "URL is required"
     };
   }
   
   return {
     url,
     extractType,
     format,
     quality: $input.body.quality || "best",
     startTime: $input.body.startTime || null,
     endTime: $input.body.endTime || null,
     generateTranscript: $input.body.generateTranscript || false
   };
   ```

3. **HTTP Request Node: Call Video Extraction API**
   - Method: POST
   - URL: `https://your-workspace--content-extraction-service-extract-video-content.modal.run`
   - Authentication: Bearer Token
   - Request Body:
     ```json
     {
       "url": "{{$node.Function.json.url}}",
       "extract_type": "{{$node.Function.json.extractType}}",
       "format": "{{$node.Function.json.format}}",
       "quality": "{{$node.Function.json.quality}}",
       "start_time": "{{$node.Function.json.startTime}}",
       "end_time": "{{$node.Function.json.endTime}}",
       "generate_transcript": "{{$node.Function.json.generateTranscript}}"
     }
     ```

4. **Wait Node: Delay**
   - Wait for 30 seconds to allow processing

5. **HTTP Request Node: Check Task Status**
   - Method: GET
   - URL: `https://your-workspace--content-extraction-service-get-task-status.modal.run?task_id={{$node["HTTP Request"].json.task_id}}`
   - Authentication: Bearer Token

6. **IF Node: Check Status**
   - Condition: `{{$node["HTTP Request1"].json.status}} === "completed"`
   - If True: Continue to response
   - If False: Loop back to Wait node

7. **Respond to Webhook Node**
   - Response Body:
     ```json
     {
       "status": "success",
       "file_url": "{{$workflow.staticWebhookUrl}}/download/{{$node["HTTP Request1"].json.task_id}}.{{$node.Function.json.format}}",
       "transcript": "{{$node["HTTP Request1"].json.data.transcript}}",
       "metadata": "{{$node["HTTP Request1"].json.metadata}}"
     }
     ```

### 3. Monetization Workflow

This workflow handles payment processing and content delivery:

1. **HTTP Webhook Trigger**
   - Set up an incoming webhook to receive payment/subscription requests

2. **Switch Node: Payment Method**
   - Route based on payment method (Stripe, PayPal, etc.)

3. **HTTP Request Node: Process Payment**
   - Connect to your payment processor API
   - Verify payment status

4. **IF Node: Payment Successful**
   - Condition: `{{$node["HTTP Request"].json.status}} === "succeeded"`
   - If True: Continue to API key generation
   - If False: Return error

5. **Function Node: Generate API Key**
   ```javascript
   // Generate a unique API key
   const crypto = require('crypto');
   const apiKey = crypto.randomBytes(16).toString('hex');
   
   // Store in your database (this is just an example)
   const userEmail = $input.body.email;
   const plan = $input.body.plan;
   const expiryDate = new Date();
   expiryDate.setMonth(expiryDate.getMonth() + 1); // 1 month subscription
   
   return {
     apiKey,
     userEmail,
     plan,
     expiryDate: expiryDate.toISOString()
   };
   ```

6. **HTTP Request Node: Register in Auth System**
   - Method: POST
   - URL: `https://your-auth-api.com/register-key`
   - Request Body:
     ```json
     {
       "apiKey": "{{$node.Function.json.apiKey}}",
       "userEmail": "{{$node.Function.json.userEmail}}",
       "plan": "{{$node.Function.json.plan}}",
       "expiryDate": "{{$node.Function.json.expiryDate}}"
     }
     ```

7. **Email Node: Send API Key**
   - Send the API key and usage instructions to the customer

8. **Respond to Webhook Node**
   - Response Body:
     ```json
     {
       "status": "success",
       "message": "Subscription activated successfully",
       "apiKey": "{{$node.Function.json.apiKey}}",
       "expiryDate": "{{$node.Function.json.expiryDate}}"
     }
     ```

## Usage Tracking Workflow

This workflow tracks API usage for billing purposes:

1. **Webhook Trigger**
   - Set up to receive usage logs from your API

2. **Function Node: Process Usage Data**
   ```javascript
   // Process usage data
   const apiKey = $input.body.apiKey;
   const endpoint = $input.body.endpoint;
   const processingTime = $input.body.processingTime;
   const dataSize = $input.body.dataSize;
   
   // Calculate cost based on endpoint and usage
   let cost = 0;
   if (endpoint === "extract_web_content") {
     cost = 0.05; // $0.05 per web extraction
   } else if (endpoint === "extract_video_content") {
     cost = 0.10 + (processingTime / 60) * 0.02; // $0.10 base + $0.02 per minute
   } else if (endpoint === "summarize_text") {
     cost = 0.03; // $0.03 per summarization
   }
   
   return {
     apiKey,
     endpoint,
     timestamp: new Date().toISOString(),
     processingTime,
     dataSize,
     cost
   };
   ```

3. **Google Sheets Node or Database Node**
   - Log the usage data for billing purposes

4. **IF Node: Check Usage Limits**
   - Check if user has exceeded their plan limits
   - If exceeded, send notification

## Setting Up the Integration

1. Create the workflows in n8n
2. Deploy your Modal Labs API endpoints
3. Configure webhooks to connect your n8n workflows with the API
4. Set up payment processing with your preferred provider

## Business Models for Monetization

Here are several ways to monetize your content extraction service:

### 1. Subscription Plans

Create tiered subscription plans based on usage:

| Plan | Price | Features |
|------|-------|----------|
| Basic | $19.99/month | • 100 web extractions<br>• 50 text summarizations<br>• 5GB storage<br>• Email support |
| Professional | $49.99/month | • 500 web extractions<br>• 250 text summarizations<br>• 20GB storage<br>• 20 video extractions<br>• Priority support |
| Enterprise | $199.99/month | • Unlimited web extractions<br>• Unlimited summarizations<br>• 100GB storage<br>• 100 video extractions<br>• Custom integrations<br>• 24/7 support |

### 2. Pay-As-You-Go Model

Charge based on actual usage:

- Web content extraction: $0.05 per page
- Deep crawling with link following: $0.10 per page
- Video/audio extraction: $0.10 + $0.02 per minute
- Text summarization: $0.03 per request
- Custom Hugging Face model usage: $0.20 per request

### 3. API Credits System

Sell API credit packages that users can consume:

- 100 credits: $10
- 500 credits: $45
- 1000 credits: $80
- 5000 credits: $350

Credit consumption:
- Web extraction: 1 credit
- Video extraction (< 10 minutes): 3 credits
- Video extraction (> 10 minutes): 5 credits
- Text summarization: 1 credit
- Video transcription: 5 credits

### 4. White Label Solution

Offer your entire solution as a white-labeled service:

- Setup fee: $999
- Monthly maintenance: $299
- Revenue sharing: 15% of customer revenue
- Custom branding and domain
- Dedicated support and SLA

## Marketing Your Service

1. **Target Audiences**:
   - Content creators needing research assistance
   - Digital marketers creating content summaries
   - Researchers collecting web data
   - Developers building content-based applications
   - Education sector for resource compilation

2. **Unique Selling Points**:
   - Fully automated content extraction and processing
   - High-quality summaries from Hugging Face models
   - Reliable video and audio extraction
   - Easy integration with existing workflows
   - No coding required with n8n integration

3. **Content Marketing Strategy**:
   - Create blog posts demonstrating use cases
   - Publish case studies showing ROI for clients
   - Offer free tools that showcase limited functionality
   - Create video tutorials on integrating the API

## Scaling Your Business

As your service grows, consider these scaling strategies:

1. **Infrastructure Scaling**:
   - Modal Labs automatically scales computing resources
   - Monitor usage patterns to optimize costs
   - Implement caching for frequently requested content

2. **Team Building**:
   - Hire support staff as customer base grows
   - Bring on ML engineers to fine-tune extraction models
   - Add sales representatives for enterprise clients

3. **Feature Expansion**:
   - Add sentiment analysis capabilities
   - Implement content translation services
   - Develop specialized extraction for specific industries
   - Create branded reporting tools

## Legal Considerations

Make sure to address these important legal aspects:

1. **Terms of Service**:
   - Clearly state acceptable use policies
   - Define rate limits and fair usage policies
   - Include disclaimers about content copyright

2. **Privacy Policy**:
   - Detail how user data is stored and processed
   - Explain data retention periods
   - Define how API usage data is tracked

3. **Copyright Compliance**:
   - Emphasize that users must have rights to extract content
   - Implement DMCA takedown procedures
   - Consider content filtering for problematic material

4. **Data Protection**:
   - Implement GDPR compliance features
   - Secure storage of API keys and credentials
   - Regular security audits and penetration testing