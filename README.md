# **OPCUA ROUTER**

A simple OPC-UA communication bridge built with FastAPI, designed to connect Operational Technology (OT) assets with Information Technology (IT) systems in Industry 4.0 environments.

## 📋 **Overview**

After the rise of Industry 4.0, automation systems are increasingly required to transmit Operational Technology (OT) data to the Information Technology (IT) layer for analytics, monitoring, and enterprise-level decision-making. Reliable and standardized communication between these layers has become critical.

This project addresses that need by implementing an OPC-UA communication router built using FastAPI.
It acts as a bridge between OT assets—such as PLCs and industrial gateways—and IT applications, providing secure and seamless access to automation data through an OPC-UA Server.

The router exposes a clean REST API to the frontend, enabling applications to read, write, update, and delete OPC-UA node values. All interactions are logged and stored in a database, ensuring historical traceability and improved data management.
This provides a unified, scalable pathway for integrating industrial field data with modern IT systems.

Note:
The current implementation supports OPC-UA connectivity through freeopcua. Future versions may extend compatibility to additional OPC-UA stacks.

---

## 📡 **System Architecture**

![System Architecture](./diagram.png)

The router acts as a middleware layer:
- **OT Layer**: PLCs, industrial gateways, OPC-UA servers
- **Router Layer**: FastAPI application (this project)
- **IT Layer**: Web applications, analytics platforms, enterprise systems
- **Data Layer**: PostgreSQL for persistence and audit trails

---

## ✨ **Features**

- ✔ **Read All OPC-UA Nodes** from the database  
- ✔ **Read Specific Node** directly from the database or OPC-UA server  
- ✔ **Write Values** to an OPC-UA node + store changes  
- ✔ **Update Node** by fetching latest values from OPC-UA server  
- ✔ **Delete Node** from the database  
- ✔ Built with **FastAPI** for high performance  
- ✔ Automatic API documentation via Swagger UI  
- ✔ Clean, modular code architecture  
- ✔ Database integration for storing and retrieving node records 
- ✔ API Key authentication support, allowing secure access to all endpoints  
- ✔ A separate configuration file for managing runtime settings

---

## 🛠️ **Tech Stack**

| Component | Technology |
|-----------|-----------|
| API Framework | FastAPI |
| OPC-UA Client | freeopcua |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Testing | pytest + httpx |
| Authentication | API Key (Header-based) |
| Runtime | Python 3.10+ |

---

## 📦 **Project Structure**

```
OPCUA_ROUTER/
├── api/
│   └── endpoints/
│       └── opcua_router.py       # REST endpoint definitions
├── core/
│   ├── config.py                 # Application settings
│   └── security.py               # Authentication logic
├── db/
│   ├── db_actions.py             # Database operations
│   └── models.py                 # SQLAlchemy models
├── services/
│   └── opcua_driver.py           # OPC-UA client logic
├── tests/
│   ├── coverage/                 # Test coverage reports
│   ├── test_opcua_router.py      # API End point tests
│   ├── test_opcua_driver.py      # OPC-UA driver tests
│   └── conftest.py               # Pytest fixtures and configuration
├── external/
│   └── opcua_test_server/        # OPC-UA test server (submodule)
├── .env                          # Environment variables
├── diagram.png                   # Architecture diagram
├── main.py                       # Application entry point
├── models.py                     # Pydantic models
├── requirements.txt              # Python dependencies
└── README.md
```

---

## 🚀 **Getting Started**

### **Prerequisites**

- Python 3.10 or higher
- PostgreSQL database
- OPC-UA server
- Git

### **1. Clone the Repository**

```bash
git clone --recurse-submodules https://github.com/nithinkurian1988/opcua_router
cd opcua_router
```

**Note**: The `--recurse-submodules` flag ensures the OPC-UA test server submodule is cloned automatically.

If you've already cloned without submodules, initialize them with:
```bash
git submodule update --init --recursive
```

### **2. Set Up Virtual Environment**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source ./venv/bin/activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Configure Environment**

Copy the example environment file and modify it for your project:

```bash
cp .env.example .env
```

Then edit `.env` with your configuration:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/opcua_db

# Security
API_KEY=your-secret-key-here
API_KEY_NAME=X-API-Key

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# OPC-UA Server
OPCUA_SERVER_URL=opc.tcp://localhost:4840
```

**Note**: Never commit `.env` to version control. The `.env.example` file is provided as a template.

### **5. Set Up OPC-UA Server**

Before starting this application, you must have a working OPC-UA server running.

You have two options:

#### **Option 1: Use the Test OPC-UA Server (Recommended for Quick Start)**

This project includes a test OPC-UA server as a Git submodule for development and testing purposes.

**Installation:**

```bash
# Navigate to the test server directory
cd external/opcua_test_server

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source ./venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the test server
python opc_main.py
```

The test server will start on `opc.tcp://localhost:4849` by default.

