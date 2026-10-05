# System Diagrams

This document contains Mermaid diagrams visualizing the architecture and flow of the Smart Waste Collection Monitoring System.

## 1. Incremental Development Flow

```mermaid
graph TD
    A[Requirement Analysis] --> B[Increment 1: Basic Bin Management]
    B --> C[Increment 2: Smart Monitoring & Simulation]
    C --> D[Increment 3: Collection Management]
    D --> E[Increment 4: Analytics & Dashboard]
    E --> F[Increment 5: Auto-Collection Optimization]
    F --> G[Final Deployed Prototype]
    
    style B fill:#e2e3e5,stroke:#333
    style C fill:#cce5ff,stroke:#333
    style D fill:#d1ecf1,stroke:#333
    style E fill:#fff3cd,stroke:#333
    style F fill:#d4edda,stroke:#333
```

## 2. Use Case Diagram

```mermaid
usecase
    actor Admin
    actor Operator
    actor SystemTimer
    
    usecase "Login" as UC1
    usecase "Manage Waste Bins" as UC2
    usecase "View Dashboard/Analytics" as UC3
    usecase "Simulate Sensor Data" as UC4
    usecase "Assign Vehicles" as UC5
    usecase "Update Collection Status" as UC6
    usecase "Auto-generate Alerts" as UC7
    
    Admin --> UC1
    Admin --> UC2
    Admin --> UC3
    Admin --> UC4
    Admin --> UC5
    
    Operator --> UC1
    Operator --> UC6
    
    SystemTimer --> UC7
    UC4 -.->|Triggers| UC7
```

## 3. System Flow Activity Diagram

```mermaid
stateDiagram-v2
    [*] --> IdleBin
    IdleBin --> SimulatingSensor: Admin Clicks Simulate
    SimulatingSensor --> CalculateLevel
    CalculateLevel --> IdleBin: Level < 80%
    CalculateLevel --> GenerateAlert: Level >= 80%
    GenerateAlert --> AutoCreateRequest: Increment 5 Feature
    AutoCreateRequest --> PendingCollection
    PendingCollection --> AssignedCollection: Admin Assigns Vehicle
    AssignedCollection --> InProgress: Operator Updates Status
    InProgress --> Completed: Operator Completes
    Completed --> ResetBin: System Action
    ResetBin --> IdleBin
```

## 4. Entity Relationship (ER) Diagram

```mermaid
erDiagram
    USER ||--o{ COLLECTION_REQUEST : "assigned to"
    BIN ||--o{ ALERT : generates
    BIN ||--o{ COLLECTION_REQUEST : requires
    VEHICLE ||--o{ COLLECTION_REQUEST : handles
    
    USER {
        int id PK
        string username
        string role
    }
    BIN {
        int id PK
        string bin_id
        string location
        int fill_level
        string status
    }
    VEHICLE {
        int id PK
        string vehicle_number
        string status
    }
    ALERT {
        int id PK
        string alert_type
        string priority
        string status
    }
    COLLECTION_REQUEST {
        int id PK
        string status
        datetime request_date
    }
```
