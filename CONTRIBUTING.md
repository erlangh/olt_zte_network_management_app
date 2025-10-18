# 🤝 Contributing to OLT ZTE C320 Management System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or SQLite for development)
- Git
- Basic knowledge of FastAPI and React

### Development Setup

1. **Fork and clone the repository**
```bash
git clone https://github.com/your-username/olt_zte_network_management_app.git
cd olt_zte_network_management_app
```

2. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Setup backend**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
python init_db.py
```

4. **Setup frontend**
```bash
cd frontend
npm install
cp .env.example .env
```

5. **Run development servers**
```bash
# Terminal 1 - Backend
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## 📝 Development Guidelines

### Code Style

#### Python (Backend)
- Follow PEP 8 style guide
- Use type hints where possible
- Maximum line length: 100 characters
- Use meaningful variable and function names
- Add docstrings to functions and classes

Example:
```python
def get_onu_by_serial(db: Session, serial_number: str) -> Optional[ONU]:
    """
    Retrieve ONU by serial number.
    
    Args:
        db: Database session
        serial_number: ONU serial number
        
    Returns:
        ONU object or None if not found
    """
    return db.query(ONU).filter(ONU.sn == serial_number).first()
```

#### JavaScript (Frontend)
- Use ES6+ features
- Use functional components with hooks
- Use meaningful component and variable names
- Add comments for complex logic
- Keep components small and focused

Example:
```javascript
// Good
const ONUStatusBadge = ({ status }) => {
  const color = status === 'online' ? 'green' : 'red';
  return <Tag color={color}>{status.toUpperCase()}</Tag>;
};

// Avoid large components
```

### Commit Messages

Follow conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```bash
feat(onu): add bulk ONU provisioning
fix(snmp): correct OID for ONU distance
docs(readme): add troubleshooting section
refactor(api): improve error handling
```

### Branch Naming

- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/documentation-update` - Documentation
- `refactor/what-changed` - Refactoring

## 🔍 Testing

### Backend Tests

```bash
cd backend
pytest
```

Add tests for new features:
```python
# tests/test_olt.py
def test_create_olt(client):
    response = client.post("/api/v1/olt/", json={
        "name": "Test OLT",
        "ip_address": "192.168.1.100",
        "snmp_community": "public"
    })
    assert response.status_code == 200
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📚 Documentation

### API Documentation
- Update OpenAPI/Swagger docs when adding endpoints
- Add examples for request/response
- Document error codes

### Code Documentation
- Add docstrings to Python functions
- Add JSDoc comments to JavaScript functions
- Update README.md if needed

### User Documentation
- Update user guide for new features
- Add screenshots if applicable
- Update QUICK_START.md if workflow changes

## 🐛 Bug Reports

When reporting bugs, include:

1. **Description**: Clear description of the bug
2. **Steps to reproduce**: Detailed steps
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Environment**:
   - OS and version
   - Python version
   - Node.js version
   - Browser (for frontend issues)
6. **Logs**: Relevant error messages
7. **Screenshots**: If applicable

Template:
```markdown
### Bug Description
Clear and concise description of the bug.

### Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

### Expected Behavior
What you expected to happen.

### Actual Behavior
What actually happened.

### Environment
- OS: Ubuntu 22.04
- Python: 3.11.2
- Browser: Chrome 120

### Logs
```
Error message here
```

### Screenshots
[Attach screenshots if applicable]
```

## ✨ Feature Requests

When requesting features, include:

1. **Feature description**: What you want
2. **Use case**: Why you need it
3. **Proposed solution**: How it could work
4. **Alternatives**: Other approaches considered

Template:
```markdown
### Feature Description
Clear description of the feature.

### Use Case
Why this feature is needed and who would use it.

### Proposed Solution
How you think it should work.

### Alternatives
Other ways this could be implemented.
```

## 🔄 Pull Request Process

1. **Before submitting**:
   - [ ] Code follows style guidelines
   - [ ] Tests pass
   - [ ] New tests added for new features
   - [ ] Documentation updated
   - [ ] No console errors/warnings
   - [ ] Commits are clean and meaningful

2. **Create pull request**:
   - Use descriptive title
   - Reference related issues
   - Describe changes made
   - List any breaking changes
   - Add screenshots for UI changes

3. **PR template**:
```markdown
## Description
Brief description of changes.

## Related Issues
Fixes #123

## Changes Made
- Added feature X
- Fixed bug Y
- Updated documentation Z

## Breaking Changes
None / List any breaking changes

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing done

## Screenshots
[If applicable]

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
```

4. **Review process**:
   - Address review comments
   - Make requested changes
   - Keep discussion focused and professional

## 🎯 Areas for Contribution

### High Priority
- [ ] Improve SNMP OID discovery for different OLT firmware versions
- [ ] Add support for more OLT vendors (Huawei, Fiberhome, etc.)
- [ ] Implement advanced filtering and search
- [ ] Add export to Excel/PDF functionality
- [ ] Improve error handling and user feedback

### Medium Priority
- [ ] Add email/SMS alerts
- [ ] Implement historical data tracking
- [ ] Add bulk ONU provisioning
- [ ] Improve cable route visualization
- [ ] Add API rate limiting

### Low Priority
- [ ] Dark/light theme toggle
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Advanced user roles and permissions

## 🛠️ Project Structure

```
backend/
├── app/
│   ├── api/endpoints/  # API route handlers
│   ├── core/           # Config, security
│   ├── db/             # Database setup
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   └── services/       # Business logic (SNMP, Telnet)

frontend/
├── src/
│   ├── components/     # Reusable components
│   ├── pages/          # Page components
│   ├── services/       # API client
│   └── store/          # State management
```

## 📞 Communication

- **GitHub Issues**: For bugs and features
- **Pull Requests**: For code contributions
- **Discussions**: For general questions

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the issue, not the person
- Help others learn and grow

## 🎓 Learning Resources

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)

### React
- [React Documentation](https://react.dev/)
- [Ant Design Components](https://ant.design/components/overview/)

### SNMP
- [Net-SNMP Tutorial](http://www.net-snmp.org/tutorial/)
- [SNMP OID Reference](https://oidref.com/)

## ❓ Questions?

If you have questions:
1. Check existing documentation
2. Search closed issues
3. Ask in GitHub Discussions
4. Create a new issue

---

**Thank you for contributing! 🙏**

Your contributions help make this project better for everyone.
