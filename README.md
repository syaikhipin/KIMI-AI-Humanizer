---
title: Human Text Rewriter - Kimi K2
emoji: ✍️
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.9.1
app_file: app.py
pinned: false
---

# Human-Like Text Generator

Rewrite AI-generated or formal content to sound more natural and human-like using **Kimi-K2-Thinking**.

## Setup

Set these in the Space's **Settings → Repository secrets**:

- `API_KEY` - Your API key
- `API_URL` - API endpoint (default: https://openrouter.ai/api/v1/chat/completions)
- `MODEL` - Model name: `moonshotai/Kimi-K2-Thinking`

## Model

**Kimi-K2-Thinking** - Moonshot AI's reasoning model with thinking capabilities

## How It Works

1. Sends your content to Kimi-K2-Thinking
2. Applies a natural rewriting prompt
3. Filters out thinking tokens automatically
4. Streams the humanized output in real-time

## Usage

1. Paste your formal/AI-generated content
2. Click "Generate Human Version"
3. Watch the text appear in real-time
4. Copy the humanized result