#### **Option 2: Use freeopcua from GitHub**

Alternatively, you can set up an OPC-UA server using the official freeopcua implementation.

**Installation:**

```bash
# Install freeopcua
pip install opcua

# Clone the repository for examples
git clone https://github.com/FreeOpcUa/python-opcua.git
cd python-opcua/examples

# Run a sample server
python server-minimal.py
```

For more information, visit: 🔗 https://github.com/FreeOpcUa/python-opcua

**Note**: Ensure your OPC-UA server URL in the `.env` file matches the server you're running.

## ▶️ **Running the Application**

### **Start the Server**

```bash
uvicorn main:create_app --reload --host 0.0.0.0 --port 8000
```

### **Access Documentation**

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### **Run Tests**

```bash
cd opcua_router
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html:tests/coverage

# View coverage report
tests/coverage/index.html
```

---

## 🔌 **API Reference**

All endpoints require the `X-API-Key` header for authentication.

### **Authentication**

```http
X-API-Key: your-secret-key
```

### **Endpoints**

#### **GET `/opcua/read`**
Retrieve all OPC-UA nodes from the database.

**Response**:
```json
{
  "nodes": [
    {
      "node_id": 101,
      "value": 25.6,
      "timestamp": "2024-01-15T10:30:00Z"
        },
        {
      "node_id": 102,
      "value": 42.3,
      "timestamp": "2024-01-15T10:30:05Z"
    }
  ],
  "status": "Success",
  "message": "All node values retrieved successfully",
  "error": null
}
```

---

#### **GET `/opcua/read/{node_id}`**
Retrieve a specific node's latest value from the database, or directly from the OPC-UA server if not found in the database.

**Parameters**:
- `node_id` (path): Node identifier (e.g., `3`)

**Response**:
```json
{
  "status": "Success",
  "value": 89,
  "timestamp": "2025-11-20T23:20:10.472006+00:00",
  "message": "Node value retrieved successfully",
  "error": null
}
```

---

#### **POST `/opcua/write`**
Write a value to an OPC-UA node and persist to database.

**Request Body**:
```json
{
  "node_id": 3,
  "value": 22
}
```

**Response**:
```json
{
  "status": "Success",
  "message": "Node value written and stored successfully",
  "error": null
}
```

---

#### **PUT `/opcua/update/{node_id}`**
Fetch the latest value from OPC-UA server and update database.

**Parameters**:
- `node_id` (path): Node identifier (e.g., `3`)

**Response**:
```json
{
  "status": "Success",
  "value": 22,
  "timestamp": "2025-11-30T03:35:33.629847+00:00",
  "message": "Node updated successfully",
  "error": null
}
```

---

#### **DELETE `/opcua/delete/{node_id}`**
Remove a node entry from the database.

**Parameters**:
- `node_id` (path): Node identifier (e.g., `1`)

**Response**:
```json
{
  "status": "Success",
  "message": "Node deleted successfully",
  "error": null
}
```

---

## 🔐 **Security**

### **API Key Authentication**

Configure in `.env`:
```env
API_KEY=your-super-secret-key
API_KEY_NAME=X-API-Key
```

Include in all requests:
```bash
curl -X 'GET' \
  'http://localhost:8000/opcua/read' \
  -H 'accept: application/json' \
  -H 'X-API-Key: your-super-secret-key'
```

### **CORS Configuration**

Restrict frontend origins:
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourapp.com
```
## 🧪 **Testing**
#### **Postman Collection**

Import the pre-built Postman collection for testing all endpoints:

[📥 Postman Collection](https://nithinkurian1988-2214416.postman.co/workspace/Nithin-K-Kurian's-Workspace~d0409efb-27f8-4428-889d-a3e9a3cb7b16/collection/48886549-a6dd8e74-da5a-4bbb-869a-21d79e455047?action=share&source=copy-link&creator=48886549)

This collection includes pre-configured requests for all API endpoints with example payloads and headers.

## ⭐ **Future Improvements**

- API versioning (v1, v2, etc.)
- OAuth2 and JWT authentication support alongside API Key
- WebSocket support for live node monitoring
- Bulk write operations
- Node subscription management
- Frontend application with endpoint-specific UI components
- Real-time graphical visualization of sensor data
- Cloud deployment and hosting
- Multi-library OPC-UA client support (selectable via frontend or environment variable)
- Grafana dashboard templates and monitoring


