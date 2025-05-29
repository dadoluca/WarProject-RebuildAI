# War Use Case Analyzer - Frontend

A React-based frontend application for the War Use Case Analyzer API. This interface allows users to query post-conflict and humanitarian technology solutions, displaying structured analysis cards with risks, benefits, and mitigation strategies.

## Overview

The frontend is built with React and TypeScript, providing an intuitive interface to interact with the War Use Case Analyzer backend API. It features a clean, responsive design optimized for displaying complex analytical data in an accessible format.

## Features

- **Interactive Search**: Query input with configurable use case limits
- **Real-time Analysis**: Direct integration with the backend API
- **Structured Display**: Cards showing solutions, risks, mitigations, and benefits

## Technology Stack

- **React 18+** with TypeScript
- **CSS Modules** for component styling
- **Vite** for development and building
- **Modern JavaScript** (ES6+) with async/await

## Prerequisites

- Node.js 16+ and npm/yarn
- Running War Use Case Analyzer backend API (see backend README)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dadoluca/WarProject-RebuildAI.git
   cd war-use-case-analyzer/frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

4. **Open in browser**:
   Navigate to `http://localhost:5173` 

## Configuration

### Backend API Connection

The frontend connects to the backend API at `http://127.0.0.1:5000` by default. 


## Usage

### Basic Workflow

1. **Enter Query**: Type your question about post-conflict technology solutions
2. **Set Limits**: Adjust the number of solutions to generate (1-10)
3. **Search**: Click "Analyze" to send the query to the backend
4. **Review Results**: Browse through the generated cards with solutions, risks, and benefits

### Example Query

- "Lack of clean water after sudan conflict"
