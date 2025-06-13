# QR Scavenger Hunt PWA - Architecture Document

## Technology Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS for responsive design
- **PWA**: Service Worker + Web App Manifest
- **QR Scanning**: @zxing/library for QR code detection
- **Camera**: getUserMedia API for camera access
- **State Management**: React Context + useState/useEffect
- **HTTP Client**: Fetch API

### Backend
- **Framework**: Flask (Python)
- **Authentication**: JWT tokens
- **Database**: SQLite for development (easily upgradeable to PostgreSQL)
- **CORS**: Flask-CORS for cross-origin requests
- **Real-time**: Server-Sent Events (SSE) for admin notifications

### Deployment
- **Frontend**: Static hosting (Vercel/Netlify compatible)
- **Backend**: Flask server (deployable to cloud platforms)
- **Database**: File-based SQLite (portable and simple)

## Data Models

### User
```python
{
    "id": "uuid",
    "email": "string",
    "phone": "string (optional)",
    "current_step": "integer (1-13)",
    "completed_steps": "array of integers",
    "revealed_locations": "array of integers",
    "created_at": "timestamp",
    "last_active": "timestamp"
}
```

### ScavengerStep
```python
{
    "id": "integer (1-13)",
    "name": "string",
    "clue": "string",
    "qr_code_url": "string",
    "qr_code_value": "string (for validation)"
}
```

### ScanEvent
```python
{
    "id": "uuid",
    "user_id": "uuid",
    "step_id": "integer",
    "scanned_at": "timestamp",
    "success": "boolean",
    "revealed_first": "boolean"
}
```

### AdminUser
```python
{
    "id": "uuid",
    "username": "string",
    "password_hash": "string",
    "created_at": "timestamp"
}
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login with email/phone
- `POST /api/auth/admin-login` - Admin login
- `POST /api/auth/logout` - Logout (clear session)
- `GET /api/auth/me` - Get current user info

### Scavenger Hunt
- `GET /api/hunt/current-step` - Get user's current step
- `POST /api/hunt/scan-qr` - Validate QR code and progress
- `POST /api/hunt/reveal-location` - Mark location as revealed
- `GET /api/hunt/progress` - Get user's complete progress

### Admin
- `GET /api/admin/users` - List all users and their progress
- `GET /api/admin/events` - Get scan events with filters
- `POST /api/admin/user/{id}/reset` - Reset user progress
- `POST /api/admin/user/{id}/skip-step` - Skip current step for user
- `GET /api/admin/notifications/stream` - SSE endpoint for real-time updates
- `PUT /api/admin/steps/{id}` - Update step QR code

## Frontend Architecture

### Component Structure
```
src/
├── components/
│   ├── common/
│   │   ├── Navbar.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── ErrorMessage.tsx
│   ├── hunt/
│   │   ├── ClueCard.tsx
│   │   ├── QRScanner.tsx
│   │   └── ProgressIndicator.tsx
│   ├── admin/
│   │   ├── Dashboard.tsx
│   │   ├── UserList.tsx
│   │   ├── EventLog.tsx
│   │   └── StepManager.tsx
│   └── auth/
│       ├── LoginForm.tsx
│       └── AdminLogin.tsx
├── pages/
│   ├── HuntPage.tsx
│   ├── AdminPage.tsx
│   └── LoginPage.tsx
├── hooks/
│   ├── useAuth.tsx
│   ├── useHunt.tsx
│   └── useAdmin.tsx
├── services/
│   ├── api.ts
│   ├── auth.ts
│   └── qrScanner.ts
├── types/
│   └── index.ts
└── utils/
    ├── constants.ts
    └── helpers.ts
```

### PWA Features
- **Offline Support**: Cache essential resources and API responses
- **Install Prompt**: Custom install button for mobile devices
- **Push Notifications**: Admin notifications for scan events
- **Responsive Design**: Mobile-first approach with touch interactions

## Security Considerations

### Authentication
- JWT tokens with expiration
- Secure password hashing for admin accounts
- Rate limiting on login attempts

### QR Code Validation
- Server-side validation of QR codes
- Unique QR values per location
- Prevention of QR code reuse/sharing

### Admin Security
- Separate admin authentication
- Role-based access control
- Audit logging for admin actions

## Scalability Notes

### Database
- SQLite for development and small deployments
- Easy migration path to PostgreSQL for larger scale
- Indexed queries for performance

### Real-time Features
- Server-Sent Events for admin notifications
- WebSocket upgrade path for more complex real-time features
- Event-driven architecture for scan notifications

### Deployment
- Containerized deployment ready
- Environment-based configuration
- Horizontal scaling support for backend

