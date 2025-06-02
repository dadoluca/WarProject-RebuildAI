# Rebuild AI - Frontend

A **React-based frontend** for the War Use Case Analyzer API. This web interface allows users to explore post-conflict and humanitarian technology solutions, displaying **structured analysis cards** with associated risks, benefits, and mitigation strategies.

## 🖥️ Overview

The frontend is built with **React** and **TypeScript**, providing a clean, responsive interface to interact with the backend API. It’s optimized for displaying complex data in an accessible, user-friendly way.

## ✨ Features

* 🔎 **Interactive Search**: Configurable query input and result limits
* ⚡ **Real-time Analysis**: Direct API integration for up-to-date results
* 📊 **Structured Display**: Solutions, steps, risks, mitigations, and benefits

## ⚙️ Technology Stack

* **React 18+** (TypeScript)
* **CSS Modules** for modular styling
* **Vite** for fast builds and development
* **Modern JavaScript** (ES6+) with async/await

## 🛠️ Prerequisites

* **Node.js 16+**
* **NPM** or **Yarn**
* **Backend API** (see backend README for setup)

## 🚀 Installation

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

4. **Open in your browser**:
   [http://localhost:5173](http://localhost:5173)

## 🔧 Configuration

The frontend connects to the backend API by default at `http://127.0.0.1:5000`.
If needed, you can update this endpoint in the frontend source code.

## 📝 Usage

1. **Enter your query** about post-conflict technology solutions
2. **Set the number of solutions** (1–10)
3. **Click "Analyze"** to get results
4. **Review** the generated decision support cards, including:

   * Solutions and implementation steps
   * Risks and mitigations
   * Benefits

### Example Query

> *"Lack of clean water after Sudan conflict"*


